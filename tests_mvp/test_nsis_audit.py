"""Synthetic hostile archive listings; not evidence of a clean Windows install."""
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch
from scripts import audit_nsis_payload as audit
from scripts.audit_nsis_payload import listing, expected_files, launcher_match


def archive(*rows):
    return 'Type = Nsis\n\n----------\n'+'\n\n'.join(rows)


class NsisAuditTests(unittest.TestCase):
    def test_offline_nsis_cache_is_hash_checked_without_fallback_network(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'packaging').mkdir();cache=root/'.lumaforge-local/downloads';cache.mkdir(parents=True)
            record={'version':'3.13','filename':'nsis-3.13.zip','url':'https://github.com/tauri-apps/binary-releases/releases/download/nsis-3.13/nsis-3.13.zip','sha256':audit.digest(b'official-fixture')}
            (root/'packaging/nsis-toolchain.lock.json').write_text(json.dumps({'nsis':record}),encoding='utf-8')
            with patch.object(audit,'ROOT',root),patch.object(audit.urllib.request,'urlopen',side_effect=AssertionError('No network')):
                with self.assertRaisesRegex(ValueError,'Missing'):audit.prepare_archive(offline=True)
                (cache/record['filename']).write_bytes(b'tampered')
                with self.assertRaisesRegex(ValueError,'hash'):audit.prepare_archive(offline=True)
                (cache/record['filename']).write_bytes(b'official-fixture')
                self.assertEqual(audit.prepare_archive(offline=True),cache/record['filename'])
                record['url']='https://untrusted.example/nsis.zip';(root/'packaging/nsis-toolchain.lock.json').write_text(json.dumps({'nsis':record}),encoding='utf-8')
                with self.assertRaisesRegex(ValueError,'source'):audit.prepare_archive()
    def test_only_documented_tauri_bundle_marker_may_differ(self):
        build=b'code__TAURI_BUNDLE_TYPE_VAR_UNKtail';package=b'code__TAURI_BUNDLE_TYPE_VAR_NSStail'
        self.assertEqual(launcher_match(build,package),'only_Tauri_UNK_to_NSS_bundle_marker')
        with self.assertRaises(ValueError):launcher_match(build,package+b'tampered')
        with self.assertRaises(ValueError):launcher_match(build,package.replace(b'code',b'evil'))
    def test_windows_paths_collisions_and_links_block_before_extraction(self):
        for value in ('../secret','C:/secret','a/CON.txt','a\\..\\x'):
            with self.subTest(value=value),self.assertRaises(ValueError):listing(archive('Path = '+value+'\nSize = 1'))
        with self.assertRaises(ValueError):listing(archive('Path = A\nSize = 1','Path = a\nSize = 2'))
        with self.assertRaises(ValueError):listing(archive('Path = a\nSize = 1\nSymbolic Link = target'))

    def test_missing_sizes_large_extractions_and_wrong_archives_fail_closed(self):
        for data in ('Type = Zip\n\n----------\nPath = a\nSize = 1',archive('Path = a\nSize = '),archive('Path = a\nSize = 1073741825')):
            with self.subTest(data=data),self.assertRaises(ValueError):listing(data)

    def test_nsis_uninstaller_and_plugin_tokens_are_contained_relative_names(self):
        data=archive('Path = $PLUGINSDIR\\System.dll\nSize = 12\nAttributes = ','Path = uninstall.exe\nSize = ')
        self.assertEqual(listing(data),{'$PLUGINSDIR/System.dll':12,'uninstall.exe':0})

    def test_exact_expected_files_include_notices_and_manifest_but_not_host_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'COPYING.txt').write_text('fixture')
            names=expected_files({'files':{'python.exe':{}}},root,{'$PLUGINSDIR/System.dll':{}})
            self.assertEqual(names,{'runtime/python.exe','runtime/runtime-manifest.json','notices/COPYING.txt','color-studio-beta.exe','uninstall.exe','$PLUGINSDIR/System.dll'})


if __name__=='__main__':unittest.main()
