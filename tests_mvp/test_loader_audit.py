"""Keep real native-source checks strict when Windows reports stale mappings."""
import hashlib,json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace
from scripts import smoke_beta as smoke


@unittest.skipUnless(os.name=='nt','Windows loader enumeration')
class LoaderAuditTests(unittest.TestCase):
    def test_owned_python_child_is_enumerated_by_loader_filename(self):
        # Windows venv python.exe may be a redirecting launcher with a child.
        interpreter=getattr(sys,'_base_executable',sys.executable)
        child=subprocess.Popen([interpreter,'-I','-S','-B','-c','import time;print("ready",flush=True);time.sleep(20)'],stdout=subprocess.PIPE)
        try:
            self.assertEqual(child.stdout.readline().strip(),b'ready')
            paths=smoke.loader_module_paths(child.pid)
            self.assertTrue(any(os.path.samefile(p,interpreter) for p in paths))
            self.assertTrue(any(p.name.lower().startswith('python') and p.suffix.lower()=='.dll' for p in paths))
        finally:child.terminate();child.wait(10);child.stdout.close()

    def test_manifest_case_is_windows_insensitive_but_hash_is_enforced(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);runtime=root/'runtime';runtime.mkdir();system=root/'Windows';system.mkdir()
            exe=runtime/'python.exe';exe.write_bytes(b'inert executable fixture')
            dll=runtime/'python314.dll';dll.write_bytes(b'inert DLL fixture')
            (runtime/'runtime-manifest.json').write_text(json.dumps({'files':{p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (exe,dll)}}),encoding='utf-8')
            with patch.dict(os.environ,{'SYSTEMROOT':str(system)}),patch.object(smoke,'loader_module_paths',return_value=[exe,runtime/'PYTHON314.DLL']):
                self.assertTrue(smoke.loaded_modules(SimpleNamespace(pid=1),exe)['payload_module_hashes_checked'])
                dll.write_bytes(b'changed fixture')
                with self.assertRaisesRegex(AssertionError,'native bytes'):smoke.loaded_modules(SimpleNamespace(pid=1),exe)

    def test_identical_dll_bytes_outside_bundle_are_not_accepted(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);runtime=root/'runtime';runtime.mkdir();system=root/'Windows';system.mkdir();outside=root/'other';outside.mkdir()
            exe=runtime/'python.exe';exe.write_bytes(b'inert executable fixture')
            dll=runtime/'python314.dll';dll.write_bytes(b'identical inert fixture');external=outside/dll.name;external.write_bytes(dll.read_bytes())
            (runtime/'runtime-manifest.json').write_text(json.dumps({'files':{p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (exe,dll)}}),encoding='utf-8')
            with patch.dict(os.environ,{'SYSTEMROOT':str(system)}),patch.object(smoke,'loader_module_paths',return_value=[exe,external]),self.assertRaises(AssertionError):
                smoke.loaded_modules(SimpleNamespace(pid=1),exe)


if __name__=='__main__':unittest.main()
