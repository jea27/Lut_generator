"""Incident regressions: workspace-only synthetic data, no real app or user store."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
import uuid
from unittest.mock import patch

import numpy as np
from fastapi.testclient import TestClient
from apps.api.main import create_app
from apps.api.jobs import Jobs,remove_owned_part
from packages.colour_core import engine,image_io

ROOT=Path(__file__).resolve().parents[1]


class PrivateDataPreservationTests(unittest.TestCase):
    def setUp(self):
        private=ROOT/'.lumaforge-local';private.mkdir(exist_ok=True)
        self.temporary=tempfile.TemporaryDirectory(prefix='incident-synthetic-',dir=private)
        self.addCleanup(self.temporary.cleanup);self.root=Path(self.temporary.name)
        self.data=self.root/'ColorStudioBetaData';(self.data/'images').mkdir(parents=True);(self.data/'presets').mkdir()
        self.ids=[str(uuid.UUID(int=n)) for n in range(1,7)]
        payload=image_io.encode(np.full((24,32,3),.4,dtype='float32'))
        for identifier in self.ids:(self.data/'images'/f'{identifier}.png').write_bytes(payload)
        recipe=engine.Recipe().model_dump()
        for n in (7,8):
            identifier=str(uuid.UUID(int=n));(self.data/'presets'/f'{identifier}.json').write_text(
                json.dumps({'id':identifier,'name':'Synthetic saved preset','recipe':recipe}),encoding='utf-8')
        (self.data/'preferences.json').write_text('{"workspace":"pro","language":"es"}',encoding='utf-8')
        self.before=self.snapshot();self.assertEqual(len(self.before),9)
        self.client=TestClient(create_app(self.data),base_url='http://127.0.0.1')
        self.addCleanup(self.client.close)
        token=self.client.get('/api/session').json()['csrf']
        self.client.headers.update({'X-LumaForge-Local':'1','X-Color-Studio-Token':token})

    def snapshot(self):
        return {p.relative_to(self.data).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.data.rglob('*') if p.is_file() and 'jobs' not in p.relative_to(self.data).parts}

    def assert_originals(self):self.assertEqual(self.snapshot(),self.before)

    def wait_job(self,identifier):
        for _ in range(300):
            row=self.client.get('/api/jobs/'+identifier).json()
            if row['status'] not in ('queued','running','cancelling'):return row
            time.sleep(.01)
        self.fail('Synthetic batch did not finish')

    def test_authenticated_legacy_delete_and_forged_consent_never_delete_private_files(self):
        for path in ('/api/images','/api/presets/'+str(uuid.UUID(int=7))):
            for _ in range(2):
                response=self.client.request('DELETE',path,json={'approved':True,'confirm':True},headers={'X-User-Approved':'yes'})
                self.assertEqual(response.status_code,423)
                self.assertEqual(response.json()['detail'],'PRIVATE_DATA_DELETION_DISABLED')
                self.assert_originals()

    def test_startup_restart_and_unreferenced_files_are_preserved(self):
        # No recipe references any image. A non-UUID PNG and invalid preset are
        # private content too, never eligible for automatic garbage collection.
        (self.data/'images'/'unclassified.png').write_bytes(b'inert private fixture')
        corrupt=self.data/'presets'/f'{uuid.UUID(int=9)}.json';corrupt.write_bytes(b'{invalid fixture')
        self.before=self.snapshot()
        for _ in range(2):
            with TestClient(create_app(self.data),base_url='http://127.0.0.1') as client:
                token=client.get('/api/session').json()['csrf'];client.headers.update({'X-LumaForge-Local':'1','X-Color-Studio-Token':token})
                self.assertEqual(len(client.get('/api/presets').json()),2)
                self.assertEqual(client.get('/api/preferences').status_code,200)
                self.assert_originals()

    def test_cancelled_batch_keeps_all_six_images_and_both_presets(self):
        entered=threading.Event();release=threading.Event()
        def render(*args,**kwargs):
            entered.set()
            if not release.wait(3):raise RuntimeError('Test cancellation barrier timed out')
            raise engine.ProcessingCancelled()
        with patch('apps.api.jobs.engine.render',side_effect=render):
            response=self.client.post('/api/jobs',json={'source_ids':self.ids[:2],'recipe':engine.Recipe().model_dump()})
            self.assertEqual(response.status_code,200);identifier=response.json()['id']
            try:
                self.assertTrue(entered.wait(3));self.client.post('/api/jobs/'+identifier+'/cancel').raise_for_status()
            finally:release.set()
            self.assertEqual(self.wait_job(identifier)['status'],'cancelled')
        self.assert_originals()

    def test_render_failure_keeps_all_original_data(self):
        with patch('apps.api.jobs.engine.render',side_effect=ValueError('Synthetic processing failure')):
            response=self.client.post('/api/jobs',json={'source_ids':self.ids[:1],'recipe':engine.Recipe().model_dump()})
            self.assertEqual(response.status_code,200)
            self.assertEqual(self.wait_job(response.json()['id'])['status'],'completed_with_errors')
        self.assert_originals()

    def test_failed_exclusive_part_creation_does_not_delete_preexisting_file(self):
        identifier=uuid.UUID(int=100);part=self.data/'jobs'/str(identifier)/'batch-001.png.part'
        def inject(*args,**kwargs):
            part.write_bytes(b'Preexisting synthetic private file; not this operation')
            return b'Synthetic newly encoded output'
        with patch('apps.api.jobs.uuid.uuid4',return_value=identifier),patch('apps.api.jobs.image_io.encode',side_effect=inject):
            response=self.client.post('/api/jobs',json={'source_ids':self.ids[:1],'recipe':engine.Recipe().model_dump()})
            self.assertEqual(response.status_code,200)
            self.assertEqual(self.wait_job(str(identifier))['status'],'completed_with_errors')
        self.assertEqual(part.read_bytes(),b'Preexisting synthetic private file; not this operation')
        self.assert_originals()

    def test_colliding_batch_directory_is_preserved(self):
        identifier=uuid.UUID(int=101);directory=self.data/'jobs'/str(identifier);directory.mkdir()
        sentinel=directory/'job.json';sentinel.write_bytes(b'Unclassified synthetic existing record')
        with patch('apps.api.jobs.uuid.uuid4',return_value=identifier):
            response=self.client.post('/api/jobs',json={'source_ids':self.ids[:1],'recipe':engine.Recipe().model_dump()})
            self.assertEqual(response.status_code,422)
        self.assertEqual(sentinel.read_bytes(),b'Unclassified synthetic existing record');self.assert_originals()

    def test_failed_job_save_does_not_leave_phantom_running_job(self):
        body={'source_ids':self.ids[:1],'recipe':engine.Recipe().model_dump()}
        with patch('apps.api.jobs.atomic_json',side_effect=PermissionError('Synthetic job write failure')):
            self.assertEqual(self.client.post('/api/jobs',json=body).status_code,422)
        response=self.client.post('/api/jobs',json=body);self.assertEqual(response.status_code,200)
        self.assertEqual(self.wait_job(response.json()['id'])['status'],'completed');self.assert_originals()

    def test_part_cleanup_checks_creation_and_file_identity(self):
        path=self.root/'owned.part';path.write_bytes(b'inert owned temporary')
        info=path.stat();identity=(info.st_dev,info.st_ino)
        remove_owned_part(path,None);self.assertTrue(path.exists())
        path.rename(self.root/'retained-original.part');path.write_bytes(b'inert replacement, preserve')
        remove_owned_part(path,identity);self.assertEqual(path.read_bytes(),b'inert replacement, preserve')
        info=path.stat();remove_owned_part(path,(info.st_dev,info.st_ino));self.assertFalse(path.exists())
        self.assert_originals()

    def test_failed_atomic_replacement_preserves_previous_preferences(self):
        with patch('apps.api.storage.os.replace',side_effect=PermissionError('Synthetic failed replace')):
            response=self.client.put('/api/preferences',json={'workspace':'creator','language':'en'})
            self.assertEqual(response.status_code,422)
        self.assert_originals();self.assertEqual(list(self.data.glob('.pending-*')),[])

    def test_uninstall_template_cannot_purge_appdata_and_ui_cannot_issue_cleanup(self):
        template=(ROOT/'packaging/nsis/installer.nsi').read_text(encoding='utf-8')
        self.assertNotIn('DeleteAppDataCheckbox',template)
        for line in template.splitlines():
            if not line.lstrip().startswith(';'):
                self.assertNotRegex(line,r'(?i)\b(?:rmdir|delete)\b.*\$(?:LOCALAPPDATA|APPDATA)')
        ui=(ROOT/'apps/web/src/App.vue').read_text(encoding='utf-8')
        self.assertNotIn("api('/images',{method:'DELETE'})",ui)
        self.assertIn('Images and presets protected',ui)


if __name__=='__main__':unittest.main()
