"""Package only three public instrument files; never copy research data/media."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = {"form.html": "index.html", "form.js": "form.js", "form.css": "form.css"}


def prepare(root=ROOT):
    source = Path(root) / "research"
    target = Path(root) / "site/investigacion"
    if source.is_symlink() or target.is_symlink() or target.parent.is_symlink():
        raise ValueError("Public packaging must not follow directory symlinks")
    # Fail closed rather than accidentally uploading leftover files.
    if target.exists() and any(p.name not in PUBLIC_FILES.values() or not p.is_file()
                               or p.is_symlink() for p in target.iterdir()):
        raise ValueError("Unexpected file in public instrument directory")
    for name in PUBLIC_FILES:
        if not (source / name).is_file() or (source / name).is_symlink():
            raise ValueError("Missing or linked public instrument source")
    target.mkdir(parents=True, exist_ok=True)
    for name, destination in PUBLIC_FILES.items():
        shutil.copyfile(source / name, target / destination)
    return target


if __name__ == "__main__":
    prepare()
    print("Prepared site/investigacion: HTML, JavaScript, CSS only; no response data")
