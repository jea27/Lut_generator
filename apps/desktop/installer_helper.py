"""Validate a staged local package, then switch directories with crash recovery.

Only invoked by the per-user installer, using its bundled isolated Python.
Does not touch the separate data store, execute commands, or remove old packages.
"""
import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import uuid

PRODUCT='local.colorstudio.beta'
LEDGER='installer-manifest.json'
LAUNCHER='color-studio-beta.exe'
LEGACY_LAUNCHERS={
 '9308daf515781d77e3e79b2abe2ef942160f377eb17df69013eced27bb8ba7a2', # audited beta2 NSIS
 '0ee92bb92e6573f1cce3d3883a144302716c0923fd8d834e0d151998e4362742', # audited beta3 NSIS
}


class InstallError(Exception):
    def __init__(self,phase,cause=None,restored=None):
        self.phase=phase;self.cause=cause;self.restored=restored
        super().__init__(phase)
    def report(self):
        return {'ok':False,'phase':self.phase,'errno':getattr(self.cause,'errno',None),
                'winerror':getattr(self.cause,'winerror',None),'old_restored':self.restored}


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def linked(path):
    info=path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info,'st_file_attributes',0)&0x400)


def safe_name(value):
    if not isinstance(value,str) or not value or '\\' in value or ':' in value or '\x00' in value:
        raise InstallError('invalid_package_path')
    p=PurePosixPath(value)
    reserved={'CON','PRN','AUX','NUL',*(f'COM{i}' for i in range(1,10)),*(f'LPT{i}' for i in range(1,10))}
    if p.is_absolute() or p.as_posix()!=value or '..' in p.parts or any(x.endswith((' ','.')) or x.split('.')[0].upper() in reserved for x in p.parts):raise InstallError('invalid_package_path')
    return value


def read_json(path):
    if linked(path) or path.stat().st_size>4*1024*1024:raise InstallError('invalid_manifest')
    def object_pairs(pairs):
        obj={}
        for key,value in pairs:
            if key in obj:raise ValueError('duplicate key')
            obj[key]=value
        return obj
    try:
        value=json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=object_pairs)
        if not isinstance(value,dict):raise ValueError('object required')
        return value
    except (ValueError,UnicodeError) as error:raise InstallError('invalid_manifest',error) from None


def tree_files(root):
    if linked(root):raise InstallError('linked_directory')
    found={}
    for p in root.rglob('*'):
        if linked(p):raise InstallError('linked_directory_entry')
        if p.is_file():
            key=p.relative_to(root).as_posix();safe_name(key)
            if key.casefold() in found:raise InstallError('case_collision')
            found[key.casefold()]=key
    return set(found.values())


def verify(root,expected,personal_extras=False):
    if not re.fullmatch('[a-f0-9]{64}',expected) or sha(root/LEDGER)!=expected:raise InstallError('manifest_hash_mismatch')
    ledger=read_json(root/LEDGER)
    if ledger.get('schema')!=1 or ledger.get('product')!=PRODUCT or not isinstance(ledger.get('files'),dict):raise InstallError('invalid_manifest')
    if not re.fullmatch('[a-f0-9]{40}',str(ledger.get('source',''))) or not isinstance(ledger.get('version'),str) or len(ledger['version'])>80 or len(ledger['files'])>5000:raise InstallError('invalid_manifest')
    if ledger.get('generated')!=['uninstall.exe']:raise InstallError('invalid_generated_files')
    expected_files={LEDGER,'uninstall.exe'}
    seen=set()
    for name,digest in ledger['files'].items():
        safe_name(name)
        if name.casefold() in seen or not re.fullmatch('[a-f0-9]{64}',str(digest)):raise InstallError('invalid_manifest')
        seen.add(name.casefold());expected_files.add(name)
    actual=tree_files(root)
    extra=actual-expected_files
    managed={PurePosixPath(n).parts[0].casefold() for n in expected_files}
    if not expected_files<=actual or (extra and (not personal_extras or any(PurePosixPath(n).parts[0].casefold() in managed for n in extra))):raise InstallError('package_file_set_mismatch')
    for name,digest in ledger['files'].items():
        if sha(root/name)!=digest:raise InstallError('package_hash_mismatch')
    with (root/'uninstall.exe').open('rb') as stream:
        if stream.read(2)!=b'MZ':raise InstallError('invalid_uninstaller')
    if LAUNCHER not in ledger['files']:raise InstallError('missing_launcher')
    return ledger


