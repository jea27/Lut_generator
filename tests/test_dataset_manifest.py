import copy
import hashlib
import importlib.util
import json
import pathlib
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('dataset', ROOT/'scripts/validate_dataset.py')
dataset = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dataset)


class DatasetTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads((ROOT/'data/p0/dataset.json').read_text('utf-8'))

    def fixture(self, root):
        data = copy.deepcopy(self.plan)
        data['coverage_review'] = {'status': 'reviewed', 'record_id': 'REVIEW-TEST'}
        for pair in data['pairs']:
            pair['state'] = 'ready'
            for role in ('source', 'reference'):
                # Integrity-only byte fixtures, not an image quality experiment.
                content = b'\x89PNG\r\n\x1a\n' + (pair['id']+role).encode()
                path = f"{pair['id']}/{role}.png"
                file = root/path
                file.parent.mkdir(exist_ok=True)
                file.write_bytes(content)
                pair[role] = {'path': path, 'sha256': hashlib.sha256(content).hexdigest(),
                    'rights': {'status': 'cleared', 'record_id': 'RIGHTS-TEST', 'basis': 'unit-test-only'},
                    'color_space': 'sRGB', 'color_record_id': 'COLOR-TEST'}
        return data

    def test_plan_is_valid_but_not_evidence(self):
        result = dataset.validate(self.plan)
        self.assertTrue(result['schema_valid'])
        self.assertEqual(result['verified_assets'], 0)
        self.assertEqual(result['ready_pairs'], 0)
        self.assertFalse(result['gate_ready'])

    def test_complete_integrity_fixture_and_tampering(self):
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            data = self.fixture(root)
            self.assertTrue(dataset.validate(data, root)['gate_ready'])
            (root/'P0-001/source.png').write_bytes(b'changed')
            self.assertFalse(dataset.validate(data, root)['schema_valid'])

    def test_rights_and_coverage_required_even_when_files_exist(self):
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            data = self.fixture(root)
            data['pairs'][0]['source']['rights']['status'] = 'pending'
            result = dataset.validate(data, root)
            self.assertTrue(result['schema_valid'])
            self.assertFalse(result['gate_ready'])
            self.assertEqual(result['ready_pairs'], 19)

    def test_no_path_escape_or_identifying_filename(self):
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            data = self.fixture(root)
            for path in ('../outside.png', 'C:/private/source.png', 'P0-001/person-name.png'):
                with self.subTest(path=path):
                    data['pairs'][0]['source']['path'] = path
                    self.assertFalse(dataset.validate(data, root)['schema_valid'])

    def test_no_duplicate_sources_or_identical_pair(self):
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            data = self.fixture(root)
            data['pairs'][1]['source']['sha256'] = data['pairs'][0]['source']['sha256']
            self.assertFalse(dataset.validate(data)['schema_valid'])
            data = self.fixture(root)
            data['pairs'][0]['reference']['sha256'] = data['pairs'][0]['source']['sha256']
            self.assertFalse(dataset.validate(data)['schema_valid'])

    def test_cannot_declare_ready_without_local_file_checks(self):
        with tempfile.TemporaryDirectory() as folder:
            data = self.fixture(pathlib.Path(folder))
            self.assertFalse(dataset.validate(data)['gate_ready'])

    def test_rights_basis_requires_a_real_text_reference(self):
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            data = self.fixture(root)
            for value in (True, [], {}, '   '):
                data['pairs'][0]['source']['rights']['basis'] = value
                self.assertFalse(dataset.validate(data,root)['gate_ready'])

    def test_malformed_manifest_fails_closed(self):
        for change in ({'pairs': []}, {'version': True}, {'pairs': [None]*20}):
            with self.subTest(change=change):
                self.assertFalse(dataset.validate({**self.plan, **change})['schema_valid'])
        data = copy.deepcopy(self.plan)
        data['pairs'][0]['id'] = []
        self.assertFalse(dataset.validate(data)['schema_valid'])

    def test_readiness_cli_is_nonzero_on_empty_plan(self):
        with redirect_stdout(StringIO()):
            self.assertEqual(dataset.main([]), 0)
            self.assertEqual(dataset.main(['--ready']), 2)

    def test_invalid_json_cli_does_not_echo_private_content(self):
        with tempfile.TemporaryDirectory() as folder:
            path = pathlib.Path(folder)/'manifest.json'
            path.write_text('private malformed text', 'utf-8')
            output = StringIO()
            with redirect_stdout(output):
                self.assertEqual(dataset.main([str(path)]), 1)
            self.assertNotIn('private malformed text', output.getvalue())
