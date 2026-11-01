"""Synthetic packaging attacks/fixtures, not clean-Windows installation QA."""
import base64
import csv
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from scripts import build_embedded_runtime as bundle
from scripts.audit_embedded_payload import SCANNER


def wheel(path,contents,bad_record=False):
    rows=[]
    for name,raw in contents.items():
        checksum=base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).rstrip(b'=').decode()
        rows.append([name,'sha256='+('bad' if bad_record else checksum),str(len(raw))])
    record='fixture-1.dist-info/RECORD';rows.append([record,'',''])
    out=io.StringIO();csv.writer(out,lineterminator='\n').writerows(rows)
    with zipfile.ZipFile(path,'w') as archive:
        for name,raw in contents.items():archive.writestr(name,raw)
        archive.writestr(record,out.getvalue())


class EmbeddedRuntimeTests(unittest.TestCase):
    def test_public_vendor_ci_prefix_is_not_an_exception_for_own_code(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);profile='C:'+ '/Users/'+'runneradmin';(root/'text.txt').write_text(profile+'/build/input')
            data={'root':directory,'profile':profile,'files':{'text.txt':{'origin':'published-fixture.whl'}}}
            run=lambda:json.loads(subprocess.run([sys.executable,'-c',SCANNER],input=json.dumps(data),capture_output=True,text=True,check=True).stdout)
            self.assertTrue(run()['passed'])
            data['files']['text.txt']['origin']='repository'
            self.assertFalse(run()['passed'])
    def test_checkout_newlines_are_canonicalized_without_changing_binary_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);text=root/'module.py';binary=root/'original.dll'
            text.write_bytes(b'first\r\nsecond\r\n');binary.write_bytes(text.read_bytes())
            self.assertEqual(bundle.repository_bytes(text),b'first\nsecond\n')
            self.assertEqual(bundle.repository_bytes(binary),b'first\r\nsecond\r\n')
    def test_demo_cannot_silently_include_an_extra_private_photo(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);assets=[]
            for role in ('source','reference'):
                raw=b'licensed-fixture-'+role.encode();(root/(role+'.jpg')).write_bytes(raw)
                assets.append({'role':role,'file':role+'.jpg','license':'CC0-1.0','author':'Fixture only','original_url':'https://dl.polyhaven.org/fixture','sha256':bundle.digest(raw)})
            (root/'credits.json').write_text(json.dumps({'assets':assets}))
            self.assertEqual(len(bundle.authorized_demo(root)),3)
            (root/'private-fixture.jpg').write_bytes(b'not approved')
            with self.assertRaisesRegex(ValueError,'Unexpected/private'):bundle.authorized_demo(root)
    def test_privacy_scanner_does_not_confuse_https_or_compressed_bytes_with_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'app.py').write_text("url='https://example.com/reference'\n")
            (root/'font.woff2').write_bytes(b'compressed-fixture A:/bytes')
            inputs={'root':directory,'profile':'','files':{p.name:{'origin':'repository'} for p in root.iterdir()}}
            result=subprocess.run([sys.executable,'-c',SCANNER],input=json.dumps(inputs),capture_output=True,text=True,check=True)
            self.assertTrue(json.loads(result.stdout)['passed'])

    def test_privacy_scanner_blocks_profile_and_secret_without_echoing_them(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);profile='C:'+ '/Users/'+'private-fixture';value=profile+'/photos';token='ghp_'+'x'*40
            (root/'app.txt').write_text(value+'\n'+token)
            result=subprocess.run([sys.executable,'-c',SCANNER],input=json.dumps({'root':directory,'profile':profile,'files':{'app.txt':{'origin':'repository'}}}),capture_output=True,text=True,check=True)
            report=json.loads(result.stdout)
            self.assertFalse(report['passed']);self.assertNotIn(value,result.stdout);self.assertNotIn(token,result.stdout)
            self.assertTrue({'secret_pattern','local_private_profile_path'}<={r['reason'] for r in report['findings']})

    def test_windows_archive_paths_refuse_traversal_devices_and_drives(self):
        for name in ('../x','/x','C:/x','a\\b','NUL.txt','a/COM1.py','x.','x /y','a\x00b'):
            with self.subTest(name=name),self.assertRaises(ValueError):bundle.safe_member(name)
        self.assertEqual(bundle.safe_member('package/submodule.py'),'package/submodule.py')

    def test_wheel_record_hashes_are_checked_before_vendoring(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);archive=root/'fixture.whl';wheel(archive,{'package/code.py':b'pass\n'})
            files={};excluded=[];bundle.extract(archive,{'filename':archive.name},root/'out',files,excluded)
            self.assertEqual((root/'out/vendor/package/code.py').read_bytes(),b'pass\n')
            wheel(archive,{'package/code.py':b'pass\n'},bad_record=True)
            with self.assertRaisesRegex(ValueError,'RECORD'):bundle.extract(archive,{'filename':archive.name},root/'bad',{},[])

    def test_archive_case_collisions_and_symlinks_are_not_overwrites(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);archive=root/'fixture.whl'
            wheel(archive,{'package/A.py':b'first','package/a.py':b'second'})
            with self.assertRaisesRegex(ValueError,'collision'):bundle.extract(archive,{'filename':archive.name},root/'out',{},[])
            self.assertEqual((root/'out/vendor/package/A.py').read_bytes(),b'first')
            with zipfile.ZipFile(archive,'w') as z:
                info=zipfile.ZipInfo('link');info.external_attr=0o120777<<16;z.writestr(info,'outside')
            with self.assertRaisesRegex(ValueError,'symlink'):bundle.extract(archive,{'filename':archive.name},root/'links',{},[],True)

    def test_locked_cache_tampering_or_untrusted_download_fails_without_network(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'fixture.zip').write_bytes(b'changed')
            item={'filename':'fixture.zip','url':'https://www.python.org/fixture.zip','sha256':'0'*64}
            with patch.object(bundle.urllib.request,'urlopen',side_effect=AssertionError('No network')):
                with self.assertRaisesRegex(ValueError,'hash'):bundle.locked_download(item,root,True)
                item['filename']='missing.zip'
                with self.assertRaisesRegex(ValueError,'Missing'):bundle.locked_download(item,root,True)
                item['url']='https://untrusted.example/fixture.zip'
                with self.assertRaisesRegex(ValueError,'origin'):bundle.locked_download(item,root,False)

    def test_licenses_survive_pruning_and_video_test_development_files_do_not(self):
        self.assertIsNone(bundle.excluded('package.dist-info/licenses/tests/LICENSE.txt'))
        for name in ('numpy/tests/test.py','cv2/opencv_videoio_ffmpeg500_64.dll','numpy/_core/a_tests.cp314.pyd','include/headers.h'):
            with self.subTest(name=name):self.assertIsNotNone(bundle.excluded(name))
        self.assertIsNone(bundle.excluded('numpy/_core/_multiarray_umath.cp314-win_amd64.pyd'))

    def test_bundle_tampering_or_extra_manifest_named_file_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'a.py').write_bytes(b'pass')
            report={'files':{'a.py':{'sha256':bundle.digest(b'pass')}}}
            (root/bundle.MANIFEST).write_text(json.dumps(report))
            bundle.verify_bundle(root)
            (root/'nested').mkdir();(root/'nested'/bundle.MANIFEST).write_text('{}')
            with self.assertRaisesRegex(ValueError,'unexpected'):bundle.verify_bundle(root)
            (root/'nested'/bundle.MANIFEST).unlink();(root/'a.py').write_bytes(b'evil')
            with self.assertRaisesRegex(ValueError,'hash'):bundle.verify_bundle(root)

    def test_unknown_origin_even_with_forged_matching_manifest_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);target=root/'target';target.mkdir();cache=root/'cache';cache.mkdir()
            archive=cache/'python.zip'
            with zipfile.ZipFile(archive,'w') as z:z.writestr('LICENSE.txt','fixture only')
            python={'filename':'python.zip','url':'https://www.python.org/python.zip','sha256':bundle.digest(archive.read_bytes())}
            lock={'python':python,'packages':[]};lock_path=root/'lock.json';lock_path.write_text(json.dumps(lock))
            (target/'evil.dll').write_bytes(b'fixture')
            report={'lock_sha256':bundle.digest(lock_path.read_bytes()),'inputs':[python],
                    'files':{'evil.dll':{'sha256':bundle.digest(b'fixture'),'origin':'host-System32','member':'evil.dll'}}}
            (target/bundle.MANIFEST).write_text(json.dumps(report))
            with patch.object(bundle,'LOCK',lock_path),self.assertRaisesRegex(ValueError,'origin'):bundle.verify_sources(target,cache)
