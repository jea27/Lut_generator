"""Exercise the exact inline Actions script with API doubles, without network."""
import json
import pathlib
import subprocess
import textwrap
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / '.github/workflows/alert-human.yml'


class AlertWorkflowTests(unittest.TestCase):
    def run_script(self, event, existing=False, reviewer='jea27'):
        script = textwrap.dedent(WORKFLOW.read_text('utf-8').split('          script: |\n', 1)[1])
        harness = r'''
const script = __SCRIPT__;
const event = __EVENT__;
const existing = __EXISTING__;
process.env.REVIEWER_GITHUB = __REVIEWER__;
const calls=[];
const context={eventName:event,repo:{owner:'jea27',repo:'Lut_generator'},issue:{number:event==='issues'?3:4},
  payload:{pull_request:{number:4,title:'[COL-001] Preparación',html_url:'https://github.com/jea27/Lut_generator/pull/4'}}};
const github={paginate:async()=>existing?[{number:5,body:'<!-- lumaforge-review-pr:4 -->'}]:[],
  rest:{issues:{listForRepo:()=>{},create:async args=>{calls.push(['create',args]);return {data:{number:5}};},
    addLabels:async args=>calls.push(['labels',args]),createComment:async args=>calls.push(['comment',args])}}};
const core={info:()=>{},setFailed:message=>calls.push(['failed',message])};
const AsyncFunction=Object.getPrototypeOf(async function(){}).constructor;
new AsyncFunction('github','context','core',script)(github,context,core)
  .then(()=>console.log(JSON.stringify(calls))).catch(error=>{console.error(error);process.exitCode=1;});
'''
        for name, value in [('SCRIPT', script), ('EVENT', event), ('EXISTING', existing), ('REVIEWER', reviewer)]:
            harness = harness.replace('__' + name + '__', json.dumps(value))
        result = subprocess.run(['node', '-'], input=harness, cwd=ROOT, text=True,
                                encoding='utf-8', capture_output=True, check=True)
        return json.loads(result.stdout)

    def test_pr_review_uses_issue_not_pr_comment(self):
        calls = self.run_script('pull_request')
        self.assertEqual([call[0] for call in calls], ['create', 'labels', 'comment'])
        self.assertEqual(calls[1][1]['labels'], ['needs-human'])
        self.assertEqual(calls[2][1]['issue_number'], 5)
        self.assertIn('@jea27', calls[2][1]['body'])

    def test_existing_review_does_not_duplicate_alert(self):
        self.assertEqual(self.run_script('pull_request', existing=True), [])

    def test_issue_decision_mentions_reviewer(self):
        calls = self.run_script('issues')
        self.assertEqual(calls[0][1]['issue_number'], 3)
        self.assertIn('@jea27', calls[0][1]['body'])

    def test_bad_reviewer_fails_before_api_calls(self):
        calls = self.run_script('issues', reviewer='@invalid')
        self.assertEqual([call[0] for call in calls], ['failed'])
