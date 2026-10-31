"""Loopback-only LumaForge API. Images/presets are private local application data."""
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
    app=FastAPI(title='Color Studio local beta',version='0.3.0-beta.2',
                docs_url=None,redoc_url=None,openapi_url=None)
    default_data=Path(os.environ.get('LOCALAPPDATA',str(Path.home())))/'ColorStudioBetaData' if getattr(sys,'frozen',False) else ROOT/'.lumaforge-local'
    data=Path(data_dir or os.environ.get('LUMAFORGE_DATA_DIR',default_data)).resolve()
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

    @app.get('/api/health')
    def health(): return {'version':'0.3.0-beta.2','offline_processing':True,'domain':'encoded-sRGB-D65'}

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
            if len(list(images.glob('*.png')))>=32: raise HTTPException(409,'32 local images maximum; clear temporary images first')
            rgb,alpha,notes=image_io.decode(payload)
            analysis=engine.analyze(rgb,alpha)
            identifier=str(uuid.uuid4())
            atomic_bytes(private_path(data,'images',identifier+'.png'),image_io.encode(rgb,alpha))
            result={'id':identifier,'width':rgb.shape[1],'height':rgb.shape[0],'has_alpha':alpha is not None,
                    'notes':notes,'analysis':analysis,'preview_url':f'/api/images/{identifier}/preview'}
        return {**result,'metrics':stats}

    @app.post('/api/demo/load')
    def demo():
        directory=ROOT/'apps/demo'
        if not (directory/'credits.json').is_file():raise HTTPException(503,'Demo files are not bundled')
        result={}
        for role in ('source','reference'):
            payload=(directory/(role+'.jpg')).read_bytes()
            result[role]=upload(UploadFile(file=io.BytesIO(payload),filename=role+'.jpg'))
        result['credits']=json.loads((directory/'credits.json').read_bytes())
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
            atomic_json(private_path(data,'presets',identifier+'.json'),record)
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
        with LOCK: path_for(identifier,presets,'.json').unlink()
        return {'removed':True}

    @app.delete('/api/images')
    def clear_images():
        with LOCK:
            if jobs.active():raise HTTPException(409,'Cancel the active batch before clearing images')
            for path in images.glob('*.png'): private_path(data,'images',path.name).unlink()
        return {'removed':True,'presets_preserved':True}

    dist=ROOT/'apps/web/dist'
    if dist.is_dir(): app.mount('/',StaticFiles(directory=dist,html=True),name='web')
    return app


app=create_app()
