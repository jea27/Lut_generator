"""Loopback-only LumaForge API. Images/presets are private local application data."""
import io
import json
import os
import threading
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse

import psutil
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
from PIL import Image, UnidentifiedImageError
from packages.colour_core import engine, image_io

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
    app=FastAPI(title='LumaForge local',version='0.1.0')
    data=Path(data_dir or os.environ.get('LUMAFORGE_DATA_DIR',ROOT/'.lumaforge-local'))
    images=data/'images'; presets=data/'presets'
    images.mkdir(parents=True,exist_ok=True); presets.mkdir(parents=True,exist_ok=True)

    @app.middleware('http')
    async def local_only(request, call_next):
        host=request.headers.get('host','').split(':')[0]
        if host not in ('localhost','127.0.0.1'):
            return JSONResponse({'detail':'Loopback host required'},status_code=403)
        if request.method not in ('GET','HEAD','OPTIONS'):
            origin=request.headers.get('origin')
            if request.headers.get('x-lumaforge-local')!='1' or (origin and urlparse(origin).hostname not in ('localhost','127.0.0.1')):
                return JSONResponse({'detail':'Local application header/origin required'},status_code=403)
            limit=33*1024*1024 if request.url.path=='/api/images' else 64*1024
            length=request.headers.get('content-length')
            if length is None and request.method=='DELETE':length='0'
            if length is None:return JSONResponse({'detail':'Content-Length required'},status_code=411)
            try: size=int(length)
            except ValueError:return JSONResponse({'detail':'Invalid Content-Length'},status_code=400)
            if size>limit:return JSONResponse({'detail':'Request exceeds local size limit'},status_code=413)
        response=await call_next(request)
        response.headers['Cache-Control']='no-store'
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['Referrer-Policy']='no-referrer'
        return response

    @app.exception_handler(ValueError)
    async def invalid(request,error): return JSONResponse({'detail':str(error)},status_code=422)

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
        path=directory/(identifier+suffix)
        if not path.is_file(): raise HTTPException(404,'Unknown local asset')
        return path

    def pixels(identifier, size=None):
        return image_io.decode(path_for(identifier,images,'.png').read_bytes(),max_side=size)

    @app.get('/api/health')
    def health(): return {'version':'0.1.0','offline_processing':True,'domain':'encoded-sRGB-D65'}

    @app.post('/api/images')
    def upload(file: UploadFile=File(...)):
        with LOCK,measurement() as stats:
            payload=file.file.read(32*1024*1024+1)
            if len(payload)>32*1024*1024: raise HTTPException(413,'Maximum upload 32 MiB')
            if len(list(images.glob('*.png')))>=8: raise HTTPException(409,'8 local images maximum; clear temporary images first')
            rgb,alpha,notes=image_io.decode(payload)
            analysis=engine.analyze(rgb,alpha)
            identifier=str(uuid.uuid4())
            (images/(identifier+'.png')).write_bytes(image_io.encode(rgb,alpha))
            result={'id':identifier,'width':rgb.shape[1],'height':rgb.shape[0],'has_alpha':alpha is not None,
                    'notes':notes,'analysis':analysis,'preview_url':f'/api/images/{identifier}/preview'}
        return {**result,'metrics':stats}

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
            output=engine.render(rgb,body.recipe)
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
                payload=image_io.encode(engine.render(rgb,recipe),alpha,'PNG' if format=='png' else 'JPEG')
                media='image/png' if format=='png' else 'image/jpeg'
        return Response(payload,media_type=media,headers={'Content-Disposition':f'attachment; filename="lumaforge.{format}"',
                'X-Processing-Ms':str(stats['wall_ms']),'X-RSS-Peak-MB':str(stats['rss_peak_mb'])})

    @app.get('/api/presets')
    def list_presets():
        with LOCK:
            return [json.loads(p.read_text('utf-8')) for p in sorted(presets.glob('*.json'))]

    @app.post('/api/presets')
    def save_preset(body:Preset):
        with LOCK:
            if len(list(presets.glob('*.json')))>=100: raise HTTPException(409,'100 presets maximum')
            recipe=engine.validate_recipe(body.recipe)
            identifier=str(uuid.uuid4()); record={'id':identifier,'name':body.name,'recipe':recipe.model_dump()}
            (presets/(identifier+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
        return record

    @app.post('/api/presets/validate')
    def validate_preset(body:engine.Recipe): return engine.validate_recipe(body).model_dump()

    @app.delete('/api/presets/{identifier}')
    def delete_preset(identifier:str):
        with LOCK: path_for(identifier,presets,'.json').unlink()
        return {'removed':True}

    @app.delete('/api/images')
    def clear_images():
        with LOCK:
            for path in images.glob('*.png'): path.unlink()
        return {'removed':True,'presets_preserved':True}

    dist=ROOT/'apps/web/dist'
    if dist.is_dir(): app.mount('/',StaticFiles(directory=dist,html=True),name='web')
    return app


app=create_app()
