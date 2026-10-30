"""Audit dataset bookkeeping/integrity, never implement image/color processing."""
import argparse
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'data' / 'p0' / 'dataset.json'
CHALLENGES = {'skin', 'shadows', 'highlights', 'mixed-light', 'night', 'backlight', 'saturation'}
SCENES = {'portrait', 'landscape', 'interior', 'street', 'still-life'}
ASSET_PATH = re.compile(r'P0-\d{3}/(?:source|reference)\.(?:jpg|jpeg|png)')


def validate(data, media_root=None):
    errors, pending = [], []
    report = {'schema_valid': False, 'ready_pairs': 0, 'verified_assets': 0,
              'required_pairs': 20, 'gate_ready': False, 'errors': errors, 'pending': pending}
    if not isinstance(data, dict) or type(data.get('version')) is not int or data.get('version') != 1 or not isinstance(data.get('pairs'), list):
        errors.append('manifest: expected version 1 and pairs list')
        return report
    pairs = data['pairs']
    ids = [p.get('id') for p in pairs if isinstance(p, dict)]
    if len(pairs) != 20 or not all(isinstance(x, str) for x in ids) or set(ids) != {f'P0-{i:03}' for i in range(1, 21)}:
        errors.append('manifest: expected 20 unique IDs P0-001..P0-020')
    observed_challenges, sources = set(), set()
    base = pathlib.Path(media_root).resolve() if media_root else None
    for index, pair in enumerate(pairs, 1):
        if not isinstance(pair, dict):
            errors.append('pair: expected object')
            continue
        raw_id = pair.get('id')
        pid = raw_id if isinstance(raw_id, str) and re.fullmatch(r'P0-\d{3}', raw_id) else f'pair-{index}'
        start_errors = len(errors)
        pair_pending = False
        if not isinstance(pair.get('scene'), str) or pair.get('scene') not in SCENES:
            errors.append(f'{pid}: invalid scene')
        challenges = pair.get('challenges')
        if not isinstance(challenges, list) or not challenges or any(not isinstance(x, str) or x not in CHALLENGES for x in challenges):
            errors.append(f'{pid}: invalid challenges')
        else:
            observed_challenges.update(challenges)
        if not isinstance(pair.get('state'), str) or pair.get('state') not in {'planned', 'ready'}:
            errors.append(f'{pid}: invalid state')
        if pair.get('state') != 'ready':
            pending.append(f'{pid}: pair not declared ready')
            pair_pending = True
        for role in ('source', 'reference'):
            label = f'{pid}/{role}'
            asset = pair.get(role)
            if asset is None:
                pending.append(f'{label}: media/rights missing')
                pair_pending = True
                continue
            if not isinstance(asset, dict):
                errors.append(f'{label}: expected object or null')
                continue
            path = asset.get('path', '')
            if not isinstance(path, str) or not ASSET_PATH.fullmatch(path) or not path.startswith(f'{pid}/{role}.'):
                errors.append(f'{label}: use anonymous relative slot path, no traversal or drive paths')
                continue
            digest = asset.get('sha256', '')
            if not isinstance(digest, str) or not re.fullmatch(r'[a-f0-9]{64}', digest):
                errors.append(f'{label}: invalid SHA256')
                continue
            if role == 'source':
                if digest in sources:
                    errors.append(f'{label}: duplicate source content')
                sources.add(digest)
            rights = asset.get('rights')
            if not isinstance(rights, dict) or rights.get('status') != 'cleared' or not re.fullmatch(
                    r'RIGHTS-[A-Z0-9-]+', str(rights.get('record_id', ''))) or not rights.get('basis'):
                pending.append(f'{label}: rights review/evidence missing')
                pair_pending = True
            if asset.get('color_space') != 'sRGB' or not re.fullmatch(
                    r'COLOR-[A-Z0-9-]+', str(asset.get('color_record_id', ''))):
                pending.append(f'{label}: documented sRGB preparation missing')
                pair_pending = True
            if base:
                candidate = (base / path).resolve()
                if not candidate.is_relative_to(base):
                    errors.append(f'{label}: resolved path leaves media root')
                    continue
                try:
                    if not candidate.is_file() or not 0 < candidate.stat().st_size <= 100 * 1024 * 1024:
                        errors.append(f'{label}: file missing, empty or over 100 MiB')
                        continue
                    hasher = hashlib.sha256()
                    with candidate.open('rb') as stream:
                        signature = stream.read(8)
                        hasher.update(signature)
                        for block in iter(lambda: stream.read(1024 * 1024), b''):
                            hasher.update(block)
                    expected = b'\x89PNG\r\n\x1a\n' if candidate.suffix == '.png' else b'\xff\xd8\xff'
                    if not signature.startswith(expected) or hasher.hexdigest() != digest:
                        errors.append(f'{label}: signature or SHA256 mismatch')
                    else:
                        report['verified_assets'] += 1
                except OSError:
                    errors.append(f'{label}: cannot read media file')
            else:
                pair_pending = True
        a, b = pair.get('source'), pair.get('reference')
        if isinstance(a, dict) and isinstance(b, dict) and a.get('sha256') == b.get('sha256'):
            errors.append(f'{pid}: source and reference must differ')
        if not pair_pending and len(errors) == start_errors:
            report['ready_pairs'] += 1
    if not CHALLENGES.issubset(observed_challenges):
        errors.append('manifest: required planned scene challenges not covered')
    review = data.get('coverage_review')
    if not isinstance(review, dict) or review.get('status') != 'reviewed' or not re.fullmatch(
            r'REVIEW-[A-Z0-9-]+', str(review.get('record_id', ''))):
        pending.append('manifest: human diversity/coverage review missing')
    if not base:
        pending.append('manifest: local files not checked; pass --media-root explicitly')
    report['schema_valid'] = not errors
    report['gate_ready'] = not errors and not pending and report['ready_pairs'] == 20 and report['verified_assets'] == 40
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=pathlib.Path, nargs='?', default=DEFAULT)
    parser.add_argument('--media-root', type=pathlib.Path)
    parser.add_argument('--ready', action='store_true', help='Exit 2 when valid bookkeeping is still incomplete')
    args = parser.parse_args(argv)
    try:
        report = validate(json.loads(args.manifest.read_text('utf-8')), args.media_root)
    except (OSError, ValueError, TypeError):
        print(json.dumps({'schema_valid': False, 'errors': ['cannot read valid manifest JSON']}))
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if not report['schema_valid'] else 2 if args.ready and not report['gate_ready'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
