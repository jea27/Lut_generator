import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from scripts import human_reviews as h
from scripts import sync_product as product

ROOT=Path(__file__).resolve().parents[1]


class Reviews(unittest.TestCase):
    def setUp(self):
        self.manifest=h.policy(ROOT)
        self.f=next(f for f in self.manifest['features'] if f['id']=='glow')
        self.context=h.context(ROOT,self.f,self.manifest)

    def comment(self,id=100,kind='approve',feature=None):
        f=feature or self.f;c=h.context(ROOT,f,self.manifest)
        d={'feature':f['id'],**c,'decision':kind,'checklist':[c['id'] for c in f['review']['checklist']],
           'notes':'Synthetic correction only' if kind=='changes' else ''}
        return {'id':id,'body':h.PREFIX+json.dumps(d)+'\n```','user':copy.deepcopy(h.REVIEWER),
                'created_at':'2026-10-31T12:00:00Z','updated_at':'2026-10-31T12:00:00Z',
                'issue_url':f'https://api.github.com/repos/{h.REPO}/issues/{f["issue"]}'}

    def change(self,c,**fields):
        d=h.unpack(c['body'],h.PREFIX);d.update(fields);c['body']=h.PREFIX+json.dumps(d)+'\n```';return c

    def acknowledged(self,c):
        r=h.receipt(c,self.f['issue'],self.f,self.manifest,ROOT)
        return {'id':c['id']+1000,'user':copy.deepcopy(h.BOT),'body':h.RECEIPT+json.dumps(r)+'\n```'}

    def project(self,comments,f=None):
        return h.projection(comments,self.f['issue'],f or self.f,self.manifest,ROOT)

    def test_authorized_approval_and_history(self):
        c=self.comment();r=self.project([c,self.acknowledged(c)])
        self.assertEqual(r['state'],'approved');self.assertEqual(r['latest']['reviewer'],'jea27')
        self.assertEqual(r['latest']['at'],c['created_at']);self.assertEqual(len(r['history']),1)

    def test_shared_issue_does_not_approve_diffusion_fade_or_parent(self):
        c=self.comment();records=[c,self.acknowledged(c)]
        for id in ('diffusion','fade','manual-look'):
            f=next(f for f in self.manifest['features'] if f['id']==id)
            self.assertEqual(self.project(records,f)['state'],'pending')

    def test_unprocessed_comment_is_not_approved(self):self.assertEqual(self.project([self.comment()])['state'],'pending')

    def test_impostor_login_id_bot_and_wrong_issue_rejected(self):
        for replacement in ({'login':'attacker'},{'id':1},{'type':'Bot'}):
            c=self.comment();c['user'].update(replacement)
            with self.assertRaises(ValueError):h.decision(c,self.f['issue'],self.f,self.manifest)
        c=self.comment();c['issue_url']='https://api.github.com/repos/evil/repo/issues/68'
        with self.assertRaises(ValueError):h.decision(c,self.f['issue'],self.f,self.manifest)

    def test_incomplete_duplicate_checklist_unknown_fields_and_stale_revision(self):
        for fields in ({'checklist':[]},{'checklist':['behavior','behavior']},{'revision':'f'*64},
                       {'feature':'diffusion'},{'version':'9.9.9'},{'extra':'approve-all'},{'commit':'main;echo secret'}):
            with self.assertRaises(ValueError):h.decision(self.change(self.comment(),**fields),self.f['issue'],self.f,self.manifest)

    def test_strict_envelope_duplicate_keys_nonfinite_and_crlf(self):
        c=self.comment();c['body']=c['body'].replace('\n','\r\n')
        self.assertEqual(h.decision(c,self.f['issue'],self.f,self.manifest)['decision'],'approve')
        for body in (h.PREFIX+'{"feature":"glow","feature":"fade"}\n```',h.PREFIX+'{"x":NaN}\n```',self.comment()['body']+'extra'):
            with self.assertRaises(ValueError):h.unpack(body,h.PREFIX)

    def test_changes_need_observations_not_completed_checklist(self):
        c=self.change(self.comment(kind='changes'),checklist=[])
        self.assertEqual(h.decision(c,self.f['issue'],self.f,self.manifest)['decision'],'changes')
        with self.assertRaises(ValueError):h.decision(self.change(c,notes=' '),self.f['issue'],self.f,self.manifest)

    def test_changes_supersede_approval_without_reapproval_on_deletion(self):
        a=self.comment();b=self.comment(101,'changes')
        records=[a,self.acknowledged(a),b,self.acknowledged(b)]
        self.assertEqual(self.project(records)['state'],'changes_requested')
        records.remove(b);self.assertEqual(self.project(records)['state'],'needs_review')

    def test_edit_or_delete_invalidates_and_retains_history(self):
        c=self.comment();receipt=self.acknowledged(c)
        c['updated_at']='2026-10-31T12:01:00Z'
        self.assertEqual(self.project([c,receipt])['state'],'needs_review')
        self.assertEqual(len(self.project([receipt])['history']),1)
        c=self.comment();receipt=self.acknowledged(c);self.change(c,notes='edited within same second')
        self.assertEqual(self.project([c,receipt])['state'],'needs_review')

    def test_fake_bot_receipt_ignored_and_no_private_notes_in_projection(self):
        c=self.change(self.comment(),notes='C:\\Users\\private\\file github_pat_PRIVATE_PERSON')
        receipt=self.acknowledged(c);r=self.project([c,receipt])
        self.assertNotIn('PRIVATE_PERSON',json.dumps(r));self.assertNotIn('private',json.dumps(r))
        receipt['user']['id']=1;self.assertEqual(self.project([c,receipt])['state'],'pending')

    def test_duplicate_receipts_idempotent(self):
        c=self.comment();b=self.acknowledged(c)
        self.assertEqual(len(self.project([c,b,b])['history']),1)

    def test_approving_one_capability_does_not_clear_sibling_corrections(self):
        a=self.comment();fa=next(f for f in self.manifest['features'] if f['id']=='diffusion')
        b=self.comment(101,'changes',fa)
        br={'id':1101,'user':h.BOT,'body':h.RECEIPT+json.dumps(h.receipt(b,fa['issue'],fa,self.manifest))+'\n```'}
        records=[a,self.acknowledged(a),b,br]
        class API:
            def pages(self,endpoint):return records
            def get(self,endpoint):return {'labels':[{'name':'agent-action-required'}]}
        with patch.object(h,'post') as write:
            h.reconcile_queue(API(),self.f['issue'],self.manifest)
            write.assert_not_called()
        records.remove(b)
        with patch.object(h,'post') as write:
            h.reconcile_queue(API(),self.f['issue'],self.manifest)
            self.assertEqual(write.call_args.kwargs['method'],'DELETE')

    def test_processor_replay_and_demo_guard_no_write(self):
        c=self.comment();records=[c,self.acknowledged(c)]
        class API:
            def pages(self,endpoint):return records
        with patch.object(h,'post') as write:
            self.assertFalse(h.process(API(),self.f['issue'],c['id'],self.manifest))
            with self.assertRaises(ValueError):h.process(API(),self.f['issue'],c['id'],self.manifest,demo_only=True)
            with self.assertRaises(ValueError):h.process(API(),self.f['issue'],c['id'],self.manifest,expected_body='0'*64)
            write.assert_not_called()

    def test_related_file_and_criteria_change_invalidate_unrelated_docs_do_not(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'apps').mkdir();(root/'apps/code.py').write_text('one')
            (root/'apps/version.json').write_text('{"version":"0.3.0-beta.2"}')
            def git(*args):return subprocess.check_output(['git',*args],cwd=root,stderr=subprocess.DEVNULL)
            git('init');git('config','user.name','QA');git('config','user.email','qa@example.invalid')
            git('add','.');git('commit','-m','initial')
            m={'version_source':'apps/version.json'}
            f={'id':'demo','code_paths':['apps/code.py'],'acceptance':'criterion','review':{'checklist':[{'id':'check','label':'test'}]}}
            old=h.context(root,f,m)['revision'];(root/'README.md').write_text('docs');git('add','.');git('commit','-m','docs')
            self.assertEqual(h.context(root,f,m)['revision'],old)
            (root/'apps/code.py').write_text('two');git('add','.');git('commit','-m','code')
            self.assertNotEqual(h.context(root,f,m)['revision'],old)
            changed=h.context(root,f,m)['revision'];f['acceptance']='new criterion'
            self.assertNotEqual(h.context(root,f,m)['revision'],changed)

    def test_changed_current_fingerprint_requires_review(self):
        c=self.comment();records=[c,self.acknowledged(c)];new={**self.context,'revision':'b'*64}
        with patch.object(h,'context',return_value=new):self.assertEqual(self.project(records)['state'],'needs_review')

    def test_workflow_auth_trusted_main_minimal_permissions_and_refresh(self):
        workflow=(ROOT/'.github/workflows/human-review.yml').read_text()
        for expected in ('issue_comment:','created, edited, deleted','ref: main','issues: write','45896918'):
            self.assertIn(expected,workflow)
        self.assertNotIn('contents: write',workflow);self.assertNotIn('pull_request_target',workflow)
        self.assertNotIn('github.event.comment.body }}',workflow)
        self.assertIn('Validar revisión humana',(ROOT/'.github/workflows/sync-roadmap.yml').read_text())


if __name__=='__main__':unittest.main()
