"""Hostile download/cache fixtures; no network or Microsoft installer execution."""
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.request
from scripts.prepare_installer_inputs import fetch,HttpsRedirects


class InstallerInputTests(unittest.TestCase):
    def test_insecure_redirect_is_rejected_before_the_next_request(self):
        request=urllib.request.Request('https://official.example/file')
        with self.assertRaisesRegex(ValueError,'HTTPS'):
            HttpsRedirects().redirect_request(request,None,302,'Found',{},'http://official.example/file')
        result=HttpsRedirects().redirect_request(request,None,302,'Found',{},'https://cdn.example/file')
        self.assertEqual(result.full_url,'https://cdn.example/file')

    def test_missing_offline_or_changed_cache_never_downloads(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'fixture.exe'
            item={'url':'https://official.example/file','sha256':hashlib.sha256(b'fixture').hexdigest()}
            with patch('urllib.request.build_opener',side_effect=AssertionError('Network must not be used')):
                with self.assertRaisesRegex(ValueError,'offline'):fetch(item,path,True)
                path.write_bytes(b'tampered')
                with self.assertRaisesRegex(ValueError,'Changed'):fetch(item,path,True)
                path.write_bytes(b'fixture');self.assertEqual(fetch(item,path,True),path)
                with self.assertRaisesRegex(ValueError,'HTTPS'):fetch({**item,'url':'http://official.example/file'},path)


if __name__=='__main__':unittest.main()
