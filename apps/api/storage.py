"""Atomic private records: a failed write never truncates the previous version."""
import json
import os
import tempfile
from pathlib import Path


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
