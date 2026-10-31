"""Profile the real still-image pipeline locally; never publish source paths/photos.

No runtime algorithm changes. Optional tile experiments are measurement-only.
The output is engineering evidence, not human quality acceptance.
"""
import argparse
import cProfile
import hashlib
import io
import json
import os
from pathlib import Path
import pstats
import statistics
import sys
import time
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import cv2
import numpy as np
import PIL
from PIL import Image
from packages.colour_core import engine, image_io, look


def measure(payload, recipe, tile_rows=128, profile=False):
    timings = {}
    transform, finish = engine.transform, look.apply
    def color(*args, **kwargs):
        start = time.perf_counter()
        result = transform(*args, **kwargs)
        timings['color_lut_seconds'] = timings.get('color_lut_seconds', 0) + time.perf_counter()-start
        return result
    def effects(*args, **kwargs):
        start = time.perf_counter()
        result = finish(*args, **kwargs, tile_rows=tile_rows)
        timings['finishing_seconds'] = time.perf_counter()-start
        return result
    total = time.perf_counter()
    start = time.perf_counter()
    rgb, alpha, _ = image_io.decode(payload)
    timings['decode_icc_seconds'] = time.perf_counter()-start
    prof = cProfile.Profile()
    if profile: prof.enable()
    with patch.object(engine, 'transform', color), patch.object(look, 'apply', effects):
        start = time.perf_counter()
        output = engine.render(rgb, recipe, alpha=alpha)
        timings['render_seconds'] = time.perf_counter()-start
    if profile: prof.disable()
    start = time.perf_counter()
    encoded = image_io.encode(output, alpha)
    timings['quantize_png_seconds'] = time.perf_counter()-start
    timings['pipeline_seconds'] = time.perf_counter()-total
    with Image.open(io.BytesIO(encoded)) as decoded:
        assert decoded.size == (rgb.shape[1], rgb.shape[0]) and decoded.info.get('icc_profile')
        pixel_hash = hashlib.sha256(decoded.tobytes()).hexdigest()
    top = []
    if profile:
        stats = pstats.Stats(prof)
        for (filename, line, function), values in sorted(stats.stats.items(), key=lambda item: item[1][3], reverse=True)[:18]:
            # basename/function only: co_filename may contain a private build path.
            top.append({'module': Path(filename).name, 'function': function, 'calls': values[1],
                        'self_seconds': values[2], 'cumulative_seconds': values[3]})
    return {'tile_rows': tile_rows, 'timings': timings, 'png_pixels_sha256': pixel_hash,
            'dimensions': [rgb.shape[1], rgb.shape[0]], 'profile': top}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    parser.add_argument('recipe', type=Path)
    parser.add_argument('report', type=Path)
    parser.add_argument('--repeats', type=int, default=3, choices=range(1, 6))
    parser.add_argument('--experiment-tiles', type=int, nargs='*', default=[], choices=[256, 512])
    args = parser.parse_args()
    raw = args.image.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    recipe = engine.validate_recipe(json.loads(args.recipe.read_bytes()))
    # Warm only the LUT cache; full-image work is still measured on every run.
    engine.lut_grid(recipe.model_dump_json())
    runs = [measure(raw, recipe, profile=(i == 0)) for i in range(args.repeats)]
    experiments = [measure(raw, recipe, tile_rows=tile) for tile in args.experiment_tiles]
    baseline = runs[0]['png_pixels_sha256']
    for row in experiments:
        row['identical_png_pixels_to_baseline'] = row['png_pixels_sha256'] == baseline
    assert hashlib.sha256(args.image.read_bytes()).hexdigest() == digest
    report = {'schema': 'color-studio-export-profile-v1', 'scope': 'Actual local source pipeline, not clean Windows or aesthetic validation',
              'input_sha256': digest, 'recipe': recipe.model_dump(), 'original_unchanged': True,
              'runtime': {'python': sys.version.split()[0], 'numpy': np.__version__, 'opencv': cv2.__version__,
                          'pillow': PIL.__version__, 'opencv_threads': cv2.getNumThreads(), 'logical_cpus': os.cpu_count()},
              'runs': runs, 'median_seconds': {key: statistics.median(row['timings'][key] for row in runs) for key in runs[0]['timings']},
              'repeat_pixels_equal': all(row['png_pixels_sha256'] == baseline for row in runs),
              'tile_experiments_not_shipped': experiments, 'human_quality_approved': False}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'median_seconds': report['median_seconds'], 'repeat_pixels_equal': report['repeat_pixels_equal'],
                      'tile_experiments': [{'rows': row['tile_rows'], 'seconds': row['timings']['pipeline_seconds'],
                                             'pixels_equal': row['identical_png_pixels_to_baseline']} for row in experiments]}))


if __name__ == '__main__': main()