def owned(root):
    if not root.exists():return True
    if linked(root):return False
    if not any(root.iterdir()):return True
    main=root/LAUNCHER
    if not main.is_file() or linked(main):return False
    if sha(main) in LEGACY_LAUNCHERS:return True
    if (root/LEDGER).is_file():
        record=read_json(root/LEDGER)
        return record.get('product')==PRODUCT and isinstance(record.get('files'),dict) and record['files'].get(LAUNCHER)==sha(main)
    return False


def journal_path(target):return target.parent/('.lf-install-'+hashlib.sha256(target.name.casefold().encode()).hexdigest()[:16]+'.json')


def tree_digest(root):
    # Only the aggregate hash enters the private journal; no personal filenames.
    rows={name:sha(root/name) for name in sorted(tree_files(root))}
    return hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()


@contextmanager
def target_lock(target):
    # Stable inode; never unlink a lock while another process may hold it.
    path=journal_path(target).with_suffix('.lock')
    try:
        if linked(path):raise InstallError('linked_transaction_lock')
    except FileNotFoundError:pass
    flags=os.O_RDWR|os.O_CREAT|getattr(os,'O_NOFOLLOW',0)|getattr(os,'O_NOINHERIT',0)
    with os.fdopen(os.open(path,flags,0o600),'r+b') as stream:
        if path.stat().st_size==0:stream.write(b'1');stream.flush()
        stream.seek(0)
        try:
            if os.name=='nt':
                import msvcrt
                msvcrt.locking(stream.fileno(),msvcrt.LK_NBLCK,1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
        except OSError as error:raise InstallError('another_transaction_running',error) from None
        try:yield
        finally:
            stream.seek(0)
            if os.name=='nt':msvcrt.locking(stream.fileno(),msvcrt.LK_UNLCK,1)
            else:fcntl.flock(stream.fileno(),fcntl.LOCK_UN)


def write_journal(path,record):
    raw=(json.dumps(record,sort_keys=True)+'\n').encode()
    with path.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())


def refuse_private_locations(*locations):
    private_override=os.environ.get('LUMAFORGE_DATA_DIR')
    private=Path(private_override).resolve() if private_override else None
    for location in locations:
        if any(part.casefold()=='colorstudiobetadata' for part in location.absolute().parts):
            raise InstallError('private_data_install_location')
        resolved=location.resolve()
        if private is not None and (resolved==private or resolved.is_relative_to(private) or private.is_relative_to(resolved)):
            raise InstallError('private_data_install_location')


def refuse_linked_locations(*locations):
    for location in locations:
        for part in (location.absolute(),*location.absolute().parents):
            try:
                if linked(part):raise InstallError('linked_install_location')
            except FileNotFoundError:pass


def recover(target):
    refuse_linked_locations(target)
    refuse_private_locations(target)
    path=journal_path(target)
    if not path.exists():return 'none'
    record=read_json(path)
    if record.get('product')!=PRODUCT or record.get('target')!=target.name or set(record)!={'product','target','stage','backup','old_launcher_sha256','old_tree_sha256','manifest_sha256'}:
        raise InstallError('invalid_recovery_journal')
    for field in ('stage','backup'):safe_name(record[field])
    if not re.fullmatch('[a-f0-9]{64}',str(record['manifest_sha256'])) or (record['old_launcher_sha256'] is not None and not re.fullmatch('[a-f0-9]{64}',str(record['old_launcher_sha256']))):raise InstallError('invalid_recovery_journal')
    if record['old_tree_sha256'] is not None and not re.fullmatch('[a-f0-9]{64}',str(record['old_tree_sha256'])):raise InstallError('invalid_recovery_journal')
    if '/' in record['stage'] or not re.fullmatch(r'\.lf-previous-[a-f0-9]{32}',record['backup']):raise InstallError('invalid_recovery_journal')
    backup=target.parent/record['backup']
    if backup.exists():
        original=record['old_launcher_sha256']
        if linked(backup) or not owned(backup) or (original and sha(backup/LAUNCHER)!=original) or (not original and any(backup.iterdir())) or tree_digest(backup)!=record['old_tree_sha256']:
            raise InstallError('recovery_backup_changed')
    if not target.exists() and backup.exists():
        backup.rename(target);path.unlink();return 'old_restored_after_interruption'
    if target.exists() and backup.exists():
        verify(target,record['manifest_sha256'],personal_extras=True);path.unlink();return 'new_commit_verified_after_interruption'
    if not backup.exists():
        if target.exists() and record['old_launcher_sha256'] and sha(target/LAUNCHER)!=record['old_launcher_sha256']:raise InstallError('recovery_target_changed')
        if target.exists() and record['old_tree_sha256'] and tree_digest(target)!=record['old_tree_sha256']:raise InstallError('recovery_target_changed')
        if target.exists() and record['old_tree_sha256'] is None:verify(target,record['manifest_sha256'],personal_extras=True)
        path.unlink();return 'old_not_moved'
    raise InstallError('manual_recovery_required')


