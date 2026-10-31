"""Atomic private records: a failed write never truncates the previous version."""
import json
import os
import tempfile
from pathlib import Path


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


def atomic_json(path, value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    descriptor, temporary=tempfile.mkstemp(prefix='.pending-',dir=path.parent)
    try:
        with os.fdopen(descriptor,'w',encoding='utf-8') as stream:
            json.dump(value,stream,ensure_ascii=False,indent=2,allow_nan=False)
            stream.flush();os.fsync(stream.fileno())
        os.replace(temporary,path)
    finally:
        if os.path.exists(temporary):os.unlink(temporary)


def atomic_bytes(path, payload):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    descriptor,temporary=tempfile.mkstemp(prefix='.pending-',dir=path.parent)
    try:
        with os.fdopen(descriptor,'wb') as stream:
            stream.write(payload);stream.flush();os.fsync(stream.fileno())
        os.replace(temporary,path)
    finally:
        if os.path.exists(temporary):os.unlink(temporary)
