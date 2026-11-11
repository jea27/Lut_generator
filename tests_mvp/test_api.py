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
from pathlib import Path
from unittest.mock import patch
import uuid
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

    def test_project_survives_restart_with_same_media_recipe_and_render(self):
        source=self.upload();reference=self.upload()
        recipe={'intensity':.42,'exposure':.3,'look':{'enabled':True,'glow':.2}}
        draft={'name':'Synthetic project','source_id':source['id'],'reference_id':reference['id'],
               'recipe':recipe,'zoom':1.5,'split':63,'matched':True}
        before=self.client.post('/api/export/png',json={'source_id':source['id'],'recipe':recipe})
        self.assertEqual(before.status_code,200,before.text[:100])
        saved=self.client.post('/api/projects',json=draft)
        self.assertEqual(saved.status_code,201,saved.text)
        identifier=saved.json()['id']
        store=Path(self.directory.name)
        images={p.name:p.read_bytes() for p in (store/'images').iterdir()}
        with TestClient(create_app(store),base_url='http://127.0.0.1') as restarted:
            path='/api/projects/'+identifier
            self.assertEqual(restarted.get(path).status_code,403)
            csrf=restarted.get('/api/session').json()['csrf']
            restarted.headers.update({**H,'X-Color-Studio-Token':csrf})
            self.assertEqual(restarted.get('/api/projects').json(),{'projects':[saved.json()],'unreadable':0})
            reopened=restarted.get(path)
            self.assertEqual(reopened.status_code,200,reopened.text)
            value=reopened.json()
            self.assertEqual(value['source']['id'],source['id'])
            self.assertEqual(value['reference']['id'],reference['id'])
            self.assertEqual((value['source']['width'],value['source']['height']),(48,32))
            self.assertEqual((value['split'],value['zoom'],value['matched']),(63,1.5,True))
            self.assertEqual(value['recipe']['look']['glow'],.2)
            after=restarted.post('/api/export/png',json={'source_id':source['id'],'recipe':value['recipe']})
            self.assertEqual(after.status_code,200,after.text[:100])
            with Image.open(io.BytesIO(before.content)) as expected, Image.open(io.BytesIO(after.content)) as actual:
                self.assertEqual((actual.mode,actual.size,actual.tobytes()),(expected.mode,expected.size,expected.tobytes()))
                self.assertTrue(actual.info['icc_profile'])
        self.assertEqual({p.name:p.read_bytes() for p in (store/'images').iterdir()},images)

    def test_project_copies_never_overwrite_and_changed_media_is_rejected(self):
        asset=self.upload()
        draft={'name':'Synthetic project','source_id':asset['id'],'recipe':{}}
        first=self.client.post('/api/projects',json=draft)
        self.assertEqual(first.status_code,201,first.text)
        first_id=first.json()['id']
        record=Path(self.directory.name)/'projects'/(first_id+'.json')
        original=record.read_bytes()
        self.assertEqual(self.client.post('/api/projects',json={**draft,'source_id':'../preferences.json'}).status_code,409)
        self.assertEqual(self.client.post('/api/projects',json={**draft,'absolute_path':'ignored'}).status_code,422)
        with patch('apps.api.main.uuid.uuid4',return_value=uuid.UUID(first_id)):
            collision=self.client.post('/api/projects',json={**draft,'name':'Another copy'})
        self.assertEqual(collision.status_code,409)
        self.assertEqual(record.read_bytes(),original)
        second=self.client.post('/api/projects',json={**draft,'recipe':{'intensity':.2}})
        self.assertEqual(second.status_code,201,second.text)
        self.assertNotEqual(second.json()['id'],first_id)
        media=Path(self.directory.name)/'images'/(asset['id']+'.png')
        media.write_bytes(b'synthetic changed media')
        changed=self.client.get('/api/projects/'+first_id)
        self.assertEqual(changed.json()['detail'],'PROJECT_MEDIA_CHANGED')
        self.assertEqual(changed.status_code,409)
        media.rename(media.with_suffix('.retained'))
        missing=self.client.get('/api/projects/'+first_id)
        self.assertEqual(missing.json()['detail'],'PROJECT_MEDIA_UNAVAILABLE')
        self.assertEqual(record.read_bytes(),original)

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
