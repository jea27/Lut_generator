import importlib.util
import pathlib
import unittest
import contextlib
import io
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('import_issues', ROOT / 'scripts' / 'import_issues.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class ImportIssueTests(unittest.TestCase):
    def test_existing_ids_deduplicates(self):
        self.assertEqual(mod.existing_ids(['[COL-001] Uno','[COL-001] duplicado','otro [COL-010]']), {'COL-001','COL-010'})
    def test_issue_body_has_acceptance(self):
        task = {'id':'COL-123','title':'Test','phase':'P0','priority':'Media','executor':'humano','acceptance':'Prueba demostrable'}
        self.assertEqual(mod.issue_title(task), '[COL-123] Test')
        self.assertIn('Prueba demostrable', mod.issue_body(task))
    def test_dry_run_never_uses_gh(self):
        output = io.StringIO()
        with patch('sys.argv', ['import_issues.py']), patch.object(mod.subprocess, 'run') as run:
            with contextlib.redirect_stdout(output):
                mod.main()
        run.assert_not_called()
        self.assertIn('DRY RUN: 42', output.getvalue())
        self.assertIn('[COL-042]', output.getvalue())

if __name__ == '__main__':
    unittest.main()
