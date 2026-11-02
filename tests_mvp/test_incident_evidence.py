"""Synthetic snapshot/path checks; never queries Security or actual user data."""
import json,os,shutil,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.name=='nt','Windows evidence collector')
class IncidentEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='audit-synthetic-',dir=ROOT/'.lumaforge-local');self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.snapshot=self.root/'baseline.json';self.output=self.root/'receipt.json'
        self.snapshot.write_text(json.dumps({'preferences.json':'a'*64}),encoding='utf-8')
        self.shell=shutil.which('powershell.exe')
        if not self.shell:self.skipTest('Built-in PowerShell unavailable')

    def run_collector(self,output):
        return subprocess.run([self.shell,'-NoProfile','-NonInteractive','-File',str(ROOT/'scripts/collect_private_event_evidence.ps1'),
            '-IncidentLocalTime','2026-11-02T07:12:44','-SnapshotPath',str(self.snapshot),'-OutputPath',str(output),'-ValidateOnly'],capture_output=True,text=True,timeout=20)

    def test_validate_only_converts_time_without_querying_security_or_data(self):
        result=self.run_collector(self.output);self.assertEqual(result.returncode,0,result.stderr)
        report=json.loads(self.output.read_bytes());self.assertEqual(report['status'],'validation_only_no_events_read')
        self.assertTrue(report['incident_utc'].startswith('2026-11-02T06:12:44'))
        self.assertEqual(report['matching_events'],[]);self.assertFalse(report['logging_configuration_changed'])
        self.assertFalse(report['data_files_read_or_modified'])

    def test_output_escape_and_overwrite_are_rejected_before_event_access(self):
        self.output.write_bytes(b'preserve evidence')
        self.assertNotEqual(self.run_collector(self.output).returncode,0);self.assertEqual(self.output.read_bytes(),b'preserve evidence')
        outside=ROOT/'incident-evidence-must-not-exist.json';self.assertFalse(outside.exists())
        self.assertNotEqual(self.run_collector(outside).returncode,0);self.assertFalse(outside.exists())

    def test_event_filter_handles_deletion_without_object_name_and_excludes_unrelated_paths(self):
        wrapper=self.root/'filter-fixture.ps1'
        wrapper.write_text(r'''
. $env:LF_TEST_SCRIPT -IncidentLocalTime '2026-11-02T07:12:44' -SnapshotPath $env:LF_TEST_BASELINE -OutputPath $env:LF_TEST_OUTPUT -ValidateOnly
function New-FixtureEvent($Id,$Object,$Handle){
 $lfElement='<Event><EventData><Data Name="ObjectName">'+$Object+'</Data><Data Name="ProcessId">0x123</Data><Data Name="HandleId">'+$Handle+'</Data></EventData></Event>'
 $lfEvent=[pscustomobject]@{Id=$Id;RecordId=1;TimeCreated=[datetime]'2026-11-02T06:12:44Z';Xml=$lfElement}
 $lfEvent | Add-Member -MemberType ScriptMethod -Name ToXml -Value {$this.Xml}
 return $lfEvent
}
$lfFixtures=@((New-FixtureEvent 4663 'C:\Synthetic\ColorStudioBetaData\preferences.json' '0x10'),(New-FixtureEvent 4660 '' '0x10'),(New-FixtureEvent 4663 'C:\Synthetic\Other\preferences.json' '0x11'),(New-FixtureEvent 4660 '' '0x11'))
$lfResult=Select-LfTargetEvents $lfFixtures @{'preferences.json'=$true}
if(@($lfResult.retained).Count -ne 2){throw 'Unrelated object or handle was retained'}
if(@($lfResult.retained | Where-Object id -eq 4660).Count -ne 1){throw 'Deletion without ObjectName was not correlated'}
''',encoding='utf-8')
        env=dict(os.environ,LF_TEST_SCRIPT=str(ROOT/'scripts/collect_private_event_evidence.ps1'),LF_TEST_BASELINE=str(self.snapshot),LF_TEST_OUTPUT=str(self.output))
        result=subprocess.run([self.shell,'-NoProfile','-NonInteractive','-File',str(wrapper)],env=env,capture_output=True,text=True,timeout=20)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(self.output.read_bytes())['status'],'validation_only_no_events_read')
