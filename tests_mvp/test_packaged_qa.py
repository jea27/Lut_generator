"""Harness regressions, not evidence of installation on clean Windows."""
import io
import os
from pathlib import Path
import threading
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from scripts.smoke_beta import isolated_environment,read_ready


class PackagedHarnessTests(unittest.TestCase):
    def test_child_environment_drops_secrets_developer_paths_and_python_overrides(self):
        environment={'SYSTEMROOT':'C:/Windows','TEMP':'C:/Temp','PATH':'developer-tools',
                     'PYTHONHOME':'developer-runtime','PYTHONPATH':'source-tree',
                     'VIRTUAL_ENV':'developer-venv','GH_TOKEN':'private-fixture'}
        with patch.dict(os.environ,environment,clear=True):
            result=isolated_environment(Path('qa-data'))
            self.assertEqual(os.environ,environment)
        self.assertFalse({'GH_TOKEN','VIRTUAL_ENV','PYTHONHOME','PYTHONPATH'} & result.keys())
        windows=Path('C:/Windows')
        self.assertEqual(result['PATH'],os.pathsep.join(map(str,(windows/'System32',windows))))
        self.assertEqual(result['PYTHONNOUSERSITE'],'1')

    def test_startup_metadata_is_strict_and_rejects_eof_or_untrusted_output(self):
        self.assertEqual(read_ready(SimpleNamespace(stdout=io.BytesIO(b'{"port":54321}\n')))['port'],54321)
        for raw in (b'',b'not JSON',b'[]',b'{"port":true}',b'{"port":"1"}',b'{"port":65536}'):
            with self.subTest(raw=raw),self.assertRaisesRegex(RuntimeError,'metadata'):
                read_ready(SimpleNamespace(stdout=io.BytesIO(raw)))

    def test_silent_or_broken_program_cannot_hang_the_harness(self):
        done=threading.Event()
        class Silent:
            def readline(self,*args):done.wait(2);return b''
        try:
            with self.assertRaisesRegex(RuntimeError,'timed out'):
                read_ready(SimpleNamespace(stdout=Silent()),timeout=.02)
        finally:done.set()