def commit(stage,target,expected,fault=None):
    refuse_linked_locations(stage,target)
    refuse_private_locations(stage,target)
    stage=stage.resolve();target=target.resolve()
    if stage==target or stage.parent!=target.parent or target==target.parent or linked(stage):raise InstallError('unsafe_install_location')
    # A regular NSIS stage is a fresh sibling, never a folder within the old app.
    for ancestor in (stage.parent,target.parent):
        if linked(ancestor):raise InstallError('linked_install_parent')
    for key in ('USERPROFILE','LOCALAPPDATA','APPDATA','ProgramFiles','ProgramData','SYSTEMROOT','WINDIR','TEMP'):
        value=os.environ.get(key)
        if value:
            protected=Path(value).resolve()
            if target==protected or (key in ('SYSTEMROOT','WINDIR') and target.is_relative_to(protected)):
                raise InstallError('protected_install_location')
    with target_lock(target):return _commit(stage,target,expected,fault)


def _commit(stage,target,expected,fault):
    recovery=recover(target)
    ledger=verify(stage,expected)
    if not owned(target):raise InstallError('target_not_owned')
    managed={LEDGER,LAUNCHER,'uninstall.exe','runtime','notices','_internal','ColorEngine.exe'}
    managed|={PurePosixPath(n).parts[0] for n in ledger['files']}
    managed={n.casefold() for n in managed}
    preserved=0
    old_tree=tree_digest(target) if target.exists() else None
    if target.exists():
        tree_files(target) # Refuse junctions/symlinks before copying personal extras.
        for item in target.iterdir():
            if item.name.casefold() not in managed:
                destination=stage/item.name
                if destination.exists():raise InstallError('personal_file_collision')
                try:
                    if item.is_dir():shutil.copytree(item,destination,symlinks=False)
                    else:shutil.copy2(item,destination)
                except OSError as error:raise InstallError('personal_copy_failed_old_unchanged',error) from None
                preserved+=1
    backup=target.parent/('.lf-previous-'+uuid.uuid4().hex)
    journal=journal_path(target)
    old_sha=sha(target/LAUNCHER) if (target/LAUNCHER).is_file() else None
    record={'product':PRODUCT,'target':target.name,'stage':stage.name,'backup':backup.name,
            'old_launcher_sha256':old_sha,'old_tree_sha256':old_tree,'manifest_sha256':expected}
    try:write_journal(journal,record)
    except OSError as error:raise InstallError('journal_prepare_failed_old_unchanged',error) from None
    moved=False
    try:
        if fault:fault('before_old_move')
        if target.exists() and tree_digest(target)!=old_tree:raise OSError('Old installation changed during staging')
        if target.exists():target.rename(backup);moved=True
        if fault:fault('after_old_move')
        stage.rename(target)
    except OSError as error:
        restored=None
        if moved and not target.exists():
            try:
                if tree_digest(backup)!=old_tree:raise OSError('Backup changed')
                backup.rename(target);restored=True
            except OSError:restored=False
        if restored is not False:journal.unlink()
        raise InstallError('directory_switch_failed',error,restored) from None
    # The old directory is deliberately retained: no recursive deletion of user data.
    retained=False
    try:journal.unlink()
    except OSError:retained=True # New package is committed; next attempt revalidates the journal.
    return {'ok':True,'phase':'committed','journal_retained':retained,'version':ledger['version'],'recovery':recovery,
            'personal_top_entries_preserved':preserved,'previous_directory':backup.name if moved else None,
            'data_store_modified':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--stage',required=True,type=Path);parser.add_argument('--target',required=True,type=Path);parser.add_argument('--manifest-sha256',required=True)
    args=parser.parse_args()
    try:result=commit(args.stage,args.target,args.manifest_sha256)
    except InstallError as error:print(json.dumps(error.report()));raise SystemExit(2)
    except Exception as error:
        print(json.dumps({'ok':False,'phase':'filesystem_or_manifest_error','errno':getattr(error,'errno',None),'winerror':getattr(error,'winerror',None)}));raise SystemExit(2)
    print(json.dumps(result))
