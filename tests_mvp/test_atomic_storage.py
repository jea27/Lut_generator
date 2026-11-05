"""Workspace-only fault injection: never use the installed application's store."""
import os
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from apps.api.storage import atomic_bytes, atomic_json

ROOT = Path(__file__).resolve().parents[1]


class AtomicStorageTests(unittest.TestCase):
    def setUp(self):
        private = ROOT / '.lumaforge-local'
        private.mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix='atomic-synthetic-', dir=private)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def writers(self):
        return ((atomic_json, {'synthetic': 'new record'}),
                (atomic_bytes, b'new synthetic image bytes'))

    def test_failed_commit_keeps_replacement_at_pending_name(self):
        for index, (writer, value) in enumerate(self.writers()):
            with self.subTest(writer=writer.__name__):
                target = self.root / f'record-{index}'
                target.write_bytes(b'previous synthetic record')
                foreign_paths = []

                def replace(source, destination):
                    source = Path(source)
                    source.rename(self.root / f'retained-original-{index}')
                    source.write_bytes(b'foreign synthetic file; preserve')
                    foreign_paths.append(source)
                    raise PermissionError('Synthetic publication failure')

                with patch('apps.api.storage.os.replace', side_effect=replace):
                    with self.assertRaises(PermissionError):
                        writer(target, value)
                self.assertEqual(target.read_bytes(), b'previous synthetic record')
                self.assertEqual(len(foreign_paths), 1)
                self.assertTrue(foreign_paths[0].exists(), 'Cleanup deleted a replacement it did not create')
                self.assertEqual(foreign_paths[0].read_bytes(), b'foreign synthetic file; preserve')

    def test_successful_commit_keeps_reused_pending_name(self):
        real_replace = os.replace
        for index, (writer, value) in enumerate(self.writers()):
            with self.subTest(writer=writer.__name__):
                target = self.root / f'record-{index}'
                foreign_paths = []

                def replace(source, destination):
                    real_replace(source, destination)
                    Path(source).write_bytes(b'new unrelated synthetic file')
                    foreign_paths.append(Path(source))

                with patch('apps.api.storage.os.replace', side_effect=replace):
                    writer(target, value)
                self.assertTrue(target.is_file())
                self.assertEqual(len(foreign_paths), 1)
                self.assertTrue(foreign_paths[0].exists(), 'Cleanup deleted a newly reused name')
                self.assertEqual(foreign_paths[0].read_bytes(), b'new unrelated synthetic file')

    def test_failed_sync_keeps_previous_content_and_removes_only_owned_pending(self):
        for index, (writer, value) in enumerate(self.writers()):
            with self.subTest(writer=writer.__name__):
                target = self.root / f'record-{index}'
                target.write_bytes(b'previous synthetic bytes')
                with patch('apps.api.storage.os.fsync', side_effect=OSError('Synthetic disk failure')):
                    with self.assertRaises(OSError):
                        writer(target, value)
                self.assertEqual(target.read_bytes(), b'previous synthetic bytes')
                self.assertEqual(list(self.root.glob('.pending-*')), [])

    def test_changed_temporary_is_not_published_or_cleaned(self):
        target = self.root / 'preferences.json'
        target.write_bytes(b'previous synthetic record')
        real_fdopen = os.fdopen
        foreign_paths = []

        @contextmanager
        def fdopen(*args, **kwargs):
            with real_fdopen(*args, **kwargs) as stream:
                yield stream
            pending, = self.root.glob('.pending-*')
            pending.rename(self.root / 'retained-original')
            pending.write_bytes(b'unrelated synthetic content')
            foreign_paths.append(pending)

        with patch('apps.api.storage.os.fdopen', side_effect=fdopen):
            with self.assertRaisesRegex(OSError, 'Private temporary changed'):
                atomic_json(target, {'synthetic': 'new value'})
        self.assertEqual(target.read_bytes(), b'previous synthetic record')
        self.assertEqual(foreign_paths[0].read_bytes(), b'unrelated synthetic content')

    def test_create_only_preserves_existing_file_for_both_writers(self):
        for index, (writer, value) in enumerate(self.writers()):
            with self.subTest(writer=writer.__name__):
                target = self.root / f'record-{index}'
                target.write_bytes(b'existing synthetic bytes')
                with self.assertRaises(FileExistsError):
                    writer(target, value, overwrite=False)
                self.assertEqual(target.read_bytes(), b'existing synthetic bytes')
                self.assertEqual(list(self.root.glob('.pending-*')), [])

    def test_concurrent_create_only_has_one_winner_and_no_truncated_output(self):
        target = self.root / 'new-image.png'
        barrier = threading.Barrier(6)

        def create(index):
            payload = bytes([index]) * 65536
            barrier.wait(timeout=5)
            try:
                atomic_bytes(target, payload, overwrite=False)
            except FileExistsError:
                return None
            return payload

        with ThreadPoolExecutor(max_workers=6) as pool:
            winners = [payload for payload in pool.map(create, range(6)) if payload is not None]
        self.assertEqual(len(winners), 1)
        self.assertEqual(target.read_bytes(), winners[0])
        self.assertEqual(list(self.root.glob('.pending-*')), [])

    def test_link_publication_branch_keeps_collision_and_completed_content(self):
        # Exercise the POSIX strategy using real hard links, also on Windows NTFS.
        target = self.root / 'linked-output'
        with patch('apps.api.storage._WINDOWS', False):
            atomic_bytes(target, b'synthetic complete output', overwrite=False)
            with self.assertRaises(FileExistsError):
                atomic_bytes(target, b'conflicting output', overwrite=False)
        self.assertEqual(target.read_bytes(), b'synthetic complete output')
        self.assertEqual(list(self.root.glob('.pending-*')), [])

    def test_link_failure_does_not_fall_back_to_overwrite(self):
        target = self.root / 'unsupported-output'
        with patch('apps.api.storage._WINDOWS', False), patch(
                'apps.api.storage.os.link', side_effect=OSError('Synthetic unsupported filesystem')):
            with self.assertRaises(OSError):
                atomic_bytes(target, b'synthetic output', overwrite=False)
        self.assertFalse(target.exists())
        self.assertEqual(list(self.root.glob('.pending-*')), [])


if __name__ == '__main__':
    unittest.main()
