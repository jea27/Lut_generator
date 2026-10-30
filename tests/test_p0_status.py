import importlib.util
import pathlib
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('p0_status',ROOT/'scripts/p0_status.py')
p0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p0)


def complete_reports():
    return {'interviews':{'schema_valid':True,'gate_ready':True,'completed_sessions':12},
            'dataset':{'schema_valid':True,'gate_ready':True,'ready_pairs':20},
            'benchmark':{'schema_valid':True,'bookkeeping_ready':True,'completed_automatic':100}}


def approved_issues():
    return [{'title':f'[{tid}] fixture','state':'CLOSED',
             'labels':[{'name':'roadmap'},{'name':'approved'}]} for tid in p0.TASKS]


class P0StatusTests(unittest.TestCase):
    def test_merged_documentation_does_not_infer_acceptance(self):
        issues = approved_issues()
        issues[4]['state'] = 'OPEN'
        issues[4]['labels'] = [{'name':'roadmap'},{'name':'status:review'}]
        result = p0.approvals_from_issues(issues)
        self.assertIn('COL-005',result['pending'])
        self.assertFalse(result['all_accepted'])

    def test_duplicates_and_notification_issues_cannot_approve_tasks(self):
        issues = approved_issues()
        issues.append(issues[0].copy())
        issues.append({'title':'[COL-005] Review fixture','state':'CLOSED','labels':[{'name':'approved'}]})
        result = p0.approvals_from_issues(issues)
        self.assertEqual(result['duplicate_ids'],['COL-001'])
        self.assertNotIn('COL-001',result['accepted'])

    def test_no_approval_inferred_when_github_not_read(self):
        result = p0.summarize(complete_reports())
        self.assertTrue(result['technical_evidence_ready'])
        self.assertFalse(result['p0_records_and_acceptance_complete'])

    def test_even_complete_records_never_authorize_p1(self):
        result = p0.summarize(complete_reports(),p0.approvals_from_issues(approved_issues()))
        self.assertTrue(result['p0_records_and_acceptance_complete'])
        self.assertFalse(result['automatic_p1_authorization'])

    def test_missing_validator_or_evidence_fails_closed(self):
        reports = complete_reports()
        reports['dataset'] = {'schema_valid':False,'errors':['missing']}
        result = p0.summarize(reports)
        self.assertFalse(result['technical_evidence_ready'])
        self.assertEqual(result['errors'],{'dataset':['missing']})

    def test_api_failure_cannot_fabricate_approval(self):
        with patch.object(p0.subprocess,'run',side_effect=OSError('private error not logged')):
            self.assertFalse(p0.github_approvals('gh')['available'])

    def test_ready_cli_reports_incomplete_without_changing_files(self):
        reports = complete_reports()
        reports['interviews']['gate_ready'] = False
        with patch.object(p0,'load_reports',return_value=reports), redirect_stdout(StringIO()):
            self.assertEqual(p0.main(['--ready']),2)

    def test_github_command_is_read_only(self):
        with patch.object(p0.subprocess,'run') as run:
            run.return_value.stdout = '[]'
            p0.github_approvals('gh')
        args = run.call_args.args[0]
        self.assertEqual(args[:3],['gh','issue','list'])
        self.assertNotIn('edit',args)
        self.assertNotIn('create',args)
