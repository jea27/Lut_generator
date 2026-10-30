import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from scripts.prepare_research_site import prepare, PUBLIC_FILES

ROOT = Path(__file__).resolve().parents[1]


class ResearchSiteTests(unittest.TestCase):
    def test_packages_only_allowlist_and_keeps_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); source = root / 'research'; source.mkdir()
            for name in PUBLIC_FILES:
                (source / name).write_text(name, encoding='utf-8')
            (source / 'private.json').write_text('private', encoding='utf-8')
            target = prepare(root)
            self.assertEqual({p.name for p in target.iterdir()}, {'index.html', 'form.js', 'form.css'})
            self.assertEqual((target / 'index.html').read_text(), 'form.html')
            self.assertTrue((source / 'private.json').exists())
            prepare(root)  # safe repeated packaging, no stale data included

    def test_unexpected_public_file_fails_without_upload_or_deletion(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / 'research').mkdir()
            for name in PUBLIC_FILES:
                (root / 'research' / name).write_text(name, encoding='utf-8')
            target = root / 'site/investigacion'; target.mkdir(parents=True)
            leaked = target / 'response.json'; leaked.write_text('private', encoding='utf-8')
            with self.assertRaises(ValueError):
                prepare(root)
            self.assertEqual(leaked.read_text(), 'private')
            self.assertFalse((target / 'index.html').exists())

    def test_both_deploy_paths_package_instrument(self):
        for name in ('publish-roadmap.yml', 'sync-roadmap.yml'):
            workflow = (ROOT / '.github/workflows' / name).read_text(encoding='utf-8')
            self.assertIn('python scripts/prepare_research_site.py', workflow)

    def test_codes_are_three_unique_unassigned_reservations(self):
        registry = json.loads((ROOT / 'data/p0/participant_codes.json').read_text(encoding='utf-8'))
        self.assertEqual([c['code'] for c in registry['codes']], ['R101', 'R102', 'R103'])
        self.assertTrue(all(c['state'] == 'reserved_not_distributed' for c in registry['codes']))
        self.assertEqual(registry['responses_received'], 0)
        self.assertTrue(all(set(c) == {'code', 'state'} for c in registry['codes']))

    @unittest.skipUnless(shutil.which('node'), 'Node unavailable')
    def test_share_cancel_failure_and_fragment_privacy(self):
        source = r"""
const assert = require('node:assert/strict');
const {participantCodeFromHash, canShareFile, shareResponse} = require('./research/form.js');
async function test() {
  assert.equal(participantCodeFromHash('#R101'), 'R101');
  for (const hash of ['#R000', '?code=R101', '#email@example.com', '#R101/../', '#<script>'])
    assert.equal(participantCodeFromHash(hash), '');
  assert.equal(canShareFile({}, {}), false);
  const file = {};
  assert.equal(await shareResponse({}, file), 'unavailable');
  const success = {canShare: () => true, share: async ({files}) => assert.equal(files[0], file)};
  assert.equal(await shareResponse(success, file), 'handed_to_share_ui');
  assert.equal(await shareResponse({...success, share: async () => {throw {name:'AbortError'}}}, file), 'cancelled');
  assert.equal(await shareResponse({...success, share: async () => {throw {name:'NotAllowedError'}}}, file), 'failed');
  assert.equal(canShareFile({canShare:()=>{throw Error('unsupported')}, share:()=>{}}, file), false);
}
test().catch(e=>{console.error(e);process.exitCode=1});
"""
        subprocess.run(['node', '-e', source], cwd=ROOT, check=True, capture_output=True)
