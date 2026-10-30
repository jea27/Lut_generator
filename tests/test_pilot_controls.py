import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from scripts.run_pilot_controls import load_assets, run


def synthetic_fixture(root):
    # Hash-only fixture, not an actual photo or research evidence.
    data = {'version': 1, 'license': 'CC0-1.0', 'pairs': []}
    for capture in ('DSC_0106', 'DSC_0181'):
        assets = []
        for variant in ('jpg_plain', 'jpg_pretty'):
            name = f'{capture}-{variant}.jpg'; payload = name.encode('ascii')
            (root / name).write_bytes(payload)
            assets.append({'variant': variant, 'local_path': '.research-media/polyhaven-rural/' + name,
                           'bytes': len(payload), 'sha256': hashlib.sha256(payload).hexdigest()})
        data['pairs'].append({'capture': capture, 'assets': assets})
    manifest = root / 'synthetic-manifest.json'
    manifest.write_text(json.dumps(data), encoding='utf-8')
    return manifest, data


class PilotControlTests(unittest.TestCase):
    def test_verified_inventory_has_exactly_four_unique_names(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); manifest, _ = synthetic_fixture(root)
            assets, digest = load_assets(manifest, root)
            self.assertEqual(len(assets), 4)
            self.assertEqual(len(digest), 64)

    def test_rejects_modified_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); manifest, _ = synthetic_fixture(root)
            (root / 'DSC_0106-jpg_plain.jpg').write_bytes(b'corrupted')
            with self.assertRaises(ValueError):
                load_assets(manifest, root)

    def test_rejects_path_missing_duplicate_and_license(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); manifest, data = synthetic_fixture(root)
            for mutation in (lambda d: d['pairs'][0]['assets'][0].update(local_path='../private.jpg'),
                             lambda d: d['pairs'].pop(),
                             lambda d: d['pairs'].append(d['pairs'][0]),
                             lambda d: d.update(license='unknown')):
                invalid = copy.deepcopy(data); mutation(invalid)
                manifest.write_text(json.dumps(invalid), encoding='utf-8')
                with self.assertRaises(ValueError):
                    load_assets(manifest, root)

    def test_no_repeats_means_no_measurement(self):
        for repetitions in (0, 1, True, 11):
            with self.assertRaises(ValueError):
                run('unused', 'unused', repetitions)
