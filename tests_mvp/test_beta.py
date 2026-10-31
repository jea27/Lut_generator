import io
import json
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient
from apps.api.main import create_app
from apps.api.jobs import Jobs
from apps.api.storage import atomic_json
from packages.colour_core import engine


class BetaTests(unittest.TestCase):
    def setUp(self):
        self.directory=tempfile.TemporaryDirectory();self.root=Path(self.directory.name)
        self.client=TestClient(create_app(self.root),base_url='http://127.0.0.1')
        csrf=self.client.get('/api/session').json()['csrf'];self.client.headers.update({'X-LumaForge-Local':'1','X-Color-Studio-Token':csrf})
        self.recipe=engine.Recipe().model_dump()

    def tearDown(self):self.client.close();self.directory.cleanup()

    def image(self):
        buffer=io.BytesIO();Image.new('RGB',(96,128),'orange').save(buffer,format='PNG')
        response=self.client.post('/api/images',files={'file':('fixture.png',buffer.getvalue(),'image/png')})
        self.assertEqual(response.status_code,200,response.text);return response.json()['id']

    def test_private_get_and_cross_origin_session_are_denied(self):
        other=TestClient(create_app(self.root/'other'),base_url='http://127.0.0.1')
        self.assertEqual(other.get('/api/presets').status_code,403)
        self.assertEqual(other.get('/api/session',headers={'Origin':'http://127.0.0.1:9999'}).status_code,403)
        self.assertEqual(self.client.get('/api/presets',headers={'Sec-Fetch-Site':'same-site'}).status_code,403)
        other.close()

    def test_presets_crud_groups_persist_and_corrupt_record_is_retained(self):
        p=self.client.post('/api/presets',json={'name':'One','group':'Portrait','recipe':self.recipe}).json()
        response=self.client.put('/api/presets/'+p['id'],json={'name':'Renamed','group':'Landscape','recipe':self.recipe})
        self.assertEqual(response.status_code,200);self.assertEqual(response.json()['group'],'Landscape')
        corrupt=self.root/'presets'/'bad.json';corrupt.write_text('{bad',encoding='utf-8')
        rows=self.client.get('/api/presets').json();self.assertEqual(len(rows),1);self.assertTrue(corrupt.exists())
        self.assertEqual(self.client.delete('/api/presets/'+p['id']).status_code,200)
        self.assertEqual(self.client.get('/api/presets').json(),[])

    def test_preferences_persist_without_session_secrets(self):
        value={'language':'en','welcome_seen':True,'export_format':'jpg'}
        self.assertEqual(self.client.put('/api/preferences',json=value).status_code,200)
        self.assertEqual(self.client.get('/api/preferences').json(),value)
        self.assertNotIn('csrf',(self.root/'preferences.json').read_text())

    def test_atomic_failed_serialization_does_not_truncate_previous_record(self):
        path=self.root/'test.json';atomic_json(path,{'good':1})
        with self.assertRaises(ValueError):atomic_json(path,{'bad':float('nan')})
        self.assertEqual(json.loads(path.read_bytes()),{'good':1})
        self.assertEqual(list(self.root.glob('.pending-*')),[])

    def test_batch_outputs_are_separate_from_inputs_and_downloadable(self):
        ids=[self.image(),self.image()];before={p.name:p.read_bytes() for p in (self.root/'images').glob('*')}
        response=self.client.post('/api/jobs',json={'source_ids':ids,'recipe':self.recipe,'format':'png'})
        self.assertEqual(response.status_code,200,response.text);identifier=response.json()['id']
        for _ in range(100):
            record=self.client.get('/api/jobs/'+identifier).json()
            if record['status'] not in ('queued','running','cancelling'):break
            time.sleep(.01)
        self.assertEqual(record['status'],'completed',record)
        self.assertEqual(record['completed'],2)
        self.assertEqual(before,{p.name:p.read_bytes() for p in (self.root/'images').glob('*')})
        exported=self.client.get(f'/api/jobs/{identifier}/files/0');self.assertEqual(exported.status_code,200)
        with Image.open(io.BytesIO(exported.content)) as image:self.assertEqual(image.size,(96,128))
        self.assertEqual(self.client.post('/api/jobs',json={'source_ids':[ids[0],ids[0]],'recipe':self.recipe}).status_code,422)

    def test_cancel_cooperative_and_recovery_never_claims_completion(self):
        with self.assertRaises(engine.ProcessingCancelled):engine.render(np.zeros((128,64,3),dtype='float32'),engine.Recipe(),cancel=lambda:True)
        identifier='abc';directory=self.root/'jobs'/identifier;directory.mkdir(parents=True)
        atomic_json(directory/'job.json',{'id':identifier,'status':'running','items':[]})
        jobs=Jobs(self.root/'jobs',threading.Lock())
        self.assertEqual(jobs.get(identifier)['status'],'interrupted')
        self.assertEqual(jobs.get(identifier)['items'],[])

    def test_demo_has_credits_and_is_not_a_research_claim(self):
        response=self.client.post('/api/demo/load',json={})
        self.assertEqual(response.status_code,200,response.text)
        self.assertFalse(response.json()['credits']['research_validated'])
        self.assertEqual(response.json()['source']['width'],1024)

    def test_running_batch_cancel_and_clear_guard(self):
        identifier=self.image();started=threading.Event();release=threading.Event()
        render=engine.render
        def controlled(*args,**kwargs):
            started.set();release.wait(3)
            return render(*args,**kwargs)
        with patch('apps.api.jobs.engine.render',side_effect=controlled):
            record=self.client.post('/api/jobs',json={'source_ids':[identifier],'recipe':self.recipe}).json()
            self.assertTrue(started.wait(2))
            cancelled=self.client.post('/api/jobs/'+record['id']+'/cancel',json={})
            self.assertEqual(cancelled.status_code,200)
            release.set()
            for _ in range(100):
                status=self.client.get('/api/jobs/'+record['id']).json()['status']
                if status=='cancelled':break
                time.sleep(.01)
        self.assertEqual(status,'cancelled')
        self.assertEqual(list((self.root/'jobs'/record['id']).glob('*.png')),[])
        self.assertEqual(list((self.root/'jobs'/record['id']).glob('*.part')),[])
        self.assertTrue((self.root/'images'/(identifier+'.png')).exists())

    def test_invalid_paths_corrupt_input_and_corrupt_preferences(self):
        self.assertEqual(self.client.get('/api/jobs/missing/files/0').status_code,404)
        self.assertEqual(self.client.put('/api/presets/not-a-uuid',json={'name':'x','recipe':self.recipe}).status_code,404)
        self.assertEqual(self.client.post('/api/images',files={'file':('bad.jpg',b'not jpeg','image/jpeg')}).status_code,422)
        (self.root/'preferences.json').write_text('{broken',encoding='utf-8')
        self.assertEqual(self.client.get('/api/preferences').json()['language'],'es')
        self.assertEqual((self.root/'preferences.json').read_text(),'{broken')
