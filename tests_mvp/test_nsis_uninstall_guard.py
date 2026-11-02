"""Run the real NSIS path guard against workspace-only filesystem fixtures.

This is not a Color Studio installer or clean-Windows test. The inert probe only
writes its own uninstaller; its uninstall section calls the extracted guard and
never deletes files, changes the registry, or launches installed application code.
"""
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
import zipfile

from scripts.audit_nsis_payload import verify_toolchain


ROOT = Path(__file__).resolve().parents[1]
PRIVATE = ROOT / '.lumaforge-local'
CACHE = ROOT / 'apps/desktop/src-tauri/target/.tauri/NSIS'
ARCHIVE = PRIVATE / 'downloads/nsis-3.13.zip'
REPARSE_POINT = 0x400


@unittest.skipUnless(os.name == 'nt', 'The real NSIS guard probe requires Windows')
class NsisUninstallGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.compiler = CACHE / 'Bin/makensis.exe'
        if not cls.compiler.is_file() or not ARCHIVE.is_file():
            raise unittest.SkipTest('Authorized pinned NSIS 3.13 cache/archive is unavailable; no download or installation')
        try:
            verify_toolchain(ARCHIVE, CACHE)
        except (OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
            raise RuntimeError('Present NSIS 3.13 cache failed official hash/inventory verification: ' + type(error).__name__) from None

        PRIVATE.mkdir(exist_ok=True)
        if PRIVATE.is_symlink() or not PRIVATE.resolve().is_relative_to(ROOT.resolve()):
            raise RuntimeError('Refusing a linked or external probe directory')
        cls.temporary = tempfile.TemporaryDirectory(prefix='ug-', dir=PRIVATE)
        cls.root = Path(cls.temporary.name).absolute()
        cls.junctions = []
        cls.addClassCleanup(cls.cleanup_fixture)
        cls.assert_private(cls.root)
        temporary_files = cls.root / 'Process temporary files'
        temporary_files.mkdir()
        cls.child_env = dict(os.environ, TEMP=str(temporary_files), TMP=str(temporary_files), NSISDIR=str(CACHE))

        template = (ROOT / 'packaging/nsis/installer.nsi').read_text(encoding='utf-8')
        functions = re.findall(r'^Function un\.LFCheckManagedPath\s*\n.*?^FunctionEnd\s*$', template, re.MULTILINE | re.DOTALL)
        if len(functions) != 1:
            raise AssertionError('Expected exactly one real un.LFCheckManagedPath function')
        cls.publisher = cls.root / 'guard-publisher.exe'
        cls.uninstaller = cls.root / 'guard-probe.exe'
        source = '\n'.join((
            'Unicode true',
            '!include LogicLib.nsh',
            '!include FileFunc.nsh',
            'Name "Workspace-only uninstall path guard probe"',
            'RequestExecutionLevel user',
            'SilentInstall silent',
            'SilentUnInstall silent',
            'AutoCloseWindow true',
            'OutFile "' + str(cls.publisher).replace('$', '$$') + '"',
            functions[0],
            'Section',
            '  WriteUninstaller "$EXEDIR\\guard-probe.exe"',
            'SectionEnd',
            'Section Uninstall',
            '  Push "$INSTDIR\\runtime\\vendor"',
            '  Call un.LFCheckManagedPath',
            '  SetErrorLevel 0',
            'SectionEnd',
            '',
        ))
        source_file = cls.root / 'guard-probe.nsi'
        source_file.write_text(source, encoding='utf-8-sig')
        compiled = subprocess.run([str(cls.compiler), '/NOCONFIG', '/V2', str(source_file)],
                                  cwd=cls.root, env=cls.child_env, capture_output=True, text=True, timeout=30)
        if compiled.returncode:
            raise AssertionError('Real guard probe compilation failed:\n' + compiled.stdout + compiled.stderr)
        published = subprocess.run([str(cls.publisher), '/S'], cwd=cls.root, env=cls.child_env,
                                   capture_output=True, text=True, timeout=15)
        if published.returncode or not cls.uninstaller.is_file():
            raise AssertionError('Inert probe could not write its own uninstaller: ' + str(published.returncode))

    @classmethod
    def assert_private(cls, path):
        path = Path(path)
        if not path.is_absolute() or not path.is_relative_to(cls.root) or not path.resolve().is_relative_to(cls.root.resolve()):
            raise RuntimeError('Probe operation escaped its owned workspace fixture')
        if cls.root.parent.resolve() != PRIVATE.resolve() or cls.root.lstat().st_file_attributes & REPARSE_POINT:
            raise RuntimeError('Probe cleanup root is no longer an owned ordinary directory')

    @classmethod
    def cleanup_fixture(cls):
        # Check every absolute target before cleanup. Remove junction entries only;
        # never recurse through them or point a fixture at a system/user directory.
        cls.assert_private(cls.root)
        for link in reversed(cls.junctions):
            cls.assert_private(link)
            try:
                info = link.lstat()
            except FileNotFoundError:
                continue
            if info.st_file_attributes & REPARSE_POINT:
                os.rmdir(link)
        cls.assert_private(cls.root)
        cls.temporary.cleanup()

    def setUp(self):
        # Keep the lexical path short enough for Win32 APIs without enabling
        # long-path policy on the developer or CI host. Child paths retain spaces.
        case = hashlib.sha256(self._testMethodName.encode()).hexdigest()[:8]
        self.fixture = self.root / case
        self.assert_private(self.fixture)
        self.fixture.mkdir()
        self.markers = {}
        self.marker(self.fixture / 'untouched-sibling.txt')

    def marker(self, path):
        self.assert_private(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = b'Synthetic preservation sentinel; not personal data or an executable.\r\n'
        path.write_bytes(payload)
        self.markers[path] = payload

    def run_guard(self, target, expected):
        self.assert_private(target)
        # _?= must be last and its path must not be quoted (NSIS Chapter 3).
        # Passing this raw command line directly to CreateProcess, without a shell,
        # avoids NSIS's normal self-copy to the host temporary directory.
        command = subprocess.list2cmdline([str(self.uninstaller), '/S']) + ' _?=' + str(target)
        result = subprocess.run(command, executable=str(self.uninstaller), cwd=self.root, env=self.child_env,
                                capture_output=True, text=True, timeout=15)
        for path, payload in self.markers.items():
            self.assertEqual(path.read_bytes(), payload, 'Probe modified an owned preservation sentinel')
        self.assertEqual(result.returncode, expected,
                         'Unexpected guard result: ' + str(result.returncode) + '\n' + result.stdout + result.stderr)

    def junction(self, link, destination):
        self.assert_private(link)
        self.assert_private(destination)
        powershell = shutil.which('powershell.exe')
        if not powershell:
            self.skipTest('PowerShell is unavailable for an unprivileged workspace-only junction fixture')
        self.junctions.append(link)
        # The script is fixed; paths are data in the child process environment.
        env = dict(self.child_env, LF_GUARD_LINK=str(link), LF_GUARD_DESTINATION=str(destination))
        created = subprocess.run([powershell, '-NoProfile', '-NonInteractive', '-Command',
                                  "New-Item -ItemType Junction -Path $env:LF_GUARD_LINK -Target $env:LF_GUARD_DESTINATION -ErrorAction Stop | Out-Null"],
                                 cwd=self.root, env=env, capture_output=True, text=True, timeout=15)
        if created.returncode:
            self.skipTest('Windows did not permit an unprivileged junction inside the owned fixture')
        self.assert_private(link)
        self.assertTrue(link.lstat().st_file_attributes & REPARSE_POINT, 'Fixture is not a real Windows junction')

    def test_normal_managed_directory_is_allowed_and_markers_unchanged(self):
        target = self.fixture / 'Application with spaces'
        self.marker(target / 'runtime/vendor/managed-sentinel.txt')
        self.marker(target / 'personal-sentinel.txt')
        self.run_guard(target, 0)

    def test_private_store_root_aborts_before_any_resource_change(self):
        target=self.fixture/'ColorStudioBetaData'
        self.marker(target/'runtime/vendor/private-sentinel.txt')
        self.marker(target/'images/private.png')
        self.run_guard(target,2)

    def test_private_store_ancestor_aborts_even_for_missing_resources(self):
        target=self.fixture/'colorstudiobetadata'/'Nested application'
        self.marker(target.parent/'presets/private.json')
        self.run_guard(target,2)

    def test_missing_managed_directories_are_allowed_without_creating_them(self):
        target = self.fixture / 'Application with missing runtime'
        self.marker(target / 'personal-sentinel.txt')
        self.run_guard(target, 0)
        self.assertFalse((target / 'runtime').exists())
        missing_target = self.fixture / 'Missing installation'
        self.run_guard(missing_target, 0)
        self.assertFalse(missing_target.exists())

    def test_junction_at_managed_directory_aborts_before_changes(self):
        target = self.fixture / 'Application'
        self.marker(target / 'personal-sentinel.txt')
        (target / 'runtime').mkdir()
        destination = self.fixture / 'Owned junction destination'
        self.marker(destination / 'managed-sentinel.txt')
        self.junction(target / 'runtime/vendor', destination)
        self.run_guard(target, 2)

    def test_junction_at_installation_root_aborts_before_changes(self):
        destination = self.fixture / 'Owned application destination'
        self.marker(destination / 'runtime/vendor/managed-sentinel.txt')
        target = self.fixture / 'Application junction'
        self.junction(target, destination)
        self.run_guard(target, 2)

    def test_junction_in_lexical_ancestor_aborts_before_changes(self):
        destination = self.fixture / 'Owned ancestor destination'
        self.marker(destination / 'Application/runtime/vendor/managed-sentinel.txt')
        ancestor = self.fixture / 'Ancestor junction'
        self.junction(ancestor, destination)
        self.run_guard(ancestor / 'Application', 2)


if __name__ == '__main__':
    unittest.main()
