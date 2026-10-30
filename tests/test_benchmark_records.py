import copy
import datetime
import hashlib
import importlib.util
import json
import pathlib
import unittest
from contextlib import redirect_stdout
from io import StringIO

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('benchmark', ROOT/'scripts/validate_benchmark.py')
benchmark = importlib.util.module_from_spec(spec)
spec.loader.exec_module(benchmark)
TODAY = datetime.date(2026,10,30)


def sha(value):
    return hashlib.sha256(value.encode()).hexdigest()


def fixture():
    # Bookkeeping fixtures, never competitor results or files.
    data = json.loads((ROOT/'data/p0/benchmark.json').read_text('utf-8'))
    data['dataset_sha256'] = sha('unit-test-manifest')
    for product in data['products']:
        for pair in data['pair_ids']:
            data['runs'].append({'product_id':product['id'],'pair_id':pair,
                'mode':'automatic','state':'complete','tool_version':'unit-test-only',
                'source_sha256':sha(pair+'source'),'reference_sha256':sha(pair+'reference'),
                'output_sha256':sha(pair+product['id']+'output'),
                'capture_sha256':sha(pair+product['id']+'capture'),
                'elapsed_seconds':1,'timing_method':'stopwatch','recorded_on':'2026-10-29',
                'settings_record_id':'SETTINGS-TEST','color_record_id':'COLOR-TEST',
                'review_record_id':'REVIEW-TEST'})
    return data


class BenchmarkTests(unittest.TestCase):
    def test_plan_is_valid_not_executed(self):
        data = json.loads((ROOT/'data/p0/benchmark.json').read_text('utf-8'))
        result = benchmark.validate(data, TODAY)
        self.assertTrue(result['schema_valid'])
        self.assertEqual(result['completed_automatic'],0)
        self.assertFalse(result['bookkeeping_ready'])
        self.assertFalse(result['research_validated'])

    def test_full_bookkeeping_fixture_does_not_approve_research(self):
        result = benchmark.validate(fixture(), TODAY)
        self.assertTrue(result['bookkeeping_ready'])
        self.assertEqual(result['complete_products'],5)
        self.assertFalse(result['research_validated'])

    def test_duplicate_pair_product_cannot_inflate_results(self):
        data = fixture()
        data['runs'][-1] = copy.deepcopy(data['runs'][0])
        self.assertFalse(benchmark.validate(data,TODAY)['bookkeeping_ready'])

    def test_inputs_are_identical_across_tools(self):
        data = fixture()
        data['runs'][20]['source_sha256'] = sha('wrong-input')
        self.assertFalse(benchmark.validate(data,TODAY)['schema_valid'])

    def test_blocked_is_not_quality_failure_or_measured_zero(self):
        data = fixture()
        data['runs'][0] = {'product_id':'luttie','pair_id':'P0-001','mode':'automatic',
                          'state':'blocked','reason_code':'privacy'}
        result = benchmark.validate(data,TODAY)
        self.assertTrue(result['schema_valid'])
        self.assertEqual(result['blocked_runs'],1)
        self.assertEqual(result['completed_automatic'],99)
        data['runs'][0]['elapsed_seconds'] = 0
        self.assertFalse(benchmark.validate(data,TODAY)['schema_valid'])

    def test_nonfinite_boolean_huge_or_missing_timing_rejected(self):
        for value in (True, float('nan'), -1, None, 10**1000):
            data = fixture()
            data['runs'][0]['elapsed_seconds'] = value
            self.assertFalse(benchmark.validate(data,TODAY)['schema_valid'])

    def test_versions_evidence_and_dates_required(self):
        for field,value in [('tool_version',''),('capture_sha256',None),
                            ('color_record_id',''),('recorded_on','2099-01-01')]:
            data = fixture()
            data['runs'][0][field] = value
            self.assertFalse(benchmark.validate(data,TODAY)['schema_valid'])

    def test_refined_passes_do_not_replace_automatic_baseline(self):
        data = fixture()
        for run in data['runs']:
            run['mode'] = 'refined'
        result = benchmark.validate(data,TODAY)
        self.assertEqual(result['refined_runs'],100)
        self.assertEqual(result['completed_automatic'],0)
        self.assertFalse(result['bookkeeping_ready'])

    def test_ready_cli_on_empty_registry_and_malformed_manifest(self):
        with redirect_stdout(StringIO()):
            self.assertEqual(benchmark.main([]),0)
            self.assertEqual(benchmark.main(['--ready']),2)
        for data in ([], {'version':True}, {'version':1,'products':[]}):
            self.assertFalse(benchmark.validate(data,TODAY)['schema_valid'])
