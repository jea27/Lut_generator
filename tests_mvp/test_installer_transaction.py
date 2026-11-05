"""Synthetic filesystem transactions, not Windows installation/power-loss evidence.

Fake MZ fixtures are inert byte strings. No executable, old uninstaller, real
preference store, personal photograph or system directory is opened or run.
"""
import errno
import hashlib
import json
import os
import subprocess
from pathlib import Path
import tempfile
import unittest
import shutil
import time
import uuid
from unittest.mock import patch

from apps.desktop import installer_helper as installer


ROOT=Path(__file__).resolve().parents[1]


class SyntheticInterruption(BaseException):
    """Bypass ordinary exception handling to leave a crash-recovery fixture."""


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def snapshot(directory):
    if not directory.exists():return None
    return {p.relative_to(directory).as_posix():digest(p.read_bytes())
            for p in directory.rglob('*') if p.is_file()}


class InstallerTransactionTests(unittest.TestCase):
    def setUp(self):
        private=ROOT/'.lumaforge-local';private.mkdir(exist_ok=True)
        self.temporary=tempfile.TemporaryDirectory(prefix='installer-synthetic-',dir=private)
        self.addCleanup(self.temporary.cleanup)
        self.root=Path(self.temporary.name)
        self.target=self.root/'Color Studio QA'
        self.stage=self.root/'.lf-stage-synthetic'
        self.data=self.root/'External Data QA';self.data.mkdir()
        (self.data/'preferences.json').write_text('{"workspace":"pro","language":"en"}',encoding='utf-8')
        (self.data/'images').mkdir();(self.data/'presets').mkdir()
        for index in range(6):(self.data/'images'/f'synthetic-{index}.png').write_bytes(b'Inert synthetic PNG sentinel '+bytes([index]))
        for index in range(2):(self.data/'presets'/f'synthetic-{index}.json').write_bytes(b'{"fixture":"saved recipe, not a real user"}')
        self.original_data=snapshot(self.data)
        self.assertEqual(len(self.original_data),9)

    def package(self,path,version='0.3.0-beta.4',legacy_files=False):
        path.mkdir()
        files={installer.LAUNCHER:b'MZ synthetic launcher '+version.encode(),
               'runtime/python.exe':b'MZ synthetic interpreter '+version.encode(),
               'runtime/app/fixture.py':b'# Synthetic inert source\n',
               'notices/LICENSE.txt':b'Synthetic test notice, not a license grant\n'}
        if legacy_files:
            files.update({'ColorEngine.exe':b'MZ synthetic legacy sidecar',
                          '_internal/legacy.dll':b'MZ synthetic legacy dependency'})
        for name,raw in files.items():
            file=path/name;file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(raw)
        (path/'uninstall.exe').write_bytes(b'MZ synthetic generated uninstaller, never executed')
        ledger={'schema':1,'product':installer.PRODUCT,'version':version,'source':'1'*40,
                'generated':['uninstall.exe'],'files':{name:digest(raw) for name,raw in files.items()}}
        (path/installer.LEDGER).write_text(json.dumps(ledger),encoding='utf-8')
        return installer.sha(path/installer.LEDGER)

    def old_package(self,extras=False):
        self.package(self.target,'0.3.0-beta.3',legacy_files=True)
        if extras:
            (self.target/'personal-sentinel.txt').write_bytes(b'Synthetic personal file; preserve exactly')
            (self.target/'User originals').mkdir()
            (self.target/'User originals/fixture.raw').write_bytes(b'Synthetic original, not a photograph')
            (self.target/'User originals/saved.recipe.json').write_bytes(b'{"synthetic":"saved recipe, preserve"}')
        return snapshot(self.target)

    def assert_data_untouched(self):
        self.assertEqual(snapshot(self.data),self.original_data)

    def journal_record(self):
        return json.loads(installer.journal_path(self.target).read_text(encoding='utf-8'))

    def interrupt_after_old_move(self,expected):
        def fault(phase):
            if phase=='after_old_move':raise SyntheticInterruption('Synthetic interruption; not a real power cut')
        with self.assertRaises(SyntheticInterruption):
            installer.commit(self.stage,self.target,expected,fault=fault)
        self.assertFalse(self.target.exists())
        self.assertTrue(installer.journal_path(self.target).is_file())
        return self.root/self.journal_record()['backup']

    def interrupt_after_new_move(self,expected):
        original=Path.rename
        def rename(path,destination):
            result=original(path,destination)
            if path==self.stage:raise SyntheticInterruption('Synthetic interruption after directory switch')
            return result
        try:
            with patch.object(Path,'rename',new=rename),self.assertRaises(SyntheticInterruption):
                installer.commit(self.stage,self.target,expected)
        except installer.InstallError as error:
            # Preserve only this test-owned synthetic tree before unittest cleanup.
            # A successful rerun does not explain an earlier filesystem error.
            evidence=ROOT/'.lumaforge-local'/('installer-unexpected-'+uuid.uuid4().hex)
            shutil.copytree(self.root,evidence,symlinks=True)
            (evidence/'failure.json').write_text(json.dumps({'schema':'synthetic-installer-failure-v1',
                'test':self.id(),'observed_unix_ns':time.time_ns(),'error':error.report(),
                'target_exists':self.target.exists(),'stage_exists':self.stage.exists(),
                'historical_actor_identified':False,'scope':'Only this owned synthetic fixture; never actual application data'},indent=2)+'\n',encoding='utf-8')
            raise
        self.assertTrue(self.target.is_dir())
        self.assertTrue(installer.journal_path(self.target).is_file())

    def symlink(self,path,destination,directory=False):
        try:path.symlink_to(destination,target_is_directory=directory)
        except NotImplementedError:
            self.skipTest('Symlink fixtures are not supported by this interpreter')
        except OSError as error:
            if getattr(error,'winerror',None) in (1314,50) or error.errno in (errno.EPERM,errno.EACCES,errno.ENOTSUP):
                self.skipTest('Symlink fixture requires unavailable privileges/support; no permissions changed')
            raise

    def junction(self,path,destination):
        if os.name!='nt':self.skipTest('Real NTFS junction case is covered on Windows')
        self.assertTrue(path.absolute().is_relative_to(self.root))
        self.assertTrue(destination.resolve().is_relative_to(self.root))
        env=dict(os.environ,LF_TEST_JUNCTION=str(path),LF_TEST_DESTINATION=str(destination))
        subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',
            'New-Item -ItemType Junction -Path $env:LF_TEST_JUNCTION -Target $env:LF_TEST_DESTINATION -ErrorAction Stop | Out-Null'],
            env=env,check=True,capture_output=True,timeout=20)
        self.assertTrue(path.is_junction())
        self.addCleanup(lambda:path.rmdir() if path.is_junction() else None)

    def test_clean_install_commits_verified_fake_package_without_backup(self):
        expected=self.package(self.stage);before=snapshot(self.stage)
        result=installer.commit(self.stage,self.target,expected)
        self.assertTrue(result['ok']);self.assertEqual(result['phase'],'committed')
        self.assertIsNone(result['previous_directory'])
        self.assertEqual(result['personal_top_entries_preserved'],0)
        self.assertFalse(result['data_store_modified'])
        self.assertEqual(snapshot(self.target),before)
        self.assertFalse(self.stage.exists());self.assertFalse(installer.journal_path(self.target).exists())
        installer.verify(self.target,expected);self.assert_data_untouched()

    def test_private_store_names_are_rejected_before_any_journal_or_recovery(self):
        expected=self.package(self.stage)
        for target in (self.root/'ColorStudioBetaData',self.root/'colorstudiobetadata'/'nested-app'):
            with self.subTest(target=target.name):
                before=snapshot(self.root)
                with self.assertRaises(installer.InstallError) as raised:installer.commit(self.stage,target,expected)
                self.assertEqual(raised.exception.phase,'private_data_install_location')
                with self.assertRaises(installer.InstallError):installer.recover(target)
                self.assertEqual(snapshot(self.root),before);self.assert_data_untouched()

    def test_custom_private_store_and_its_ancestors_are_never_install_targets(self):
        expected=self.package(self.stage)
        private=self.root/'Custom Private Store';self.package(private)
        before=snapshot(self.root)
        with patch.dict(os.environ,{'LUMAFORGE_DATA_DIR':str(private)}):
            for target in (private,private/'child',self.root):
                with self.subTest(target=target.name),self.assertRaises(installer.InstallError) as raised:
                    installer.commit(self.stage,target,expected)
                self.assertEqual(raised.exception.phase,'private_data_install_location')
            with self.assertRaises(installer.InstallError):installer.recover(private)
        self.assertEqual(snapshot(self.root),before);self.assert_data_untouched()

    def test_update_keeps_complete_old_backup_personal_extras_and_external_data(self):
        old=self.old_package(extras=True);expected=self.package(self.stage)
        result=installer.commit(self.stage,self.target,expected)
        self.assertRegex(result['previous_directory'],r'^\.lf-previous-[a-f0-9]{32}$')
        backup=self.root/result['previous_directory'];self.assertEqual(snapshot(backup),old)
        self.assertEqual(result['personal_top_entries_preserved'],2)
        for name in ('personal-sentinel.txt','User originals/fixture.raw'):
            self.assertEqual((self.target/name).read_bytes(),(backup/name).read_bytes())
        self.assertFalse((self.target/'ColorEngine.exe').exists())
        self.assertFalse((self.target/'_internal').exists())
        self.assertNotEqual(installer.sha(self.target/installer.LAUNCHER),old[installer.LAUNCHER])
        installer.verify(self.target,expected,personal_extras=True);self.assert_data_untouched()

    def test_corrupted_staged_payload_leaves_old_installation_byte_identical(self):
        old=self.old_package(extras=True);expected=self.package(self.stage)
        (self.stage/'runtime/python.exe').write_bytes(b'MZ synthetic tamper')
        with self.assertRaises(installer.InstallError) as raised:
            installer.commit(self.stage,self.target,expected)
        self.assertEqual(raised.exception.phase,'package_hash_mismatch')
        self.assertEqual(snapshot(self.target),old)
        self.assertFalse(installer.journal_path(self.target).exists())
        self.assertEqual(list(self.root.glob('.lf-previous-*')),[]);self.assert_data_untouched()

    def test_corrupted_manifest_digest_never_starts_directory_switch(self):
        old=self.old_package();self.package(self.stage)
        with self.assertRaises(installer.InstallError) as raised:
            installer.commit(self.stage,self.target,'0'*64)
        self.assertEqual(raised.exception.phase,'manifest_hash_mismatch')
        self.assertEqual(snapshot(self.target),old)
        self.assertFalse(installer.journal_path(self.target).exists());self.assert_data_untouched()

    def test_oserror_after_old_move_rolls_back_and_fresh_stage_retry_succeeds(self):
        old=self.old_package(extras=True);expected=self.package(self.stage)
        def fault(phase):
            if phase=='after_old_move':
                error=OSError(errno.EACCES,'Synthetic denied rename')
                error.winerror=32 # Synthetic Win32 code, not a real sharing violation.
                raise error
        with self.assertRaises(installer.InstallError) as raised:
            installer.commit(self.stage,self.target,expected,fault=fault)
        report=raised.exception.report()
        self.assertEqual(set(report),{'ok','phase','errno','winerror','old_restored'})
        self.assertFalse(report['ok']);self.assertEqual(report['winerror'],32)
        self.assertEqual(report['phase'],'directory_switch_failed')
        self.assertEqual(report['errno'],errno.EACCES);self.assertTrue(report['old_restored'])
        self.assertEqual(snapshot(self.target),old);self.assertTrue(self.stage.is_dir())
        self.assertFalse(installer.journal_path(self.target).exists());self.assert_data_untouched()
        # NSIS extracts a fresh stage on a retry; the failed stage remains evidence.
        retry=self.root/'.lf-stage-retry';new_hash=self.package(retry)
        result=installer.commit(retry,self.target,new_hash)
        self.assertTrue(result['ok']);self.assertEqual(snapshot(self.root/result['previous_directory']),old)
        self.assertTrue(self.stage.is_dir());self.assert_data_untouched()

    def test_failed_rollback_keeps_journal_and_backup_for_later_guarded_recovery(self):
        old=self.old_package();expected=self.package(self.stage);original=Path.rename
        def rename(path,destination):
            if path==self.stage or path.name.startswith('.lf-previous-'):
                raise OSError(errno.EACCES,'Synthetic switch and rollback lock')
            return original(path,destination)
        with patch.object(Path,'rename',new=rename),self.assertRaises(installer.InstallError) as raised:
            installer.commit(self.stage,self.target,expected)
        self.assertFalse(raised.exception.report()['old_restored'])
        record=self.journal_record();backup=self.root/record['backup']
        self.assertEqual(snapshot(backup),old);self.assertFalse(self.target.exists())
        self.assertTrue(self.stage.is_dir());self.assert_data_untouched()
        self.assertEqual(installer.recover(self.target),'old_restored_after_interruption')
        self.assertEqual(snapshot(self.target),old);self.assert_data_untouched()

    def test_interrupted_before_old_move_is_recovered_without_modifying_old(self):
        old=self.old_package();expected=self.package(self.stage)
        def fault(phase):
            if phase=='before_old_move':raise SyntheticInterruption('Synthetic pre-move interruption')
        with self.assertRaises(SyntheticInterruption):
            installer.commit(self.stage,self.target,expected,fault=fault)
        self.assertEqual(snapshot(self.target),old)
        self.assertEqual(installer.recover(self.target),'old_not_moved')
        self.assertEqual(installer.recover(self.target),'none')
        self.assertEqual(snapshot(self.target),old);self.assert_data_untouched()

    def test_interrupted_after_old_move_restores_backup_and_recovery_is_idempotent(self):
        old=self.old_package(extras=True);expected=self.package(self.stage)
        backup=self.interrupt_after_old_move(expected);self.assertEqual(snapshot(backup),old)
        self.assertEqual(installer.recover(self.target),'old_restored_after_interruption')
        self.assertEqual(snapshot(self.target),old);self.assertTrue(self.stage.is_dir())
        self.assertFalse(backup.exists());self.assertEqual(installer.recover(self.target),'none')
        self.assert_data_untouched()

    def test_commit_recovers_prior_interruption_before_applying_fresh_stage(self):
        old=self.old_package();expected=self.package(self.stage)
        self.interrupt_after_old_move(expected)
        retry=self.root/'.lf-stage-next-execution';retry_hash=self.package(retry)
        result=installer.commit(retry,self.target,retry_hash)
        self.assertEqual(result['recovery'],'old_restored_after_interruption')
        self.assertEqual(snapshot(self.root/result['previous_directory']),old)
        installer.verify(self.target,retry_hash);self.assertTrue(self.stage.is_dir());self.assert_data_untouched()

    def test_interrupted_after_new_move_verifies_new_commit_and_keeps_backup(self):
        old=self.old_package(extras=True);expected=self.package(self.stage)
        self.interrupt_after_new_move(expected);backup=self.root/self.journal_record()['backup']
        new=snapshot(self.target)
        self.assertEqual(installer.recover(self.target),'new_commit_verified_after_interruption')
        self.assertEqual(snapshot(self.target),new);self.assertEqual(snapshot(backup),old)
        self.assertEqual(installer.recover(self.target),'none');self.assert_data_untouched()

    def test_interrupted_fresh_install_verifies_new_target_without_old_backup(self):
        expected=self.package(self.stage);self.interrupt_after_new_move(expected)
        before=snapshot(self.target)
        self.assertEqual(installer.recover(self.target),'old_not_moved')
        self.assertEqual(snapshot(self.target),before)
        installer.verify(self.target,expected);self.assert_data_untouched()

    def test_unexpected_switch_error_retains_a_synthetic_diagnostic_before_cleanup(self):
        expected=self.package(self.stage);original=Path.rename
        before=set((ROOT/'.lumaforge-local').glob('installer-unexpected-*'))
        def deny(path,destination):
            if path==self.stage:raise PermissionError(errno.EACCES,'Controlled synthetic directory denial')
            return original(path,destination)
        with patch.object(Path,'rename',new=deny),self.assertRaises(installer.InstallError):
            self.interrupt_after_new_move(expected)
        added=set((ROOT/'.lumaforge-local').glob('installer-unexpected-*'))-before
        self.assertEqual(len(added),1);evidence=added.pop()
        try:
            record=json.loads((evidence/'failure.json').read_bytes())
            self.assertEqual(record['error']['phase'],'directory_switch_failed')
            self.assertEqual(record['error']['errno'],errno.EACCES)
            self.assertEqual(snapshot(evidence/'External Data QA'),self.original_data)
            self.assert_data_untouched()
        finally:
            # Delete only the diagnostic produced by this known synthetic injection.
            self.assertEqual(evidence.resolve().parent,(ROOT/'.lumaforge-local').resolve())
            self.assertEqual(record['test'],self.id())
            shutil.rmtree(evidence)

    def test_changed_backup_personal_file_is_not_restored_automatically(self):
        self.old_package(extras=True);expected=self.package(self.stage);backup=self.interrupt_after_old_move(expected)
        launcher_before=installer.sha(backup/installer.LAUNCHER)
        (backup/'personal-sentinel.txt').write_bytes(b'Synthetic personal edit after interruption')
        changed=snapshot(backup)
        with self.assertRaises(installer.InstallError) as raised:installer.recover(self.target)
        self.assertEqual(raised.exception.phase,'recovery_backup_changed')
        self.assertEqual(installer.sha(backup/installer.LAUNCHER),launcher_before)
        self.assertEqual(snapshot(backup),changed);self.assertFalse(self.target.exists())
        self.assertTrue(installer.journal_path(self.target).exists());self.assert_data_untouched()

    def test_corrupt_new_commit_requires_intervention_without_overwriting_either_tree(self):
        old=self.old_package();expected=self.package(self.stage);self.interrupt_after_new_move(expected)
        backup=self.root/self.journal_record()['backup']
        (self.target/'runtime/python.exe').write_bytes(b'MZ synthetic altered committed file')
        changed=snapshot(self.target)
        with self.assertRaises(installer.InstallError) as raised:installer.recover(self.target)
        self.assertEqual(raised.exception.phase,'package_hash_mismatch')
        self.assertEqual(snapshot(self.target),changed);self.assertEqual(snapshot(backup),old)
        self.assertTrue(installer.journal_path(self.target).is_file());self.assert_data_untouched()

    def test_reappearing_target_retains_journal_backup_and_foreign_recipe(self):
        old=self.old_package(extras=True);expected=self.package(self.stage)
        def fault(phase):
            if phase=='after_old_move':
                self.target.mkdir()
                (self.target/'replacement.recipe.json').write_bytes(b'{"synthetic":"foreign replacement, preserve"}')
        with self.assertRaises(installer.InstallError) as raised:installer.commit(self.stage,self.target,expected,fault=fault)
        self.assertEqual(raised.exception.phase,'directory_switch_failed')
        self.assertIs(raised.exception.report()['old_restored'],False)
        journal=installer.journal_path(self.target);self.assertTrue(journal.is_file())
        backup=self.root/self.journal_record()['backup'];self.assertEqual(snapshot(backup),old)
        foreign=snapshot(self.target)
        with self.assertRaises((installer.InstallError,OSError)):installer.recover(self.target)
        self.assertTrue(journal.is_file());self.assertEqual(snapshot(self.target),foreign)
        self.assertEqual(snapshot(backup),old);self.assert_data_untouched()
        # The replacement is a test-owned synthetic fixture. Retain it elsewhere;
        # a real unknown directory requires operator review, never automatic purge.
        self.target.rename(self.root/'retained-foreign-target')
        self.assertEqual(installer.recover(self.target),'old_restored_after_interruption')
        self.assertEqual(snapshot(self.target),old);self.assert_data_untouched()

    def test_unknown_nonempty_root_is_preserved_and_rejected(self):
        self.target.mkdir();(self.target/'unrelated.txt').write_bytes(b'Synthetic unrelated directory')
        old=snapshot(self.target);expected=self.package(self.stage)
        with self.assertRaises(installer.InstallError) as raised:
            installer.commit(self.stage,self.target,expected)
        self.assertEqual(raised.exception.phase,'target_not_owned')
        self.assertEqual(snapshot(self.target),old)
        self.assertFalse(installer.journal_path(self.target).exists());self.assert_data_untouched()

    def test_protected_root_and_non_sibling_stage_are_rejected_before_any_move(self):
        old=self.old_package();expected=self.package(self.stage)
        with patch.dict(os.environ,{'USERPROFILE':str(self.target)}),self.assertRaises(installer.InstallError) as raised:
            installer.commit(self.stage,self.target,expected)
        self.assertEqual(raised.exception.phase,'protected_install_location')
        other=self.root/'other';other.mkdir();nested=other/'stage';nested_hash=self.package(nested)
        with self.assertRaises(installer.InstallError) as raised:installer.commit(nested,self.target,nested_hash)
        self.assertEqual(raised.exception.phase,'unsafe_install_location')
        self.assertEqual(snapshot(self.target),old);self.assert_data_untouched()

    def test_manifest_traversal_windows_devices_and_case_collisions_never_move_old(self):
        old=self.old_package()
        for index,name in enumerate(('../outside.txt','/absolute','C:/private','runtime\\escape.dll','NUL.txt','a/COM1.log','runtime//x','runtime/x.')):
            with self.subTest(name=name):
                stage=self.root/('stage-invalid-'+str(index));self.package(stage)
                ledger=json.loads((stage/installer.LEDGER).read_text(encoding='utf-8'))
                ledger['files'][name]=digest(b'not a real file')
                (stage/installer.LEDGER).write_text(json.dumps(ledger),encoding='utf-8')
                with self.assertRaises(installer.InstallError) as raised:
                    installer.commit(stage,self.target,installer.sha(stage/installer.LEDGER))
                self.assertEqual(raised.exception.phase,'invalid_package_path')
                self.assertEqual(snapshot(self.target),old)
        self.package(self.stage);ledger=json.loads((self.stage/installer.LEDGER).read_text(encoding='utf-8'))
        ledger['files']['RUNTIME/PYTHON.EXE']=ledger['files']['runtime/python.exe']
        (self.stage/installer.LEDGER).write_text(json.dumps(ledger),encoding='utf-8')
        with self.assertRaises(installer.InstallError) as raised:
            installer.commit(self.stage,self.target,installer.sha(self.stage/installer.LEDGER))
        self.assertEqual(raised.exception.phase,'invalid_manifest')
        self.assertEqual(snapshot(self.target),old);self.assert_data_untouched()

    def test_recovery_journal_cannot_escape_sibling_directory(self):
        old=self.old_package();expected=self.package(self.stage)
        record={'product':installer.PRODUCT,'target':self.target.name,'stage':'../outside',
                'backup':'.lf-previous-'+'a'*32,'old_launcher_sha256':installer.sha(self.target/installer.LAUNCHER),
                'old_tree_sha256':installer.tree_digest(self.target),
                'manifest_sha256':expected}
        installer.write_journal(installer.journal_path(self.target),record)
        with self.assertRaises(installer.InstallError):installer.recover(self.target)
        self.assertEqual(snapshot(self.target),old)
        self.assertTrue(installer.journal_path(self.target).is_file());self.assert_data_untouched()

    def test_malformed_private_journal_is_retained_without_renaming_data(self):
        old=self.old_package();expected=self.package(self.stage)
        journal=installer.journal_path(self.target)
        for raw in ('null','[]','{"product":"one","product":"two"}'):
            with self.subTest(raw=raw):
                journal.write_text(raw,encoding='utf-8')
                with self.assertRaises(installer.InstallError) as raised:
                    installer.commit(self.stage,self.target,expected)
                self.assertEqual(raised.exception.phase,'invalid_manifest')
                self.assertEqual(journal.read_text(encoding='utf-8'),raw)
                self.assertEqual(snapshot(self.target),old);self.assert_data_untouched()

    def test_another_transaction_lock_blocks_update_without_modifying_either_tree(self):
        old=self.old_package();expected=self.package(self.stage);staged=snapshot(self.stage)
        with installer.target_lock(self.target):
            with self.assertRaises(installer.InstallError) as raised:
                installer.commit(self.stage,self.target,expected)
        self.assertEqual(raised.exception.phase,'another_transaction_running')
        self.assertEqual(snapshot(self.target),old);self.assertEqual(snapshot(self.stage),staged)
        self.assertFalse(installer.journal_path(self.target).exists());self.assert_data_untouched()
        # The OS lock is released; keeping its inode must not prevent a later update.
        self.assertTrue(installer.commit(self.stage,self.target,expected)['ok'])
        self.assert_data_untouched()

    def test_user_change_during_staging_is_preserved_and_switch_is_aborted(self):
        old=self.old_package(extras=True);expected=self.package(self.stage)
        replacement=b'Synthetic user edit made while the package was staged'
        def fault(phase):
            if phase=='before_old_move':(self.target/'personal-sentinel.txt').write_bytes(replacement)
        with self.assertRaises(installer.InstallError) as raised:
            installer.commit(self.stage,self.target,expected,fault=fault)
        self.assertEqual(raised.exception.phase,'directory_switch_failed')
        self.assertIsNone(raised.exception.report()['old_restored'])
        self.assertEqual(installer.sha(self.target/installer.LAUNCHER),old[installer.LAUNCHER])
        self.assertEqual((self.target/'personal-sentinel.txt').read_bytes(),replacement)
        self.assertEqual(list(self.root.glob('.lf-previous-*')),[])
        self.assertFalse(installer.journal_path(self.target).exists());self.assert_data_untouched()

    def test_linked_staged_file_is_rejected_without_reading_external_target(self):
        old=self.old_package();expected=self.package(self.stage)
        outside=self.data/'external-fixture.bin';outside.write_bytes(b'Synthetic external bytes')
        self.symlink(self.stage/'runtime/linked.dll',outside)
        with self.assertRaises(installer.InstallError) as raised:installer.commit(self.stage,self.target,expected)
        self.assertEqual(raised.exception.phase,'linked_directory_entry')
        self.assertEqual(snapshot(self.target),old);self.assertEqual(outside.read_bytes(),b'Synthetic external bytes')

    def test_linked_stage_root_is_rejected_before_resolving_it(self):
        old=self.old_package();expected=self.package(self.stage)
        alias=self.root/'stage-alias';self.symlink(alias,self.stage,directory=True)
        with self.assertRaises(installer.InstallError) as raised:installer.commit(alias,self.target,expected)
        self.assertEqual(raised.exception.phase,'linked_install_location')
        self.assertEqual(snapshot(self.target),old);self.assert_data_untouched()

    def test_linked_parent_is_rejected_before_resolve_hides_the_alias(self):
        parent=self.root/'real-parent';parent.mkdir()
        stage=parent/'stage';expected=self.package(stage)
        target=parent/'Color Studio QA';self.package(target,'0.3.0-beta.3');old=snapshot(target)
        alias=self.root/'parent-alias';self.symlink(alias,parent,directory=True)
        with self.assertRaises(installer.InstallError) as raised:
            installer.commit(alias/'stage',alias/target.name,expected)
        self.assertEqual(raised.exception.phase,'linked_install_location')
        self.assertEqual(snapshot(target),old);self.assert_data_untouched()


    def test_ntfs_junction_stage_is_rejected_before_resolving(self):
        old=self.old_package();expected=self.package(self.stage)
        alias=self.root/'stage-junction';self.junction(alias,self.stage)
        with self.assertRaises(installer.InstallError) as raised:installer.commit(alias,self.target,expected)
        self.assertEqual(raised.exception.phase,'linked_install_location')
        self.assertEqual(snapshot(self.target),old);self.assert_data_untouched()

    def test_ntfs_junction_parent_is_rejected_before_resolving(self):
        parent=self.root/'real-parent';parent.mkdir()
        stage=parent/'stage';expected=self.package(stage)
        target=parent/'Color Studio QA';self.package(target,'0.3.0-beta.3');old=snapshot(target)
        alias=self.root/'parent-junction';self.junction(alias,parent)
        with self.assertRaises(installer.InstallError) as raised:installer.commit(alias/'stage',alias/target.name,expected)
        self.assertEqual(raised.exception.phase,'linked_install_location')
        self.assertEqual(snapshot(target),old);self.assert_data_untouched()

    def test_ntfs_junction_payload_does_not_read_or_modify_external_files(self):
        old=self.old_package();expected=self.package(self.stage)
        self.junction(self.stage/'runtime/external',self.data)
        real_sha=installer.sha
        def sha(path):
            self.assertFalse(path.resolve().is_relative_to(self.data))
            return real_sha(path)
        with patch.object(installer,'sha',side_effect=sha),self.assertRaises(installer.InstallError) as raised:
            installer.commit(self.stage,self.target,expected)
        self.assertEqual(raised.exception.phase,'linked_directory_entry')
        self.assertEqual(snapshot(self.target),old);self.assert_data_untouched()

    def test_ntfs_junction_recovery_parent_cannot_move_retained_backup(self):
        old=self.old_package();expected=self.package(self.stage)
        backup=self.interrupt_after_old_move(expected)
        alias=self.root/'recovery-parent-junction';self.junction(alias,self.root)
        with self.assertRaises(installer.InstallError) as raised:installer.recover(alias/self.target.name)
        self.assertEqual(raised.exception.phase,'linked_install_location')
        self.assertFalse(self.target.exists());self.assertEqual(snapshot(backup),old)
        self.assertTrue(installer.journal_path(self.target).is_file());self.assert_data_untouched()

    @unittest.skipUnless(os.name=='nt','Real Windows sharing violation')
    def test_real_directory_lock_denies_switch_preserves_data_and_allows_retry(self):
        import ctypes
        from ctypes import wintypes
        old=self.old_package(extras=True);expected=self.package(self.stage)
        kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        kernel.CreateFileW.argtypes=[wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE]
        kernel.CreateFileW.restype=wintypes.HANDLE
        kernel.CloseHandle.argtypes=[wintypes.HANDLE]
        handle=kernel.CreateFileW(str(self.target),0x80000000,3,None,3,0x02000000,None)
        self.assertNotEqual(handle,ctypes.c_void_p(-1).value)
        try:
            with self.assertRaises(installer.InstallError) as raised:installer.commit(self.stage,self.target,expected)
            self.assertEqual(raised.exception.phase,'directory_switch_failed')
            self.assertIn(raised.exception.report()['winerror'],(5,32))
            self.assertEqual(snapshot(self.target),old);self.assert_data_untouched()
        finally:kernel.CloseHandle(handle)
        retry=self.root/'.lf-stage-after-real-lock';retry_hash=self.package(retry)
        self.assertTrue(installer.commit(retry,self.target,retry_hash)['ok']);self.assert_data_untouched()


if __name__=='__main__':unittest.main()
