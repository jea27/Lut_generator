import unittest
from scripts.check_advisories import check,packages


class AdvisoryTests(unittest.TestCase):
    def test_pinned_package_scope_contains_all_ecosystems_and_no_paths(self):
        queries=packages()
        self.assertEqual({q['package']['ecosystem'] for q in queries},{'PyPI','npm','crates.io'})
        self.assertGreater(len(queries),100)
        self.assertTrue(all(set(q)=={'package','version'} for q in queries))

    def test_pagination_is_merged_without_duplicate_findings(self):
        q={'package':{'ecosystem':'PyPI','name':'test'},'version':'1.0'}
        calls=[]
        def fetch(queries):
            calls.append(queries)
            return {'results':[{'vulns':[{'id':'GHSA-test'}],**({'next_page_token':'next'} if len(calls)==1 else {})}]}
        report=check([q],fetch)
        self.assertEqual(len(calls),2)
        self.assertEqual(report[0]['advisories'],['GHSA-test'])
        self.assertEqual(calls[1][0]['page_token'],'next')
        self.assertNotIn('page_token',q)

    def test_missing_response_never_means_no_vulnerabilities(self):
        with self.assertRaises(ValueError):check([{'package':{},'version':'1'}],lambda q:{'results':[]})
        with self.assertRaises(OSError):check([{'package':{},'version':'1'}],lambda q:(_ for _ in ()).throw(OSError()))

    def test_truncated_pagination_never_produces_clear_report(self):
        with self.assertRaises(ValueError):
            check([{'package':{},'version':'1'}],lambda q:{'results':[{'next_page_token':'same'}]})
