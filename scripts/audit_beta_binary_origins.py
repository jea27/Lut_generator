"""Reconcile PyInstaller PE inputs with the frozen tree, without publishing paths.

Byte provenance is distinct from redistribution rights. Fail closed on native
tool-cache inputs, missing sources and hashes that no longer match the build.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys


def inspect(toc_path, frozen):
    toc_path, frozen = Path(toc_path), Path(frozen)
    if toc_path.stat().st_size > 16*1024*1024: raise ValueError('Unexpectedly large build TOC')
    records = []
    def walk(item):
        if isinstance(item, (list, tuple)):
            if len(item) == 3 and all(isinstance(x, str) for x in item) and item[2] in ('BINARY', 'EXTENSION'):
                records.append(item)
            else:
                for child in item: walk(child)
    walk(ast.literal_eval(toc_path.read_text(encoding='utf-8')))
    rows, excluded = [], []
    for name, source, _ in records:
        if Path(name).suffix.lower() not in ('.dll', '.pyd'): continue
        target = (frozen/'_internal'/name).resolve()
        if not target.is_relative_to(frozen.resolve()): raise ValueError('Build destination escapes staging')
        if 'ffmpeg' in name.lower() and not target.exists():
            # Analysis TOC precedes the intentional still-photo spec exclusion.
            excluded.append({'file': name.replace('\\', '/'), 'reason': 'video_codec_intentionally_not_redistributed'})
            continue
        path = Path(source)
        normalized = path.as_posix().lower()
        # Tool-provided native libraries have no product redistribution decision.
        if '/dependencies/native/' in normalized or '/libheif/' in normalized:
            origin = 'external_tool_native_cache_requires_provenance'
        elif '/site-packages/' in normalized:
            origin = 'installed_wheel_subject_to_notices'
        elif '/windows kits/' in normalized and '/redist/' in normalized:
            origin = 'windows_sdk_redist_subject_to_terms'
        elif path.resolve().is_relative_to(Path(sys.base_prefix).resolve()):
            origin = 'installed_python_runtime_supply_chain_review_required'
        else:
            origin = 'unclassified_build_input'
        original_hash = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        target_hash = hashlib.sha256(target.read_bytes()).hexdigest() if target.is_file() else None
        rows.append({'file': name.replace('\\', '/'), 'origin_class': origin,
                     'source_sha256': original_hash, 'frozen_sha256': target_hash,
                     'byte_identical': original_hash is not None and original_hash == target_hash})
    unsafe = [row['file'] for row in rows if not row['byte_identical'] or row['origin_class'] in
              ('external_tool_native_cache_requires_provenance', 'unclassified_build_input')]
    if not rows: raise ValueError('No PE records found; not an audited binary build')
    return {'schema': 'color-studio-build-origin-audit-v1', 'files': rows, 'excluded_not_shipped': excluded,
            'blocked_files': unsafe, 'build_origin_gate_passed': not unsafe,
            'redistribution_approved': False,
            'scope': 'PyInstaller PE build inputs only; hashes do not grant license rights. CPython/wheels/Microsoft terms still require owner review.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('toc', type=Path); parser.add_argument('frozen', type=Path); parser.add_argument('report', type=Path)
    args = parser.parse_args()
    report = inspect(args.toc, args.frozen)
    args.report.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'pe_files': len(report['files']), 'blocked_files': len(report['blocked_files']),
                      'build_origin_gate_passed': report['build_origin_gate_passed']}))
    return 0 if report['build_origin_gate_passed'] else 2


if __name__ == '__main__': raise SystemExit(main())
