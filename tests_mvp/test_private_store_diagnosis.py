"""Synthetic private snapshots; never read the real store or NTFS journal."""
import hashlib,json,os,shutil,subprocess,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.name=='nt','PowerShell Windows diagnosis')
class PrivateStoreDiagnosisTests(unittest.TestCase):
    def setUp(self):
        private=ROOT/'.lumaforge-local';private.mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(prefix='sd-',dir=private);self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.data=self.root/'ColorStudioBetaData';self.data.mkdir()
        self.snapshot=self.root/'snapshot.json';self.output=self.root/'result.json'
        self.shell=shutil.which('powershell.exe')
        if not self.shell:self.skipTest('Built-in PowerShell unavailable; no installation')

    def run_script(self,output):
        return subprocess.run([self.shell,'-NoProfile','-NonInteractive','-File',str(ROOT/'scripts/diagnose_private_store.ps1'),
                               '-SnapshotPath',str(self.snapshot),'-DataDir',str(self.data),'-OutputPath',str(output)],
                              capture_output=True,text=True,timeout=20)

    def test_missing_fixture_is_reported_without_modification_or_journal_read(self):
        image='images/11111111-1111-4111-8111-111111111111.png';missing='images/22222222-2222-4222-8222-222222222222.png'
        file=self.data/image;file.parent.mkdir();file.write_bytes(b'inert synthetic fixture')
        self.snapshot.write_text(json.dumps({image:hashlib.sha256(file.read_bytes()).hexdigest(),missing:'a'*64}),encoding='utf-8')
        result=self.run_script(self.output);self.assertEqual(result.returncode,0,result.stderr)
        report=json.loads(self.output.read_bytes());self.assertEqual(report['missing'],[missing]);self.assertTrue(report['present_hashes_equal'])
        self.assertEqual(report['usn']['status'],'not_requested');self.assertEqual(report['files_deleted'],0)
        self.assertEqual(len(report['directory_identities']),3)
        self.assertEqual(file.read_bytes(),b'inert synthetic fixture');self.assertFalse((self.data/missing).exists())

    def test_output_cannot_escape_or_overwrite_private_results(self):
        self.snapshot.write_text('{}',encoding='utf-8');self.output.write_bytes(b'preserve')
        result=self.run_script(self.output);self.assertNotEqual(result.returncode,0);self.assertEqual(self.output.read_bytes(),b'preserve')
        outside=ROOT/'diagnosis-must-not-be-created.json';self.assertFalse(outside.exists())
        self.assertNotEqual(self.run_script(outside).returncode,0);self.assertFalse(outside.exists())

    def test_changed_preference_is_reported_without_rewriting_it(self):
        file=self.data/'preferences.json';file.write_bytes(b'{"workspace":"pro"}')
        self.snapshot.write_text(json.dumps({'preferences.json':hashlib.sha256(b'{"workspace":"creator"}').hexdigest()}),encoding='utf-8')
        result=self.run_script(self.output);self.assertEqual(result.returncode,0,result.stderr)
        report=json.loads(self.output.read_bytes());self.assertEqual(report['changed'],['preferences.json'])
        self.assertFalse(report['present_hashes_equal']);self.assertEqual(file.read_bytes(),b'{"workspace":"pro"}')


if __name__=='__main__':unittest.main()
