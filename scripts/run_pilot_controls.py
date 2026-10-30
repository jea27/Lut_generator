"""Real-photo infrastructure checks only. Never runs products or populates P0 runs."""
import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    from scripts.benchmark_metrics import read_image, measure, repeatability, timing_summary
except ModuleNotFoundError:
    from benchmark_metrics import read_image, measure, repeatability, timing_summary


def load_assets(manifest, media_root):
    payload = Path(manifest).read_bytes()
    data = json.loads(payload)
    if data.get('version') != 1 or data.get('license') != 'CC0-1.0':
        raise ValueError('Expected the reviewed CC0 pilot manifest')
    root = Path(media_root).resolve()
    assets = []
    for pair in data.get('pairs', []):
        capture = pair.get('capture')
        if capture not in ('DSC_0106', 'DSC_0181'):
            raise ValueError('Unexpected capture')
        for asset in pair.get('assets', []):
            variant = asset.get('variant')
            if variant not in ('jpg_plain', 'jpg_pretty'):
                raise ValueError('Unexpected variant')
            name = f'{capture}-{variant}.jpg'
            if asset.get('local_path') != '.research-media/polyhaven-rural/' + name:
                raise ValueError('Unexpected manifest path')
            path = (root / name).resolve()
            if path.parent != root or (root / name).is_symlink():
                raise ValueError('Media must stay within supplied root')
            if path.stat().st_size > 100 * 1024 * 1024:
                raise ValueError('Media size exceeds pilot limit')
            content = path.read_bytes()
            if len(content) != asset.get('bytes') or hashlib.sha256(content).hexdigest() != asset.get('sha256'):
                raise ValueError('Pilot hash or length mismatch')
            assets.append((name, path, asset['sha256']))
    expected = {f'{c}-{v}.jpg' for c in ('DSC_0106', 'DSC_0181') for v in ('jpg_plain', 'jpg_pretty')}
    if len(assets) != 4 or {a[0] for a in assets} != expected:
        raise ValueError('Need exactly the four unique pilot assets')
    return assets, hashlib.sha256(payload).hexdigest()


def run(manifest, media_root, repeats=3):
    if type(repeats) is not int or not 2 <= repeats <= 10:
        raise ValueError('Use 2-10 observed repetitions')
    import numpy as np
    import PIL
    assets, manifest_hash = load_assets(manifest, media_root)
    records = []
    for name, path, digest in assets:
        arrays, durations, sizes = [], [], []
        for _ in range(repeats):
            started = time.perf_counter()
            image, metadata = read_image(path, None)
            if metadata['sha256'] != digest:
                raise ValueError('Photo changed during the experiment')
            sizes.append(metadata['oriented_size'])
            image.thumbnail((512, 512), PIL.Image.Resampling.LANCZOS)
            arrays.append(np.array(image, dtype=np.float64) / 255.)
            image.close()
            durations.append(time.perf_counter() - started)
        started = time.perf_counter()
        identity = measure(arrays[0], arrays[0])
        metric_seconds = time.perf_counter() - started
        records.append({'asset': name, 'sha256': digest, 'profile': metadata['profile'],
                        'oriented_size': sizes[0], 'measurement_size': list(arrays[0].shape[:2][::-1]),
                        'identity_control': identity, 'repeat_decode_control': repeatability(arrays),
                        'preprocess_wall_seconds_observed': durations,
                        'preprocess_first_observed_seconds': durations[0],
                        'preprocess_subsequent_summary': timing_summary(durations[1:]),
                        'identity_metric_wall_seconds': metric_seconds,
                        'model_inference_seconds': None})
    dimensions = {r['asset']: r['oriented_size'] for r in records}
    guards = []
    for capture in ('DSC_0106', 'DSC_0181'):
        different = dimensions[capture + '-jpg_plain.jpg'] != dimensions[capture + '-jpg_pretty.jpg']
        guards.append({'capture': capture, 'dimensions_equal': not different,
                       'pixel_fidelity_allowed': False,
                       'reason': 'reject_before_resize' if different else 'alignment_and_target_not_reviewed'})
    return {'version': 1, 'evidence_type': 'real_photo_infrastructure_control',
            'research_validated': False, 'product_runs': 0, 'synthetic_samples': 0,
            'measured_utc': datetime.now(timezone.utc).isoformat(),
            'pilot_manifest_sha256': manifest_hash, 'numpy': np.__version__, 'pillow': PIL.__version__,
            'scope': 'ICC decode/EXIF/Lanczos max-side512 and identity metrics; no grading model',
            'timing_caveat': 'First observed is not a cold-cache guarantee; subsequent samples are not model latency',
            'assets': records, 'pair_guards': guards}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--media-root', required=True)
    parser.add_argument('--report', required=True)
    parser.add_argument('--repeats', type=int, default=3)
    args = parser.parse_args()
    if Path(args.report).exists():
        parser.error('Existing evidence will not be overwritten')
    report = run(args.manifest, args.media_root, args.repeats)
    with Path(args.report).open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({'real_photos_checked': len(report['assets']), 'product_runs': 0,
                      'research_validated': False}))


if __name__ == '__main__':
    main()
