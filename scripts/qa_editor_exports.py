"""Prepare offline editor fixtures or measure an actual returned 8-bit PNG.

No editor is launched and no compatibility is inferred from bundle generation.
Use --help. Keep editor outputs and raw reports private until reviewed.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np
from PIL import Image
from packages.colour_core import engine, image_io


def parse_cube(text):
    size = None
    values = []
    for line in text.splitlines():
        row = line.strip()
        if not row or row.startswith('#') or row.startswith('TITLE '): continue
        if row.startswith('LUT_3D_SIZE '): size = int(row.split()[1]); continue
        if row.startswith('DOMAIN_MIN '):
            if row.split()[1:] != ['0.0', '0.0', '0.0']: raise ValueError('Unsupported LUT domain')
            continue
        if row.startswith('DOMAIN_MAX '):
            if row.split()[1:] != ['1.0', '1.0', '1.0']: raise ValueError('Unsupported LUT domain')
            continue
        values.append([float(x) for x in row.split()])
    array = np.asarray(values, dtype=np.float64)
    if size != 33 or array.shape != (33**3, 3) or not np.isfinite(array).all() or array.min() < 0 or array.max() > 1:
        raise ValueError('Expected finite 33-cubed RGB LUT in [0,1]')
    return array.reshape(33, 33, 33, 3)


def cube_samples(text, pixels):
    # Scalar oracle deliberately independent of engine.transform's vector indexing.
    table = parse_cube(text)
    samples = []
    for red, green, blue in np.asarray(pixels).reshape(-1, 3):
        p = np.array([blue, green, red], dtype=np.float64)*32
        low = np.floor(p).astype(int)
        high = np.minimum(low+1, 32)
        f = p-low
        a = table[low[0], low[1], low[2]]*(1-f[2])+table[low[0], low[1], high[2]]*f[2]
        b = table[low[0], high[1], low[2]]*(1-f[2])+table[low[0], high[1], high[2]]*f[2]
        c = table[high[0], low[1], low[2]]*(1-f[2])+table[high[0], low[1], high[2]]*f[2]
        d = table[high[0], high[1], low[2]]*(1-f[2])+table[high[0], high[1], high[2]]*f[2]
        samples.append((a*(1-f[1])+b*f[1])*(1-f[0])+(c*(1-f[1])+d*f[1])*f[0])
    return np.asarray(samples)


def compare(expected_payload, actual_payload):
    # Explicit ICC required for returned image: an untagged export must be investigated.
    for raw in (expected_payload, actual_payload):
        with Image.open(io.BytesIO(raw)) as image:
            if image.format != 'PNG' or not image.info.get('icc_profile'):
                raise ValueError('Use lossless PNG with embedded ICC; document editor color settings')
    expected, ea, _ = image_io.decode(expected_payload)
    actual, aa, _ = image_io.decode(actual_payload)
    if expected.shape != actual.shape or ea is not None or aa is not None:
        raise ValueError('Expected same RGB dimensions without alpha; do not resize or composite')
    difference = np.abs(actual-expected)*255
    delta = np.linalg.norm(engine.to_lab(actual)-engine.to_lab(expected), axis=-1)
    return {'schema': 'color-studio-editor-measurement-v1',
            'expected_sha256': hashlib.sha256(expected_payload).hexdigest(),
            'actual_sha256': hashlib.sha256(actual_payload).hexdigest(),
            'dimensions': [actual.shape[1], actual.shape[0]],
            'rgb_8bit_mean_absolute': float(difference.mean()), 'rgb_8bit_p95_absolute': float(np.percentile(difference, 95)),
            'rgb_8bit_max_absolute': float(difference.max()), 'delta_e76_d65_mean': float(delta.mean()),
            'delta_e76_d65_p95': float(np.percentile(delta, 95)),
            'compatibility_approved': False, 'scope': 'Pixel measurement only; requires actual editor/version/settings evidence and human interpretation'}


def prepare(image, recipe, destination):
    # Exclusive directory: never overwrite a person's photo or previous editor evidence.
    destination.mkdir(parents=True, exist_ok=False)
    original = image.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    rgb, alpha, _ = image_io.decode(original, max_side=1024)
    if alpha is not None: raise ValueError('Use an opaque authorized source for the editor pilot')
    recipe = engine.validate_recipe(recipe)
    color_recipe = recipe.model_copy(update={'look': engine.Look()})
    # A synthetic ramp exposes LUT ordering/interpolation; it is infrastructure evidence only.
    chart = np.zeros((256, 512, 3), np.float32)
    ramp = np.linspace(0, 1, 512, dtype=np.float32)
    chart[:64] = ramp[None, :, None]
    for channel in range(3): chart[64+channel*64:128+channel*64, :, channel] = ramp
    outputs = {'photo-source.png': image_io.encode(rgb),
               'photo-color-expected.png': image_io.encode(engine.render(rgb, color_recipe)),
               'photo-finish-excluded-from-lut.png': image_io.encode(engine.render(rgb, recipe)),
               'chart-synthetic-source.png': image_io.encode(chart),
               'chart-synthetic-color-expected.png': image_io.encode(engine.render(chart, color_recipe)),
               'identity.cube': engine.cube(engine.Recipe()).encode(),
               'color-only.cube': engine.cube(recipe).encode(),
               'recipe.json': (recipe.model_dump_json(indent=2)+'\n').encode()}
    rng = np.random.default_rng(1303)
    samples = np.vstack([rng.random((257, 3)), np.eye(3), np.zeros((1, 3)), np.ones((1, 3))]).astype(np.float32)
    error = float(np.max(np.abs(cube_samples(outputs['color-only.cube'].decode(), samples)-engine.transform(samples, recipe))))
    if error > 2e-6: raise ValueError('Serialized LUT differs from local color renderer')
    for name, raw in outputs.items(): (destination/name).write_bytes(raw)
    assert hashlib.sha256(image.read_bytes()).hexdigest() == digest
    manifest = {'schema': 'color-studio-editor-bundle-v1', 'source_sha256': digest,
                'scope': 'Real authorized photo plus explicitly synthetic chart; not a completed editor test',
                'working_domain': 'encoded-sRGB-D65', 'lut_size': 33, 'lut_scalar_oracle_max_error': error,
                'optical_effects_in_lut': False, 'original_unchanged': True,
                'editor_runs': {'photoshop': 'not_run', 'premiere': 'not_run', 'resolve': 'not_run'},
                'sha256': {name: hashlib.sha256(raw).hexdigest() for name, raw in outputs.items()}}
    (destination/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    bundle = sub.add_parser('prepare')
    bundle.add_argument('image', type=Path); bundle.add_argument('recipe', type=Path); bundle.add_argument('destination', type=Path)
    measure = sub.add_parser('compare')
    measure.add_argument('expected', type=Path); measure.add_argument('actual', type=Path); measure.add_argument('report', type=Path)
    args = parser.parse_args()
    if args.command == 'prepare':
        result = prepare(args.image, json.loads(args.recipe.read_bytes()), args.destination)
        print(json.dumps({'lut_scalar_oracle_max_error': result['lut_scalar_oracle_max_error'], 'editor_runs': result['editor_runs']}))
    else:
        if args.report.exists(): raise ValueError('Do not overwrite previous evidence')
        result = compare(args.expected.read_bytes(), args.actual.read_bytes())
        args.report.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        print(json.dumps(result))


if __name__ == '__main__': main()
