import copy
import datetime
import importlib.util
import json
import pathlib
import unittest
from contextlib import redirect_stdout
from io import StringIO

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('interviews', ROOT/'scripts/validate_interviews.py')
interviews = importlib.util.module_from_spec(spec)
spec.loader.exec_module(interviews)
TODAY = datetime.date(2026, 10, 30)


def fixture():
    # Synthetic inputs only; never written into the research registry.
    return {'version': 1, 'interviews': [
        {'id': f'E{i:02}', 'segment': 'A' if i <= 4 else 'B' if i <= 8 else 'C',
         'date': '2026-10-29', 'status': 'complete', 'notes_consent': True,
         'anonymized': True, 'redaction_record_id': f'REDACT-E{i:02}',
         'frequency_30d': 0, 'current_solution': 'unit-test-only',
         'problem_summary': 'unit-test-only', 'pay_intent': 'declined',
         'evidence_type': 'interview_notes'} for i in range(1, 13)]}


class InterviewTests(unittest.TestCase):
    def test_empty_registry_does_not_invent_evidence(self):
        report = interviews.validate({'version': 1, 'interviews': []}, TODAY)
        self.assertTrue(report['schema_valid'])
        self.assertEqual(report['completed_sessions'], 0)
        self.assertFalse(report['gate_ready'])

    def test_complete_bookkeeping_fixture(self):
        result = interviews.validate(fixture(), TODAY)
        self.assertTrue(result['gate_ready'])
        self.assertEqual(result['segments'], {'A':4, 'B':4, 'C':4, 'D':0})

    def test_duplicate_participants_not_counted_twice(self):
        data = fixture()
        data['interviews'][1] = copy.deepcopy(data['interviews'][0])
        self.assertFalse(interviews.validate(data, TODAY)['gate_ready'])

    def test_no_consent_or_redaction_means_no_ready(self):
        for field, value in [('notes_consent', False), ('anonymized', False), ('redaction_record_id', '')]:
            data = fixture()
            data['interviews'][0][field] = value
            self.assertFalse(interviews.validate(data, TODAY)['gate_ready'])

    def test_future_dates_and_boolean_frequencies_rejected(self):
        for field, value in [('date','2099-01-01'), ('frequency_30d',True), ('segment','AB')]:
            data = fixture()
            data['interviews'][0][field] = value
            self.assertFalse(interviews.validate(data, TODAY)['schema_valid'])

    def test_declined_or_unknown_are_not_changed_into_yes_or_zero(self):
        data = fixture()
        data['interviews'][0]['frequency_30d'] = None
        data['interviews'][0]['pay_intent'] = 'unknown'
        result = interviews.validate(data, TODAY)
        self.assertTrue(result['gate_ready'])
        self.assertEqual(result['missing_answers'], 13)
        self.assertIsNone(data['interviews'][0]['frequency_30d'])

    def test_contacts_rejected_and_values_never_echoed(self):
        data = fixture()
        data['interviews'][0]['email'] = 'private-contact-placeholder'
        result = interviews.validate(data, TODAY)
        self.assertFalse(result['schema_valid'])
        self.assertNotIn('private-contact-placeholder', json.dumps(result))

    def test_quota_not_met_and_drafts_not_counted(self):
        data = fixture()
        data['interviews'][0]['status'] = 'draft'
        result = interviews.validate(data, TODAY)
        self.assertEqual(result['completed_sessions'], 11)
        self.assertFalse(result['gate_ready'])

    def test_cli_reports_not_ready_for_empty_real_registry(self):
        with redirect_stdout(StringIO()):
            self.assertEqual(interviews.main([]), 0)
            self.assertEqual(interviews.main(['--ready', '--as-of','2026-10-30']), 2)

    def test_malformed_registry_rejected(self):
        for value in ([], {'version':True,'interviews':[]}, {'version':1,'interviews':[None]}):
            self.assertFalse(interviews.validate(value, TODAY)['schema_valid'])
