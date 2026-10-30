"""Exercise the exact inline Actions script with API doubles, without network."""
import json
import pathlib
import subprocess
import textwrap
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / '.github/workflows/alert-human.yml'


class AlertWorkflowTests(unittest.TestCase):
    def run_script(self, event, existing=False, reviewer='jea27', malformed=False, crlf=False, empty=False, target='3'):
        script = textwrap.dedent(WORKFLOW.read_text('utf-8').split('          script: |\n', 1)[1])
        harness = r'''
const script = __SCRIPT__;
const event = __EVENT__;
const existing = __EXISTING__;
const malformed = __MALFORMED__;
const crlf = __CRLF__;
const empty = __EMPTY__;
const target = __TARGET__;
process.env.REVIEWER_GITHUB = __REVIEWER__;
const calls=[];
const context={eventName:event,repo:{owner:'jea27',repo:'Lut_generator'},issue:{number:event==='issues'?3:4},
  payload:{inputs:{issue_number:target},pull_request:{number:4,title:'[COL-001] Preparación'},issue:{number:3,
    title:'[LUMAFORGE] ACCIÓN REQUERIDA — Revisar evidencia',
    body:['Qué has terminado','Qué necesitas de mí','Por qué necesitas mi intervención',
      'Opciones disponibles','Tu recomendación','Cómo responder','Enlace'].map(x=>'## '+x+'\nContenido concreto').join('\n\n')}}};
if(malformed) context.payload.issue.body='Petición incompleta';
if(empty) context.payload.issue.body=context.payload.issue.body.replace('## Cómo responder\nContenido concreto','## Cómo responder\n');
if(crlf) context.payload.issue.body=context.payload.issue.body.replace(/\n/g,'\r\n');
const github={paginate:async(method)=>{
  if(!existing)return [];
  if(method===github.rest.issues.listForRepo)return [{number:5,body:'<!-- lumaforge-review-pr:4 -->'}];
  const digest=require('crypto').createHash('sha256').update(context.payload.issue.body).digest('hex').slice(0,16);
  return [{body:`<!-- lumaforge-notified-issue:3:${digest} -->`}];
},
  rest:{issues:{listForRepo:()=>{},listComments:()=>{},get:async args=>{calls.push(['get',args]);return {data:context.payload.issue};},create:async args=>{calls.push(['create',args]);return {data:{number:5}};},
    addLabels:async args=>calls.push(['labels',args]),createComment:async args=>calls.push(['comment',args])}}};
const core={info:()=>{},setFailed:message=>calls.push(['failed',message])};
const AsyncFunction=Object.getPrototypeOf(async function(){}).constructor;
new AsyncFunction('github','context','core','require',script)(github,context,core,require)
  .then(()=>console.log(JSON.stringify(calls))).catch(error=>{console.error(error);process.exitCode=1;});
'''
        for name, value in [('SCRIPT', script), ('EVENT', event), ('EXISTING', existing), ('REVIEWER', reviewer), ('MALFORMED', malformed), ('CRLF', crlf), ('EMPTY', empty), ('TARGET', target)]:
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
        self.assertTrue(calls[0][1]['title'].startswith('[LUMAFORGE] ACCIÓN REQUERIDA — '))
        for field in ['Qué has terminado','Qué necesitas de mí','Por qué necesitas mi intervención',
                      'Opciones disponibles','Tu recomendación','Cómo responder','Enlace']:
            self.assertIn('## '+field+'\n', calls[2][1]['body'])

    def test_existing_review_does_not_duplicate_alert(self):
        self.assertEqual(self.run_script('pull_request', existing=True), [])

    def test_issue_decision_mentions_reviewer(self):
        calls = self.run_script('issues')
        self.assertEqual(calls[0][1]['issue_number'], 3)
        self.assertIn('@jea27', calls[0][1]['body'])

    def test_bad_reviewer_fails_before_api_calls(self):
        calls = self.run_script('issues', reviewer='@invalid')
        self.assertEqual([call[0] for call in calls], ['failed'])

    def test_issue_request_is_not_notified_twice(self):
        self.assertEqual(self.run_script('issues', existing=True), [])

    def test_incomplete_request_fails_before_notifying(self):
        calls = self.run_script('issues', malformed=True)
        self.assertEqual([call[0] for call in calls], ['failed'])

    def test_windows_newlines_are_accepted(self):
        calls = self.run_script('issues', crlf=True)
        self.assertEqual(calls[0][0], 'comment')

    def test_empty_required_section_is_rejected(self):
        calls = self.run_script('issues', empty=True)
        self.assertEqual([call[0] for call in calls], ['failed'])

    def test_manual_action_reads_existing_issue(self):
        calls = self.run_script('workflow_dispatch')
        self.assertEqual([call[0] for call in calls], ['get', 'comment'])
        self.assertEqual(calls[-1][1]['issue_number'], 3)

    def test_manual_input_does_not_become_code(self):
        calls = self.run_script('workflow_dispatch', target='3; echo x')
        self.assertEqual([call[0] for call in calls], ['failed'])
