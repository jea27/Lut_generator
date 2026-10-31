import copy
from io import BytesIO
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import urllib.error
from unittest.mock import patch

from scripts import sync_product as product

ROOT=Path(__file__).resolve().parents[1]
REPO='jea27/Lut_generator'
BASE='https://github.com/'+REPO


class ProductTests(unittest.TestCase):
    def setUp(self):
        self.manifest=json.loads((ROOT/'site/data/product-manifest.json').read_bytes())
        numbers={f['issue'] for f in self.manifest['features']}|{19,60,61,62,67}
        self.issues=[{'id':n,'number':n,'state':'open','labels':[], 'title':'Test', 'html_url':f'{BASE}/issues/{n}'} for n in numbers]
        numbers={n for f in self.manifest['features'] for n in f['delivery_prs']}
        self.prs=[{'id':n,'number':n,'state':'closed','title':'[COL-026] Entrega', 'merged_at':'2026-10-31T00:00:00Z',
                   'base':{'ref':'main'},'updated_at':'2026-10-31T00:00:00Z','html_url':f'{BASE}/pull/{n}'} for n in numbers]
        self.runs=[{'id':n,'name':name,'status':'completed','conclusion':'success','head_sha':'a'*40,'head_branch':'main','run_number':3,'html_url':f'{BASE}/actions/runs/{n}'} for n,name in enumerate(self.manifest['required_ci'])]
        self.releases=[]

    def derive(self):
        return product.derive(self.manifest,ROOT,REPO,self.issues,self.prs,self.runs,'a'*40,self.releases,[],'2026-10-31T00:00:00Z')

    def issue(self,n): return next(i for i in self.issues if i['number']==n)

    def test_idempotence_defined_denominators_and_no_double_counting(self):
        a=self.derive(); self.assertEqual(a,self.derive())
        self.assertEqual(a['metrics']['technical']['total'],8)
        self.assertEqual(a['metrics']['technical']['passed'],8)
        self.assertEqual(a['metrics']['human']['passed'],0)
        self.assertFalse(a['readiness']['beta']['go'])
        self.assertFalse(a['readiness']['commercial']['go'])
        self.assertEqual(len(a['features']),15)

    def test_merge_and_ci_are_not_human_approval_and_blocked_overrides(self):
        i=self.issue(43); i.update(state='closed',labels=[{'name':'approved'}])
        self.assertEqual(self.derive()['metrics']['human']['passed'],1)
        i['labels'].append({'name':'blocked'})
        f=next(f for f in self.derive()['features'] if f['id']=='color-match')
        self.assertTrue(f['implemented']); self.assertTrue(f['technically_verified'])
        self.assertFalse(f['human_approved']); self.assertEqual(f['status'],'blocked')

    def test_new_draft_changes_work_status_without_erasing_implemented_baseline(self):
        self.prs.append({'id':999,'number':999,'state':'open','draft':True,'title':'[COL-011] Ajuste nuevo',
                         'base':{'ref':'main'},'updated_at':'2027-01-01','html_url':BASE+'/pull/999'})
        f=next(f for f in self.derive()['features'] if f['id']=='color-match')
        self.assertTrue(f['implemented']);self.assertEqual(f['status'],'progress');self.assertEqual(f['pr_url'],BASE+'/pull/999')

    def test_future_not_approved_from_shared_issue(self):
        self.issue(68).update(state='closed',labels=[{'name':'approved'}])
        for f in self.derive()['features']:
            if f['group']=='Futuro':
                self.assertFalse(f['implemented']);self.assertFalse(f['human_approved']);self.assertEqual(f['status'],'planned')

    def test_missing_ci_and_wrong_head_cannot_verify(self):
        self.runs[0]['head_sha']='b'*40
        self.assertIsNone(self.derive()['metrics']['technical']['percent'])
        self.assertIsNone(self.derive()['metrics']['technical']['passed'])
        self.runs[0]['head_sha']='a'*40;self.runs[0]['conclusion']='failure'
        self.assertEqual(self.derive()['metrics']['technical']['passed'],0)

    def test_absent_evidence_is_unknown_and_stacked_merge_insufficient(self):
        self.manifest['features'][0]['evidence']=[{'path':'docs/evidence/absent.json','field':'passed','equals':True}]
        self.assertIsNone(self.derive()['metrics']['technical']['percent'])
        self.assertEqual(self.derive()['metrics']['technical']['unknown'],1)
        for p in self.prs:p['base']['ref']='codex/intermediate'
        self.assertFalse(any(f['implemented'] for f in self.derive()['features']))

    def test_release_requires_explicit_tag_approval_and_never_auto_approves_features(self):
        self.releases=[{'tag_name':'v0.3.0-beta.2','draft':False,'published_at':'2026-10-31T00:00:00Z','html_url':BASE+'/releases/tag/v0.3.0-beta.2'}]
        self.assertIsNone(self.derive()['latest_release']['download_url'])
        self.issue(62)['labels']=[{'name':'release-approved:v0.3.0-beta.2'}]
        self.assertTrue(self.derive()['latest_release']['authorized'])
        self.assertIsNone(self.derive()['latest_release']['download_url'])
        candidate=self.derive()['candidate']
        self.releases[0]['assets']=[{'state':'uploaded','name':'installer.exe','digest':'sha256:'+candidate['sha256']}]
        self.assertIsNotNone(self.derive()['latest_release']['download_url'])
        self.assertEqual(self.derive()['metrics']['human']['passed'],0)

    def test_public_projection_drops_bodies_emails_tokens_and_paths(self):
        i=self.issue(67);i.update(title=r'C:\Users\private-person\file',body='github_pat_secret-value',labels=[{'name':'needs-human'}])
        self.prs[0].update(title='owner@example.com',body='private interview',html_url='file:///C:/Users/private-person/photo.png')
        raw=json.dumps(self.derive())
        for forbidden in ('private-person','github_pat_secret','owner@example.com','private interview','file:///'):self.assertNotIn(forbidden,raw)
        self.assertEqual(product.link(BASE+'/issues/67',REPO),BASE+'/issues/67')
        self.assertIsNone(product.link('https://evil.test/'+REPO+'/issues/67',REPO))
        with self.assertRaises(ValueError):product.path(ROOT,'docs/evidence/../../../private.json')

    def test_schema_duplicate_metrics_and_missing_data(self):
        self.assertIsNone(product.metric([])['percent'])
        self.assertIsNone(product.metric([None,None])['passed'])
        self.assertEqual(product.metric([True,False,None])['percent'],None)
        self.manifest['features'].append(copy.deepcopy(self.manifest['features'][0]))
        with self.assertRaises(ValueError):self.derive()

    def test_api_pagination_deduplicates_and_fails_on_incomplete_schema(self):
        api=product.GitHub(REPO,'not-a-real-token')
        with patch.object(api,'get',side_effect=[[{'id':n} for n in range(100)],[{'id':0}]]):
            self.assertEqual(len(api.pages('/issues')),100)
        with patch.object(api,'get',return_value={'private':'data'}):
            with self.assertRaises(ValueError):api.pages('/issues')

    def test_api_error_preserves_previous_output_and_private_repo_refused(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); (root/'site/data').mkdir(parents=True)
            out=root/'site/data/product.json';out.write_text('previous complete snapshot')
            with patch.object(product,'ROOT',root),patch.dict(product.os.environ,{'GITHUB_REPOSITORY':REPO}),patch.object(product.GitHub,'get',side_effect=urllib.error.URLError('outage')):
                with self.assertRaises(urllib.error.URLError):product.main()
            self.assertEqual(out.read_text(),'previous complete snapshot')
            with patch.dict(product.os.environ,{'GITHUB_REPOSITORY':REPO}),patch.object(product.GitHub,'get',return_value={'private':True}):
                with self.assertRaises(ValueError):product.main()

    def test_retries_only_bounded_transient_failures(self):
        api=product.GitHub(REPO,'not-a-real-token')
        error=urllib.error.HTTPError('https://api.github.com',503,'Unavailable',{},None)
        with patch.object(product.urllib.request,'urlopen',side_effect=[error,BytesIO(b'{}')]) as call,patch.object(product.time,'sleep'):
            self.assertEqual(api.get(''),{});self.assertEqual(call.call_count,2)

    def test_public_metadata_fallback_drops_auth_without_expanding_permissions(self):
        api=product.GitHub(REPO,'not-a-real-token');api.public=True
        error=urllib.error.HTTPError('https://api.github.com',403,'Forbidden',{},None)
        with patch.object(product.urllib.request,'urlopen',side_effect=[error,BytesIO(b'{}')]) as call:
            self.assertEqual(api.get('/actions/runs'),{})
            self.assertNotIn('Authorization',call.call_args.args[0].headers)

    def test_workflow_uses_trusted_main_without_artifact_execution(self):
        workflow=(ROOT/'.github/workflows/sync-roadmap.yml').read_text()
        for trigger in ('pull_request_target:','release:','workflow_run:','Compilar candidato beta Windows','schedule:'):self.assertIn(trigger,workflow)
        self.assertIn('ref: main',workflow)
        self.assertIn("github.event_name == 'release'",workflow)
        self.assertNotIn('head.sha',workflow)
        self.assertNotIn('download-artifact',workflow)
        self.assertNotIn('contents: write',workflow)
        self.assertEqual(len(json.loads((ROOT/'site/data/roadmap.json').read_bytes())['tasks']),42)

    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_render_escapes_html_and_disables_unapproved_downloads(self):
        d=self.derive();d['features'][0]['title']='<img src=x onerror=alert(1)>'
        d['features'][0]['issue_url']='javascript:alert(1)'
        js='global.window={INITIAL_PRODUCT:'+json.dumps(d)+'};global.document={querySelectorAll:()=>[]};global.location={protocol:"file:"};'+(ROOT/'site/product.js').read_text()+';process.stdout.write(window.LumaForgeProduct.render());'
        rendered=subprocess.check_output(['node','-e',js],encoding='utf-8')
        self.assertIn('&lt;img',rendered);self.assertNotIn('<img src=x',rendered)
        self.assertNotIn('href="javascript:',rendered);self.assertNotIn('Descarga autorizada',rendered)
        self.assertIn('Ninguna release publicada',rendered)

    @unittest.skipUnless(shutil.which('node'),'Node unavailable')
    def test_render_missing_data_and_refresh_failure_keep_last_snapshot(self):
        source=(ROOT/'site/product.js').read_text()
        js='global.window={};global.document={querySelectorAll:()=>[]};global.location={protocol:"https:"};global.fetch=async()=>({ok:true,json:async()=>({schema_version:1,features:[],metrics:{}})});'+source+';window.LumaForgeProduct.refresh(()=>process.stdout.write(window.LumaForgeProduct.render()));'
        self.assertIn('Sin datos',subprocess.check_output(['node','-e',js],encoding='utf-8'))
        js='global.window={INITIAL_PRODUCT:'+json.dumps(self.derive())+'};global.document={querySelectorAll:()=>[]};global.location={protocol:"https:"};global.fetch=async()=>{throw Error("offline")};'+source+';window.LumaForgeProduct.refresh(()=>process.stdout.write(window.LumaForgeProduct.render()));'
        result=subprocess.check_output(['node','-e',js],encoding='utf-8')
        self.assertIn('Color Match',result);self.assertIn('Snapshot anterior',result)


if __name__=='__main__':unittest.main()
