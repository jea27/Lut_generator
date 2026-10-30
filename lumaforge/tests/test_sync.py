import importlib.util
import pathlib
import unittest

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

if __name__=='__main__':
    unittest.main()
