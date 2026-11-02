"""Atomic private records: a failed write never truncates the previous version."""
import json
import os
import stat
import tempfile
from pathlib import Path

_WINDOWS = os.name == 'nt'


def private_path(root, *parts):
    """Refuse traversal and linked children in the application's private store.

    Defence against accidental/tampered paths, not a sandbox against an OS user
    who can replace directories between a check and a filesystem operation.
    """
    root = Path(root)
    candidate = root.joinpath(*parts)
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise ValueError('Private storage path is outside its allowed directory')
    for parent in (candidate, *candidate.parents):
        if parent.is_symlink() or os.path.isjunction(parent):
            raise ValueError('Linked private storage paths are not supported')
        if parent == root:
            break
    return candidate


def read_record(root, *parts):
    path = private_path(root, *parts)
    if path.stat().st_size > 64 * 1024:
        raise ValueError('Private record exceeds safe size limit')
    return json.loads(path.read_bytes())


def _is_owned_temporary(path, identity):
    if identity is None or not identity[1]:
        return False
    try:
        info = path.lstat()
    except FileNotFoundError:
        return False
    return (stat.S_ISREG(info.st_mode)
            and not getattr(info, 'st_file_attributes', 0) & 0x400
            and (info.st_dev, info.st_ino) == identity)


def remove_owned_temporary(path, identity):
    """Never delete a file merely because it reused our temporary filename.

    Identity checks reduce accidental cleanup risk. They are not an OS sandbox
    against another process replacing paths between checks and operations.
    """
    path = Path(path)
    if _is_owned_temporary(path, identity):
        path.unlink()


def atomic_json(path, value, *, overwrite=True):
    payload = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False).encode('utf-8')
    atomic_bytes(path, payload, overwrite=overwrite)


def atomic_bytes(path, payload, *, overwrite=True):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix='.pending-', dir=path.parent)
    temporary = Path(temporary)
    identity = None
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            info = os.fstat(stream.fileno())
            identity = (info.st_dev, info.st_ino)
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        if not _is_owned_temporary(temporary, identity):
            raise OSError('Private temporary changed; previous content preserved')
        if overwrite:
            os.replace(temporary, path)
        elif _WINDOWS:
            # Windows rename refuses an existing destination; no exists()/write race.
            os.rename(temporary, path)
        else:
            # POSIX rename overwrites; link publishes only if the name is absent.
            # Both paths share a directory/filesystem. No unsafe fallback on failure.
            os.link(temporary, path, follow_symlinks=False)
    finally:
        remove_owned_temporary(temporary, identity)
