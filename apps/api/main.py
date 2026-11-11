"""Loopback-only LumaForge API. Images/presets are private local application data."""
import hashlib
import io
import json
import os
import threading
import time
import uuid
import secrets
import hmac
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse

import psutil
from fastapi import FastAPI, File, HTTPException, UploadFile, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
from PIL import Image, UnidentifiedImageError
from packages.colour_core import engine, image_io
from .storage import atomic_json, atomic_bytes, private_path, read_record
from .jobs import Jobs
from .limits import RequestLimits
from .capabilities import catalogue
from packages.shot_planner.planner import Setup, generate

ROOT=Path(__file__).resolve().parents[2]
LOCK=threading.Lock()


class Edit(BaseModel):
    model_config=ConfigDict(extra='forbid')
    source_id: str
    recipe: engine.Recipe


class Fit(BaseModel):
    source_id: str
    reference_id: str
    method: str = Field(default='lab-statistics',pattern='^(lab-statistics|mean-only)$')


class Preset(BaseModel):
    name: str = Field(min_length=1,max_length=80)
    recipe: engine.Recipe
    group: str = Field(default='',max_length=40)


class ProjectDraft(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str = Field(min_length=1, max_length=80, pattern=r'^[^\x00-\x1f\x7f]+$')
    source_id: str = Field(max_length=36)
    reference_id: str | None = Field(default=None, max_length=36)
    recipe: engine.Recipe
    split: float = Field(default=50, ge=0, le=100)
    zoom: float = Field(default=1, ge=1, le=3)
    matched: bool = False


class StoredProject(ProjectDraft):
    schema_version: Literal[1]
    id: str
    created_at: int = Field(ge=0, le=253402300799)
    source_sha256: str = Field(pattern='^[a-f0-9]{64}$')
    reference_sha256: str | None = Field(pattern='^[a-f0-9]{64}$')

    def summary(self):
        return {'id': self.id, 'name': self.name, 'created_at': self.created_at}


class Batch(BaseModel):
    model_config=ConfigDict(extra='forbid')
    source_ids: list[str] = Field(min_length=1,max_length=16)
    recipe: engine.Recipe
    format: str = Field(default='png',pattern='^(png|jpg)$')


class Preferences(BaseModel):
    model_config=ConfigDict(extra='forbid')
    language: str=Field(default='es',pattern='^(es|en)$')
    welcome_seen: bool=False
    export_format: str=Field(default='png',pattern='^(png|jpg)$')
    workspace: str=Field(default='creator',pattern='^(creator|pro)$')


class Plan(BaseModel):
    model_config=ConfigDict(extra='forbid')
    reference_id: str
    setup: Setup=Field(default_factory=Setup)
    recipe: engine.Recipe | None=None
    provider: str=Field(default='local-rules-v1',pattern='^local-rules-v1$')


@contextmanager
def measurement():
    process=psutil.Process(); peak=[process.memory_info().rss]; stop=threading.Event()
    def monitor():
        while not stop.wait(.01): peak[0]=max(peak[0],process.memory_info().rss)
    thread=threading.Thread(target=monitor,daemon=True); thread.start(); start=time.perf_counter()
    stats={}
    try: yield stats
    finally:
        stop.set(); thread.join()
        peak[0]=max(peak[0],process.memory_info().rss)
        stats.update(wall_ms=round((time.perf_counter()-start)*1000,1),rss_peak_mb=round(peak[0]/1024**2,1),
                     memory_method='process RSS sampled every 10ms; not exact allocation peak')


def create_app(data_dir=None):
    app=FastAPI(title='Color Studio local beta',version='0.3.0-beta.5',
                docs_url=None,redoc_url=None,openapi_url=None)
    default_data=Path(os.environ.get('LOCALAPPDATA',str(Path.home())))/'ColorStudioBetaData' if getattr(sys,'frozen',False) else ROOT/'.lumaforge-local'
    data=private_path(Path(data_dir or os.environ.get('LUMAFORGE_DATA_DIR',default_data))).resolve()
    images=private_path(data,'images'); presets=private_path(data,'presets')
    images.mkdir(parents=True,exist_ok=True); presets.mkdir(parents=True,exist_ok=True)
    session=secrets.token_urlsafe(32)
    jobs=Jobs(private_path(data,'jobs'),LOCK)
    app.add_middleware(RequestLimits)
    def same_origin(request):
        origin=request.headers.get('origin')
        if origin and origin.rstrip('/')!=str(request.base_url).rstrip('/'):return False
        return request.headers.get('sec-fetch-site','none') in ('same-origin','none')

    @app.middleware('http')
    async def local_only(request, call_next):
        host=request.headers.get('host','').split(':')[0]
        if host not in ('localhost','127.0.0.1'):
            return JSONResponse({'detail':'Loopback host required'},status_code=403)
        if request.url.path.startswith('/api/') and request.url.path not in ('/api/health','/api/session'):
            cookie=request.cookies.get('color_studio_session','')
            if not same_origin(request) or not hmac.compare_digest(cookie,session):
                return JSONResponse({'detail':'LOCAL_SESSION_REQUIRED'},status_code=403)
        if request.method not in ('GET','HEAD','OPTIONS'):
            origin=request.headers.get('origin')
            if request.headers.get('x-lumaforge-local')!='1' or not same_origin(request) or not hmac.compare_digest(request.headers.get('x-color-studio-token',''),session):
                return JSONResponse({'detail':'Local application header/origin required'},status_code=403)
        response=await call_next(request)
        response.headers['Cache-Control']='no-store'
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['Referrer-Policy']='no-referrer'
        response.headers['X-Frame-Options']='SAMEORIGIN'
        response.headers['Content-Security-Policy']=("default-src 'self'; script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; img-src 'self' blob: data:; font-src 'self' data:; "
            "connect-src 'self'; frame-src 'self'; frame-ancestors 'self'; object-src 'none'; "
            "base-uri 'none'; form-action 'self'")
        return response

    @app.exception_handler(ValueError)
    async def invalid(request,error): return JSONResponse({'detail':str(error)},status_code=422)

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request,error):
        # Do not echo raw private input or NaN into an error JSON response.
        return JSONResponse({'detail':'Invalid request: check recipe version, finite values and control ranges'},status_code=422)

    @app.exception_handler(UnidentifiedImageError)
    async def invalid_image(request,error): return JSONResponse({'detail':'Invalid JPEG/PNG image'},status_code=422)

    @app.exception_handler(Image.DecompressionBombError)
    @app.exception_handler(Image.DecompressionBombWarning)
    async def oversized_image(request,error): return JSONResponse({'detail':'Image dimensions exceed safe local limit'},status_code=413)

    @app.exception_handler(OSError)
    async def invalid_data(request,error): return JSONResponse({'detail':'Cannot read or write image data; verify format and local disk space'},status_code=422)

    def path_for(identifier, directory, suffix):
        try:
            if str(uuid.UUID(identifier))!=identifier: raise ValueError()
        except ValueError: raise HTTPException(404,'Unknown local asset')
        try:path=private_path(data,directory.relative_to(data),identifier+suffix)
        except ValueError:raise HTTPException(404,'Unknown local asset')
        if not path.is_file(): raise HTTPException(404,'Unknown local asset')
        return path

    def pixels(identifier, size=None):
        return image_io.decode(path_for(identifier,images,'.png').read_bytes(),max_side=size)

    def prepare_image(payload, *, embed_profile=True):
        rgb, alpha, notes = image_io.decode(payload)
        return image_io.encode(rgb, alpha, embed_profile=embed_profile), {
            'width': rgb.shape[1], 'height': rgb.shape[0], 'has_alpha': alpha is not None,
            'notes': notes, 'analysis': engine.analyze(rgb, alpha),
        }

    def image_asset(identifier, description):
        return {**description, 'id': identifier, 'preview_url': f'/api/images/{identifier}/preview'}

    def project_media(identifier):
        limit = 100 * 1024 * 1024
        try:
            path = path_for(identifier, images, '.png')
            with path.open('rb') as stream:
                size = os.fstat(stream.fileno()).st_size
                if size > limit:
                    raise HTTPException(409, 'PROJECT_MEDIA_UNAVAILABLE')
                payload = stream.read(size + 1)
        except (HTTPException, OSError):
            raise HTTPException(409, 'PROJECT_MEDIA_UNAVAILABLE') from None
        if len(payload) != size:
            raise HTTPException(409, 'PROJECT_MEDIA_UNAVAILABLE')
        return payload

    def restore_project_media(identifier, expected_digest):
        payload = project_media(identifier)
        if hashlib.sha256(payload).hexdigest() != expected_digest:
            raise HTTPException(409, 'PROJECT_MEDIA_CHANGED')
        try:
            rgb, alpha, notes = image_io.decode(payload, max_side=512)
            with Image.open(io.BytesIO(payload)) as image:
                width, height = image.size
        except (ValueError, OSError, Image.DecompressionBombError, Image.DecompressionBombWarning):
            raise HTTPException(409, 'PROJECT_MEDIA_UNAVAILABLE') from None
        return {'id': identifier, 'width': width, 'height': height, 'has_alpha': alpha is not None,
                'notes': notes, 'analysis': engine.analyze(rgb, alpha),
                'preview_url': f'/api/images/{identifier}/preview'}

    def read_project(path):
        record = StoredProject.model_validate(read_record(data, 'projects', path.name))
        if record.id != path.stem or str(uuid.UUID(record.id)) != record.id or not record.name.strip():
            raise ValueError('Invalid local project identity')
        if (record.reference_id is None) != (record.reference_sha256 is None):
            raise ValueError('Invalid local project reference')
        return record

    @app.get('/api/projects')
    def list_projects():
        with LOCK:
            directory = private_path(data, 'projects')
            records = []
            unreadable = 0
            for path in directory.glob('*.json'):
                try:
                    records.append(read_project(path).summary())
                except (ValueError, OSError):
                    unreadable += 1
        records.sort(key=lambda item: (item['created_at'], item['id']), reverse=True)
        return {'projects': records, 'unreadable': unreadable}

    @app.post('/api/projects', status_code=201)
    def save_project(body: ProjectDraft):
        with LOCK:
            directory = private_path(data, 'projects')
            if len(list(directory.glob('*.json'))) >= 100:
                raise HTTPException(409, 'PROJECT_LIMIT')
            name = body.name.strip()
            if not name:
                raise ValueError('Project name cannot be empty')
            recipe = engine.validate_recipe(body.recipe)
            source_digest = hashlib.sha256(project_media(body.source_id)).hexdigest()
            reference_digest = None
            if body.reference_id is not None:
                reference_digest = hashlib.sha256(project_media(body.reference_id)).hexdigest()
            identifier = str(uuid.uuid4())
            record = StoredProject(**body.model_dump(exclude={'name', 'recipe'}),
                                   schema_version=1, id=identifier, created_at=int(time.time()),
                                   name=name, recipe=recipe, source_sha256=source_digest,
                                   reference_sha256=reference_digest)
            try:
                atomic_json(private_path(data, 'projects', identifier + '.json'),
                            record.model_dump(), overwrite=False)
            except FileExistsError:
                raise HTTPException(409, 'PROJECT_COLLISION') from None
            return record.summary()

    @app.get('/api/projects/{identifier}')
    def open_project(identifier: str):
        with LOCK:
            path = path_for(identifier, private_path(data, 'projects'), '.json')
            try:
                record = read_project(path)
                recipe = engine.validate_recipe(record.recipe)
            except (ValueError, OSError):
                raise HTTPException(409, 'PROJECT_RECORD_INVALID') from None
            source = restore_project_media(record.source_id, record.source_sha256)
            reference = None
            if record.reference_id is not None:
                reference = restore_project_media(record.reference_id, record.reference_sha256)
        return {**record.summary(), 'recipe': recipe.model_dump(), 'source': source,
                'reference': reference, 'split': record.split, 'zoom': record.zoom,
                'matched': record.matched and reference is not None}

    @app.get('/api/health')
    def health(): return {'version':'0.3.0-beta.5','offline_processing':True,'domain':'encoded-sRGB-D65'}

    @app.get('/api/capabilities')
    def capabilities():return catalogue()

    @app.post('/api/planner')
    def plan(body:Plan):
        with LOCK,measurement() as stats:
            rgb,alpha,_=pixels(body.reference_id,512)
            result=generate(rgb,body.setup,alpha,body.recipe,body.provider)
        return {'plan':result,'metrics':stats}

    @app.get('/api/session')
    def bootstrap(request:Request):
        if not same_origin(request):raise HTTPException(403,'Same origin required')
        response=JSONResponse({'csrf':session})
        response.set_cookie('color_studio_session',session,httponly=True,samesite='strict',path='/api')
        return response

    @app.post('/api/images')
    def upload(file: UploadFile=File(...)):
        with LOCK,measurement() as stats:
            payload=file.file.read(32*1024*1024+1)
            if len(payload)>32*1024*1024: raise HTTPException(413,'Maximum upload 32 MiB')
            if len(list(images.glob('*.png')))>=32: raise HTTPException(409,'32 local images maximum; deletion is disabled for data protection')
            png, description = prepare_image(payload)
            identifier=str(uuid.uuid4())
            try:atomic_bytes(private_path(data,'images',identifier+'.png'),png,overwrite=False)
            except FileExistsError:raise HTTPException(409,'Existing local image preserved; retry import') from None
        return {**image_asset(identifier, description), 'metrics': stats}

    @app.post('/api/demo/load')
    def demo():
        directory=ROOT/'apps/demo'
        if not (directory/'credits.json').is_file():raise HTTPException(503,'Demo files are not bundled')
        credits = json.loads((directory/'credits.json').read_bytes())
        result = {'credits': credits}
        with LOCK, measurement() as stats:
            missing = []
            for role in ('source', 'reference'):
                # Internal demo pixels have already been normalized to sRGB.
                # The generated ICC creation timestamp would change their IDs on restart.
                png, description = prepare_image((directory/(role+'.jpg')).read_bytes(), embed_profile=False)
                digest = hashlib.sha256(png).hexdigest()
                identifier = str(uuid.uuid5(uuid.NAMESPACE_URL, f'urn:lumaforge:demo:{role}:{digest}'))
                path = private_path(data, 'images', identifier+'.png')
                if not path.exists():
                    missing.append((path, png))
                elif not path.is_file() or path.stat().st_size != len(png) or path.read_bytes() != png:
                    raise HTTPException(409, 'Existing local demo image differs and was preserved')
                result[role] = image_asset(identifier, description)
            if len(list(images.glob('*.png'))) + len(missing) > 32:
                raise HTTPException(409, 'The demo needs room for both local images. Existing images were preserved')
            for path, png in missing:
                try:
                    atomic_bytes(path, png, overwrite=False)
                except FileExistsError:
                    raise HTTPException(409, 'Existing local image preserved; retry demo') from None
        for role in ('source', 'reference'):
            result[role]['metrics'] = stats
        return result

    @app.get('/api/images/{identifier}/preview')
    def original_preview(identifier:str):
        with LOCK:
            rgb,alpha,_=pixels(identifier,1280)
            return Response(image_io.encode(rgb,alpha),media_type='image/png')

    @app.post('/api/fit')
    def match(body:Fit):
        with LOCK,measurement() as stats:
            a,aa,_=pixels(body.source_id,512); b,ba,_=pixels(body.reference_id,512)
            recipe=engine.fit(a,b,body.method,aa,ba)
        return {'recipe':recipe.model_dump(),'metrics':stats}

    @app.post('/api/preview')
    def preview(body:Edit):
        with LOCK,measurement() as stats:
            rgb,alpha,_=pixels(body.source_id,1280)
            output=engine.render(rgb,body.recipe,alpha=alpha)
            payload=image_io.encode(output,alpha)
        return Response(payload,media_type='image/png',headers={'X-Processing-Ms':str(stats['wall_ms']),
                         'X-RSS-Peak-MB':str(stats['rss_peak_mb'])})

    @app.post('/api/export/{format}')
    def export(format:str,body:Edit):
        if format not in ('png','jpg','cube','json'): raise HTTPException(404,'Unsupported format')
        with LOCK,measurement() as stats:
            recipe=engine.validate_recipe(body.recipe)
            if format=='cube': payload=engine.cube(recipe).encode(); media='text/plain'
            elif format=='json': payload=json.dumps(recipe.model_dump(),indent=2).encode(); media='application/json'
            else:
                rgb,alpha,_=pixels(body.source_id)
                payload=image_io.encode(engine.render(rgb,recipe,alpha=alpha),alpha,'PNG' if format=='png' else 'JPEG')
                media='image/png' if format=='png' else 'image/jpeg'
        return Response(payload,media_type=media,headers={'Content-Disposition':f'attachment; filename="lumaforge.{format}"',
                'X-Processing-Ms':str(stats['wall_ms']),'X-RSS-Peak-MB':str(stats['rss_peak_mb'])})

    @app.get('/api/presets')
    def list_presets():
        with LOCK:
            records=[]
            for p in sorted(presets.glob('*.json')):
                try:
                    record=read_record(data,'presets',p.name)
                    if record['id']!=p.stem or str(uuid.UUID(p.stem))!=p.stem:raise ValueError('Invalid private preset identity')
                    value=Preset.model_validate(record)
                    if not value.name.strip():raise ValueError('Invalid preset name')
                    records.append({'id':p.stem,**value.model_dump(),
                                    'recipe':engine.validate_recipe(value.recipe).model_dump()})
                except (ValueError,KeyError,TypeError,OSError):continue
            return records

    @app.post('/api/presets')
    def save_preset(body:Preset):
        with LOCK:
            if len(list(presets.glob('*.json')))>=100: raise HTTPException(409,'100 presets maximum')
            recipe=engine.validate_recipe(body.recipe)
            identifier=str(uuid.uuid4()); record={'id':identifier,'name':body.name.strip(),'group':body.group.strip(),'recipe':recipe.model_dump()}
            if not record['name']:raise ValueError('Preset name cannot be empty')
            try:atomic_json(private_path(data,'presets',identifier+'.json'),record,overwrite=False)
            except FileExistsError:raise HTTPException(409,'Existing local preset preserved; retry save') from None
        return record

    @app.put('/api/presets/{identifier}')
    def edit_preset(identifier:str,body:Preset):
        with LOCK:
            path=path_for(identifier,presets,'.json')
            if not body.name.strip():raise ValueError('Preset name cannot be empty')
            record={'id':identifier,'name':body.name.strip(),'group':body.group.strip(),'recipe':engine.validate_recipe(body.recipe).model_dump()}
            atomic_json(path,record)
            return record

    @app.get('/api/preferences')
    def preferences():
        try:return Preferences.model_validate(read_record(data,'preferences.json')).model_dump()
        except (OSError,ValueError):return Preferences().model_dump()

    @app.put('/api/preferences')
    def save_preferences(body:Preferences):
        with LOCK:atomic_json(private_path(data,'preferences.json'),body.model_dump())
        return body

    @app.post('/api/jobs')
    def start_batch(body:Batch):
        if len(set(body.source_ids))!=len(body.source_ids):raise ValueError('Duplicate batch input')
        with LOCK:
            for identifier in body.source_ids:path_for(identifier,images,'.png')
            return jobs.start(body.source_ids,body.recipe,body.format,lambda identifier:path_for(identifier,images,'.png'))

    @app.get('/api/jobs')
    def list_jobs():return [jobs.get(identifier) for identifier in list(jobs.records)]

    @app.get('/api/jobs/{identifier}')
    def job_status(identifier:str):
        try:return jobs.get(identifier)
        except KeyError:raise HTTPException(404,'Unknown batch')

    @app.post('/api/jobs/{identifier}/cancel')
    def cancel_batch(identifier:str):
        try:return jobs.cancel(identifier)
        except KeyError:raise HTTPException(404,'Unknown batch')

    @app.get('/api/jobs/{identifier}/files/{index}')
    def batch_file(identifier:str,index:int):
        try:
            record=jobs.get(identifier)
            item=next(i for i in record['items'] if i['index']==index and i['status']=='completed')
        except (KeyError,StopIteration):raise HTTPException(404,'Unknown batch output')
        try:output=private_path(data,'jobs',identifier,item['filename'])
        except ValueError:raise HTTPException(404,'Invalid batch output path')
        if output.parent!=data/'jobs'/identifier:raise HTTPException(404,'Invalid batch output path')
        return FileResponse(output,filename=item['filename'])

    @app.post('/api/presets/validate')
    def validate_preset(body:engine.Recipe): return engine.validate_recipe(body).model_dump()

    @app.delete('/api/presets/{identifier}')
    def delete_preset(identifier:str):
        # Session authentication is not proof of informed deletion consent.
        # Incident containment: no purge/cleanup bypass or automatic fallback.
        raise HTTPException(423,'PRIVATE_DATA_DELETION_DISABLED')

    @app.delete('/api/images')
    def clear_images():
        raise HTTPException(423,'PRIVATE_DATA_DELETION_DISABLED')

    dist=ROOT/'apps/web/dist'
    if dist.is_dir(): app.mount('/',StaticFiles(directory=dist,html=True),name='web')
    return app


app=create_app()
