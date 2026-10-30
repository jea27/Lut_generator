import importlib.util
import pathlib
import unittest
import json
import tempfile
from unittest.mock import patch

p=pathlib.Path(__file__).resolve().parents[1] / 'scripts' / 'sync_github.py'
spec=importlib.util.spec_from_file_location('sync_github',p)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class WorkflowRules(unittest.TestCase):
    def setUp(self):
        self.code={'requires_pr':True}
        self.research={'requires_pr':False}
        self.open={'state':'open','labels':[{'name':'roadmap'}]}
        self.approved={'state':'closed','labels':[{'name':'approved'}]}
        self.openpr={'state':'open','merged_at':None}
        self.merged={'state':'closed','merged_at':'2026-10-30T11:00:00Z'}
    def test_initial(self):
        self.assertEqual(mod.derive_status(self.code,None,None),'planned')
    def test_in_progress(self):
        issue={**self.open,'labels':[{'name':'status:in-progress'}]}
        self.assertEqual(mod.derive_status(self.code,issue,None),'progress')
    def test_review(self):
        self.assertEqual(mod.derive_status(self.code,self.open,self.openpr),'review')
    def test_closed_without_approval(self):
        self.assertEqual(mod.derive_status(self.research,{'state':'closed','labels':[]},None),'review')
    def test_closed_approved_requires_merged_pr(self):
        self.assertEqual(mod.derive_status(self.code,self.approved,None),'review')
        self.assertEqual(mod.derive_status(self.code,self.approved,self.openpr),'review')
        self.assertEqual(mod.derive_status(self.code,self.approved,self.merged),'done')
    def test_research_approved_no_pr(self):
        self.assertEqual(mod.derive_status(self.research,self.approved,None),'done')
    def test_blocked_overrides_approved(self):
        issue={**self.approved,'labels':[{'name':'approved'},{'name':'blocked'}]}
        self.assertEqual(mod.derive_status(self.code,issue,self.merged),'blocked')
    def test_ids_are_explicit(self):
        self.assertEqual(mod.ids_from_title('[COL-012] LUT export'),{'COL-012'})
        self.assertFalse(mod.ids_from_title('ordinary title'))

class SyncIntegration(unittest.TestCase):
    def test_human_decision_blocks_approval(self):
        issue={'state':'closed','labels':[{'name':'approved'},{'name':'needs-human'}]}
        self.assertEqual(mod.derive_status({'requires_pr':False},issue,None),'blocked')

    def test_draft_is_not_ready_for_review(self):
        issue={'state':'open','labels':[{'name':'status:in-progress'}]}
        self.assertEqual(mod.derive_status({},issue,{'state':'open','draft':True}),'progress')

    def test_api_paginates_and_rejects_non_list(self):
        from io import BytesIO
        with patch.object(mod.urllib.request, 'urlopen', side_effect=[
            BytesIO(json.dumps([{}]*100).encode()), BytesIO(b'[]')]) as request:
            self.assertEqual(len(mod.get_json_pages('owner/repo','issues','test-token')),100)
            self.assertIn('page=2',request.call_args.args[0].full_url)
        with patch.object(mod.urllib.request, 'urlopen', return_value=BytesIO(b'{}')):
            with self.assertRaises(ValueError): mod.get_json_pages('owner/repo','issues','test-token')

    def test_sync_metadata_and_fallback(self):
        data={'project':{},'tasks':[{'id':'COL-001','requires_pr':True}]}
        issue={'state':'closed','title':'[COL-001] Investigación',
               'labels':[{'name':'roadmap'},{'name':'approved'}],
               'html_url':'https://github.com/owner/repo/issues/2','number':2,
               'body':'PRIVATE BODY','updated_at':'2026-10-30T10:00:00Z'}
        merged={'state':'closed','merged_at':'2026-10-30T11:00:00Z',
                'title':'[COL-001] Entrega','base':{'ref':'main'},
                'html_url':'https://github.com/owner/repo/pull/3','updated_at':'2026-10-30T11:00:00Z'}
        abandoned={**merged,'merged_at':None,'updated_at':'2026-10-30T12:00:00Z','html_url':'discarded'}
        wrong_base={**merged,'base':{'ref':'experiment'},'updated_at':'2026-10-30T13:00:00Z','html_url':'wrong'}
        with tempfile.TemporaryDirectory() as directory:
            path=pathlib.Path(directory)/'roadmap.json'
            path.write_text(json.dumps(data),encoding='utf-8')
            with patch.object(mod,'PATH',path), patch.dict(mod.os.environ,
                {'GITHUB_REPOSITORY':'owner/repo','GITHUB_TOKEN':'test-token'}), patch.object(
                    mod,'get_json_pages',side_effect=[[issue,{'pull_request':{},'title':'[COL-001] Fake'}],
                                                      [merged,abandoned,wrong_base]]):
                mod.main()
            output=json.loads(path.read_text('utf-8'))
            self.assertEqual(output['tasks'][0]['status'],'done')
            self.assertEqual(output['tasks'][0]['issue_number'],2)
            self.assertEqual(output['tasks'][0]['pr_url'],merged['html_url'])
            self.assertNotIn('PRIVATE BODY',path.read_text('utf-8'))
            fallback=path.with_name('fallback.js').read_text('utf-8')
            self.assertEqual(json.loads(fallback.split('=',1)[1].strip().removesuffix(';')),output)

    def test_open_delivery_takes_priority_over_previous_merge(self):
        self.assertGreater(mod.pr_rank({'state':'open','updated_at':'a'}),
                           mod.pr_rank({'state':'closed','merged_at':'yes','updated_at':'z'}))

    def test_failed_api_does_not_overwrite_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path=pathlib.Path(directory)/'roadmap.json'
            original='{"project": {}, "tasks": []}'
            path.write_text(original,encoding='utf-8')
            with patch.object(mod,'PATH',path), patch.dict(mod.os.environ,
                {'GITHUB_REPOSITORY':'owner/repo','GITHUB_TOKEN':'test-token'}), patch.object(
                    mod,'get_json_pages',side_effect=OSError('offline')):
                with self.assertRaises(OSError): mod.main()
            self.assertEqual(path.read_text('utf-8'),original)

if __name__=='__main__':
    unittest.main()
