"""Private-kit export bounds and guest guards; no VM or installer is executed."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import uuid
from scripts import prepare_vm_qa_kit as kit
from scripts import reproduce_private_deletion as probe

ROOT=Path(__file__).resolve().parents[1]


class VmKitSafetyTests(unittest.TestCase):
    def setUp(self):
        private=ROOT/'.lumaforge-local';private.mkdir(exist_ok=True)
        temporary=tempfile.TemporaryDirectory(prefix='vm-kit-synthetic-',dir=private)
        self.addCleanup(temporary.cleanup);self.root=Path(temporary.name)

    def test_output_outside_private_workspace_is_rejected_before_reading_input(self):
        outside=ROOT/('must-not-create-'+uuid.uuid4().hex)
        with self.assertRaises(ValueError):kit.prepare(self.root/'absent.json',outside)
        self.assertFalse(outside.exists())

    def test_existing_private_output_is_never_replaced(self):
        existing=self.root/'existing';existing.mkdir();record=existing/'receipt';record.write_bytes(b'preserve synthetic evidence')
        with self.assertRaises(ValueError):kit.prepare(self.root/'absent.json',existing)
        self.assertEqual(record.read_bytes(),b'preserve synthetic evidence')

    def test_dirty_or_unaudited_installer_cannot_enter_kit(self):
        artifact=self.root/'artifact.json';artifact.write_text(json.dumps({'dirty':True,'source':'a'*40}))
        target=self.root/'must-not-create'
        with self.assertRaises(ValueError):kit.prepare(artifact,target)
        self.assertFalse(target.exists())

    def test_real_beta3_without_transaction_ledger_uses_bound_runtime_and_launcher(self):
        record=json.loads((ROOT/'docs/evidence/RUNTIME_036_ARTIFACT.json').read_bytes())
        audit=json.loads((ROOT/'docs/evidence/RUNTIME_036_NSIS.json').read_bytes())
        identity=kit.previous_identity(record,audit)
        self.assertIsNone(identity['previous_installer_manifest_sha256'])
        self.assertEqual(identity['previous_launcher_sha256'],audit['native_components']['launcher']['sha256'])
        audit['installer_sha256']='0'*64
        with self.assertRaises(ValueError):kit.previous_identity(record,audit)

    def test_offline_guide_links_must_exist_and_stay_inside_the_kit(self):
        guide=self.root/'LEEME.md';guide.write_text('[Start](guide.md)\n[Microsoft](https://learn.microsoft.com/)')
        with self.assertRaises(ValueError):kit.verify_document_links(self.root)
        (self.root/'guide.md').write_text('Synthetic documentation')
        kit.verify_document_links(self.root)
        guide.write_text('[Outside](../private.md)')
        with self.assertRaises(ValueError):kit.verify_document_links(self.root)

    def test_pinned_legacy_source_works_without_git_and_rejects_tampering(self):
        raw=probe.legacy_source('apps/api/main.py')
        folder=self.root/'qa/legacy';folder.mkdir(parents=True);source=folder/'main.py';source.write_bytes(raw)
        with patch.object(probe,'ROOT',self.root),patch.object(probe.subprocess,'check_output',side_effect=AssertionError('Git must not run in the guest')):
            self.assertEqual(probe.legacy_source('apps/api/main.py'),raw)
            source.write_bytes(b'Untrusted synthetic replacement; never execute')
            with self.assertRaises(ValueError):probe.legacy_source('apps/api/main.py')

    @unittest.skipUnless(os.name=='nt','Windows guest guard')
    def test_guest_guard_rejects_normal_checkout_before_any_install_or_host_write(self):
        shell=shutil.which('powershell.exe')
        if not shell:self.skipTest('Built-in PowerShell unavailable')
        target=Path('C:/LF-QA');before=target.exists()
        result=subprocess.run([shell,'-NoProfile','-NonInteractive','-File',str(ROOT/'scripts/qa_guest_checks.ps1')],capture_output=True,text=True,timeout=20)
        self.assertNotEqual(result.returncode,0)
        self.assertRegex(result.stderr,'Requires an isolated Windows11 VM|Extract the verified kit')
        self.assertEqual(target.exists(),before)


if __name__=='__main__':unittest.main()
