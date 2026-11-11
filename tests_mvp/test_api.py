import io
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient
from apps.api.main import create_app

H={'X-LumaForge-Local':'1'}


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.directory=tempfile.TemporaryDirectory();self.client=TestClient(create_app(self.directory.name),base_url='http://127.0.0.1')
        token=self.client.get('/api/session').json()['csrf']
        self.client.headers.update({**H,'X-Color-Studio-Token':token})
        rgb=np.random.default_rng(3).integers(0,255,(32,48,3),dtype='uint8')
        buf=io.BytesIO();Image.fromarray(rgb).save(buf,format='PNG');self.payload=buf.getvalue()

    def tearDown(self):self.client.close();self.directory.cleanup()

    def upload(self):
        r=self.client.post('/api/images',files={'file':('synthetic.png',self.payload,'image/png')},headers=H)
        self.assertEqual(r.status_code,200,r.text);return r.json()

    def test_full_workflow_original_resolution_and_presets(self):
        a=self.upload();b=self.upload()
        r=self.client.post('/api/fit',json={'source_id':a['id'],'reference_id':b['id']},headers=H)
        self.assertEqual(r.status_code,200,r.text);recipe=r.json()['recipe'];body={'source_id':a['id'],'recipe':recipe}
        preview=self.client.post('/api/preview',json=body,headers=H)
        self.assertEqual(preview.status_code,200);self.assertIn('x-rss-peak-mb',preview.headers)
        for format in ('png','jpg','cube','json'):
            response=self.client.post('/api/export/'+format,json=body,headers=H)
            self.assertEqual(response.status_code,200,response.text[:100])
            if format in ('png','jpg'):
                with Image.open(io.BytesIO(response.content)) as image:self.assertEqual(image.size,(48,32))
            if format=='cube':self.assertIn('LUT_3D_SIZE 33',response.text)
            if format=='json':self.assertEqual(response.json()['domain'],'encoded-sRGB-D65')
        p=self.client.post('/api/presets',json={'name':'Synthetic test preset','recipe':recipe},headers=H)
        self.assertEqual(p.status_code,200);self.assertEqual(len(self.client.get('/api/presets').json()),1)
        self.assertEqual(self.client.delete('/api/images',headers=H).status_code,423)
        self.assertEqual(len(self.client.get('/api/presets').json()),1)
        self.assertEqual(self.client.get('/api/images/'+a['id']+'/preview').status_code,200)

    def test_loopback_and_origin_guards(self):
        self.assertEqual(self.client.post('/api/images',headers={'X-Color-Studio-Token':''}).status_code,403)
        self.assertEqual(self.client.post('/api/images',headers={**H,'Origin':'https://untrusted.example'}).status_code,403)
        self.assertEqual(self.client.get('/api/health',headers={'Host':'untrusted.example'}).status_code,403)

    def test_demo_reuses_both_assets_after_service_restart(self):
        store=Path(self.directory.name)
        original=self.upload()['id']
        first=self.client.post('/api/demo/load',json={})
        self.assertEqual(first.status_code,200,first.text[:200])
        self.assertEqual(len(list((store/'images').glob('*.png'))),3)
        # LCMS profiles use a wall-clock timestamp with one-second precision.
        time.sleep(1.1)
        script = """
import json
import sys
sys.path[:] = json.loads(sys.argv[2])
from fastapi.testclient import TestClient
from apps.api.main import create_app

with TestClient(create_app(sys.argv[1]), base_url='http://127.0.0.1') as client:
    csrf = client.get('/api/session').json()['csrf']
    client.headers.update({'X-LumaForge-Local': '1', 'X-Color-Studio-Token': csrf})
    response = client.post('/api/demo/load', json={})
    response.raise_for_status()
    print(json.dumps({role: response.json()[role]['id'] for role in ('source', 'reference')}))
"""
        ids = json.loads(subprocess.check_output(
            [sys.executable, '-I', '-S', '-B', '-c', script, str(store), json.dumps(sys.path)],
            cwd=Path(__file__).resolve().parents[1], timeout=30,
        ))
        self.assertEqual(ids,{role:first.json()[role]['id'] for role in ('source','reference')})
        self.assertEqual(len(list((store/'images').glob('*.png'))),3)
        preview=self.client.get(first.json()['source']['preview_url'])
        with Image.open(io.BytesIO(preview.content)) as image:
            self.assertTrue(image.info['icc_profile'])
        self.assertEqual(self.client.get('/api/images/'+original+'/preview').status_code,200)

    def test_demo_preserves_existing_images_when_capacity_or_content_conflicts(self):
        images=Path(self.directory.name)/'images'
        first=self.client.post('/api/demo/load',json={})
        self.assertEqual(first.status_code,200,first.text[:200])
        source=images/(first.json()['source']['id']+'.png')
        source.write_bytes(b'Inert changed local fixture')
        self.assertEqual(self.client.post('/api/demo/load',json={}).status_code,409)
        self.assertEqual(source.read_bytes(),b'Inert changed local fixture')
        for path in images.glob('*.png'):
            path.rename(path.with_suffix('.retained'))
        for index in range(31):
            (images/f'fixture-{index}.png').write_bytes(b'Inert capacity sentinel')
        before={p.name:p.read_bytes() for p in images.iterdir()}
        self.assertEqual(self.client.post('/api/demo/load',json={}).status_code,409)
        self.assertEqual({p.name:p.read_bytes() for p in images.iterdir()},before)

    def test_bad_image_recipe_and_unknown_id(self):
        response=self.client.post('/api/images',files={'file':('bad.png',b'not image','image/png')},headers=H)
        self.assertEqual(response.status_code,422)
        a=self.upload()
        response=self.client.post('/api/preview',json={'source_id':a['id'],'recipe':{'intensity':5}},headers=H)
        self.assertEqual(response.status_code,422)
        self.assertEqual(self.client.get('/api/images/not-a-uuid/preview').status_code,404)

    def test_oversized_request_rejected_before_multipart(self):
        response=self.client.post('/api/images',headers={**H,'Content-Length':str(34*1024*1024)})
        self.assertEqual(response.status_code,413)

    def test_nonfinite_json_is_rejected_without_echoing_input(self):
        response=self.client.post('/api/preview',content='{"source_id":"private","recipe":{"intensity":NaN}}',
                                  headers={**H,'Content-Type':'application/json'})
        self.assertEqual(response.status_code,422)
        self.assertNotIn('private',response.text)
