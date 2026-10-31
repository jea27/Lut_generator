"""Adversarial local inputs; generated fixtures are not visual validation."""
import asyncio
import io
import json
import os
import tempfile
import unittest
import uuid
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from PIL import Image
from apps.api.limits import RequestLimits
from apps.api.main import create_app
from apps.api.storage import private_path
from apps.api.jobs import Jobs
from packages.colour_core import image_io
import threading


class InputSecurityTests(unittest.TestCase):
    def test_no_cdn_documentation_or_cross_origin_framing(self):
        with tempfile.TemporaryDirectory() as directory:
            with TestClient(create_app(directory),base_url='http://127.0.0.1') as client:
                for path in ('/docs','/redoc','/openapi.json'):
                    self.assertEqual(client.get(path).status_code,404)
                response=client.get('/api/health')
                self.assertEqual(response.headers['X-Frame-Options'],'SAMEORIGIN')
                csp=response.headers['Content-Security-Policy']
                self.assertIn("script-src 'self'",csp)
                self.assertIn("connect-src 'self'",csp)
                self.assertIn("frame-ancestors 'self'",csp)
                self.assertNotIn('unsafe-eval',csp)

    def test_negative_duplicate_and_missing_lengths_rejected_without_reading(self):
        async def exercise():
            touched=[]
            async def never(*args): touched.append(True)
            for lengths,expected in [([b'-1'],400),([b'1',b'1'],400),([],411),([b'9999999999999'],400)]:
                sent=[]
                async def send(message):sent.append(message)
                await RequestLimits(never)({'type':'http','path':'/api/images','method':'POST',
                     'headers':[(b'content-length',v) for v in lengths]},never,send)
                self.assertEqual(sent[0]['status'],expected)
            self.assertEqual(touched,[])
        asyncio.run(exercise())

    def test_stream_cannot_bypass_limit_with_false_content_length(self):
        app=FastAPI();app.add_middleware(RequestLimits)
        @app.post('/api/test')
        async def echo(request:Request):
            await request.body()
            return {'reached':True}
        client=TestClient(app)
        result=client.post('/api/test',content=b'x'*65537,headers={'Content-Length':'1'})
        self.assertEqual(result.status_code,413)
        self.assertNotIn('reached',result.text)
        client.close()

    def test_concurrent_heavy_requests_are_bounded_and_capacity_is_released(self):
        async def exercise():
            entered=asyncio.Event();release=asyncio.Event()
            async def handler(scope,receive,send):
                entered.set();await release.wait()
            limiter=RequestLimits(handler,capacity=1)
            scope={'type':'http','path':'/api/preview','method':'POST','headers':[(b'content-length',b'0')]}
            sent=[]
            async def send(message):sent.append(message)
            first=asyncio.create_task(limiter(scope,None,send));await entered.wait()
            await limiter(scope,None,send)
            self.assertEqual(sent[0]['status'],429)
            release.set();await first
            self.assertEqual(limiter.active,0)
        asyncio.run(exercise())

    def test_corrupt_png_crc_truncated_jpeg_and_unsupported_format(self):
        buffer=io.BytesIO();Image.new('RGB',(24,16),'red').save(buffer,format='PNG')
        corrupt=bytearray(buffer.getvalue());corrupt[29]^=1
        with self.assertRaises((ValueError,OSError)):image_io.decode(bytes(corrupt))
        buffer=io.BytesIO();Image.new('RGB',(24,16),'red').save(buffer,format='JPEG')
        with self.assertRaises((ValueError,OSError)):image_io.decode(buffer.getvalue()[:-40])
        buffer=io.BytesIO();Image.new('RGB',(24,16)).save(buffer,format='TIFF')
        with self.assertRaises(ValueError):image_io.decode(buffer.getvalue())

    def test_declared_dimensions_are_rejected_before_pixel_allocation(self):
        import struct,zlib
        buffer=io.BytesIO();Image.new('RGB',(2,2)).save(buffer,format='PNG')
        raw=bytearray(buffer.getvalue());raw[16:24]=struct.pack('>II',12001,2)
        raw[29:33]=struct.pack('>I',zlib.crc32(raw[12:29]))
        with self.assertRaises(ValueError):image_io.decode(bytes(raw))

    def test_exif_never_reaches_derived_export_or_upload_response(self):
        exif=Image.Exif();exif[315]='PRIVATE TEST AUTHOR';exif[270]='PRIVATE TEST DESCRIPTION'
        buffer=io.BytesIO();Image.new('RGB',(16,12),'red').save(buffer,format='JPEG',exif=exif)
        with tempfile.TemporaryDirectory() as directory:
            with TestClient(create_app(directory),base_url='http://127.0.0.1') as client:
                csrf=client.get('/api/session').json()['csrf']
                client.headers.update({'X-LumaForge-Local':'1','X-Color-Studio-Token':csrf})
                response=client.post('/api/images',files={'file':('private-name.jpg',buffer.getvalue())})
                self.assertEqual(response.status_code,200)
                self.assertNotIn('PRIVATE',response.text);self.assertNotIn('private-name',response.text)
                normalized=next((Path(directory)/'images').glob('*.png'))
                with Image.open(normalized) as image:self.assertEqual(dict(image.getexif()),{})
                false_length=client.post('/api/images',files={'file':('bad.jpg',buffer.getvalue())},headers={'Content-Length':'1'})
                self.assertEqual(false_length.status_code,413)

    def test_private_paths_and_tampered_job_ids_cannot_escape_store(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with self.assertRaises(ValueError):private_path(root,'..','outside.json')
            identifier=str(uuid.uuid4());job=root/'jobs'/identifier;job.mkdir(parents=True)
            (job/'job.json').write_text(json.dumps({'id':'../../outside','status':'running'}))
            jobs=Jobs(root/'jobs',threading.Lock())
            self.assertEqual(jobs.records,{})
            self.assertEqual(json.loads((job/'job.json').read_bytes())['status'],'running')
            # Windows junctions do not require Developer Mode/admin unlike symlinks.
            if os.name=='nt':
                import subprocess
                outside=root/'other';outside.mkdir()
                linked=root/'images'
                command=['cmd','/c','mklink','/J',str(linked),str(outside)]
                subprocess.run(command,check=True,capture_output=True)
                try:
                    with self.assertRaises(ValueError):create_app(root)
                finally:linked.rmdir()
            else:
                (root/'images').symlink_to(root/'jobs',target_is_directory=True)
                with self.assertRaises(ValueError):create_app(root)

    def test_well_formed_json_with_invalid_private_record_shapes_is_preserved_and_skipped(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with TestClient(create_app(root),base_url='http://127.0.0.1') as client:
                token=client.get('/api/session').json()['csrf']
                client.headers.update({'X-LumaForge-Local':'1','X-Color-Studio-Token':token})
                identifier=str(uuid.uuid4());preset=root/'presets'/(identifier+'.json')
                preset.write_text(json.dumps({'id':identifier,'name':{'bad':'shape'},'recipe':{}}))
                self.assertEqual(client.get('/api/presets').json(),[])
                self.assertTrue(preset.exists())
            identifier=str(uuid.uuid4());job=root/'jobs'/identifier;job.mkdir()
            state={'id':identifier,'status':'completed','items':[{'index':0,'status':'completed','filename':'../../secret'}]}
            (job/'job.json').write_text(json.dumps(state))
            jobs=Jobs(root/'jobs',threading.Lock())
            self.assertEqual(jobs.records,{})
            self.assertEqual(json.loads((job/'job.json').read_bytes()),state)
