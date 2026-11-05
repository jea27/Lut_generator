"""Real synthetic API exercise and fail-closed guest tools; never run an installer."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from fastapi.testclient import TestClient
import numpy as np
from apps.api.main import create_app
from packages.colour_core import image_io
from scripts.qa_guest_api import Client,exercise

ROOT=Path(__file__).resolve().parents[1]


class LocalClient:
    def __init__(self,client):self.client=client;self.headers={}
    def call(self,method,path,body=None,raw=None,content_type=None,expected=200):
        headers=dict(self.headers)
        if content_type:headers['Content-Type']=content_type
        kwargs={'json':body} if body is not None else {'content':raw} if raw is not None else {}
        response=self.client.request(method,path,headers=headers,**kwargs)
        if response.status_code!=expected:raise AssertionError((method,path,response.status_code,response.text))
        return response.content,dict(response.headers)
    def json(self,method,path,body=None):return json.loads(self.call(method,path,body)[0])


class VmCycleTests(unittest.TestCase):
    def setUp(self):
        folder=ROOT/'.lumaforge-local';folder.mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(prefix='cycle-synthetic-',dir=folder);self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.inputs=self.root/'inputs';self.inputs.mkdir()
        pixels=np.linspace(0,1,64*96*3,dtype='float32').reshape(64,96,3)
        for name,value in [('source.png',pixels),('reference.png',np.clip(pixels*.9+.04,0,1))]:
            (self.inputs/name).write_bytes(image_io.encode(value))

    def test_seed_then_restarted_app_exercises_real_exports_and_preserves_presets(self):
        data=self.root/'data';out=self.root/'first';out.mkdir()
        original={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in self.inputs.iterdir()}
        with TestClient(create_app(data),base_url='http://127.0.0.1') as client:
            state,result=exercise(LocalClient(client),self.inputs,out,cancellation=False,web_required=False)
        private_before={p.relative_to(data).as_posix():p.read_bytes() for p in (data/'images').glob('*')}
        second=self.root/'second';second.mkdir()
        with TestClient(create_app(data),base_url='http://127.0.0.1') as client:
            restored,after=exercise(LocalClient(client),self.inputs,second,state,cancellation=False,web_required=False)
        self.assertEqual(restored,state);self.assertEqual(result['png_sha256'],after['png_sha256'])
        self.assertTrue(after['creator_pro_export_equal']);self.assertTrue(after['lut_excludes_optics'])
        self.assertEqual(private_before,{p.relative_to(data).as_posix():p.read_bytes() for p in (data/'images').glob('*')})
        self.assertEqual(original,{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in self.inputs.iterdir()})
        self.assertNotIn('csrf',json.dumps(state));self.assertFalse(json.loads((second/'plan.json').read_bytes())['human_validated'])

    def test_client_rejects_remote_ports_and_request_paths_before_network(self):
        for port in (True,0,65536,'80'):
            with self.assertRaises(ValueError):Client(port)
        client=Client(12345)
        for path in ('https://example.org','//example.org','/../private'):
            with self.assertRaises(ValueError):client.call('GET',path)

    def test_api_cli_rejects_host_before_output_creation(self):
        output=self.root/'must-not-create'
        r=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/qa_guest_api.py'),'--output',str(output)],capture_output=True,text=True)
        self.assertNotEqual(r.returncode,0);self.assertIn('verified guest orchestrator',r.stderr);self.assertFalse(output.exists())

    def test_cycle_script_refuses_host_checkout_before_any_guest_operation(self):
        import shutil
        shell=shutil.which('powershell.exe')
        if not shell:self.skipTest('Windows PowerShell unavailable')
        r=subprocess.run([shell,'-NoProfile','-NonInteractive','-File',str(ROOT/'scripts/qa_vm_cycle.ps1'),'-ExpectedManifestSha256','a'*64],capture_output=True,text=True,timeout=20)
        self.assertNotEqual(r.returncode,0);self.assertIn('dedicated VM kit path',r.stderr)

    def test_host_assistant_refuses_changed_zip_before_vm_access_or_credentials(self):
        import shutil
        shell=shutil.which('powershell.exe')
        if not shell:self.skipTest('Windows PowerShell unavailable')
        archive=self.root/'synthetic.zip';archive.write_bytes(b'Not a real QA kit')
        # Windows PowerShell must initialize its own built-in module paths;
        # inheriting PS7's PSModulePath can hide even Get-FileHash in this host.
        env={k:v for k,v in os.environ.items() if k.upper()!='PSMODULEPATH'}
        r=subprocess.run([shell,'-NoProfile','-NonInteractive','-File',str(ROOT/'scripts/qa_vm_assistant.ps1'),'-KitZip',str(archive),'-ExpectedSha256','0'*64],capture_output=True,text=True,timeout=20,env=env)
        self.assertNotEqual(r.returncode,0);self.assertIn('ZIP hash mismatch',r.stderr)


if __name__=='__main__':unittest.main()
