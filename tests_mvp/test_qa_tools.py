import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import numpy as np
from PIL import Image
from packages.colour_core import engine, image_io
from scripts import qa_editor_exports as editors
from scripts.profile_export import measure
from scripts.audit_beta_binary_origins import inspect as inspect_origins


class ExportQATests(unittest.TestCase):
    def test_binary_origins_gate_rejects_tool_cache_and_modified_payload(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); source = root/'dependencies/native/vendor/runtime.dll'
            source.parent.mkdir(parents=True); source.write_bytes(b'fixture')
            frozen = root/'frozen'; (frozen/'_internal').mkdir(parents=True)
            (frozen/'_internal/runtime.dll').write_bytes(b'fixture')
            toc = root/'Analysis.toc'; toc.write_text(repr([('runtime.dll',str(source),'BINARY')]))
            result = inspect_origins(toc, frozen)
            self.assertFalse(result['build_origin_gate_passed'])
            self.assertEqual(result['blocked_files'], ['runtime.dll'])
            self.assertNotIn(str(root), json.dumps(result))
            source = root/'site-packages/vendor/runtime.dll'; source.parent.mkdir(parents=True); source.write_bytes(b'fixture')
            toc.write_text(repr([('runtime.dll',str(source),'EXTENSION')]))
            result = inspect_origins(toc, frozen)
            self.assertTrue(result['build_origin_gate_passed'])
            self.assertFalse(result['redistribution_approved'])
            (frozen/'_internal/runtime.dll').write_bytes(b'tampered')
            self.assertFalse(inspect_origins(toc, frozen)['build_origin_gate_passed'])

    def test_binary_origins_cannot_escape_frozen_tree(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); frozen = root/'frozen'; frozen.mkdir()
            toc = root/'Analysis.toc'; toc.write_text(repr([('../../private.dll',str(root/'source.dll'),'BINARY')]))
            with self.assertRaises(ValueError): inspect_origins(toc, frozen)

    def test_returned_editor_pixels_require_dimensions_icc_and_never_approve(self):
        source = np.full((5, 8, 3), .5, np.float32)
        raw = image_io.encode(source)
        result = editors.compare(raw, raw)
        self.assertEqual(result['rgb_8bit_max_absolute'], 0)
        self.assertFalse(result['compatibility_approved'])
        with self.assertRaises(ValueError): editors.compare(raw, image_io.encode(source[:3]))
        stream = io.BytesIO(); Image.new('RGB', (8, 5)).save(stream, format='PNG')
        with self.assertRaises(ValueError): editors.compare(raw, stream.getvalue())

    def test_serialized_cube_order_and_endpoints_against_independent_oracle(self):
        samples = np.array([[1,0,0], [0,1,0], [0,0,1], [.1,.7,.3], [1,1,1], [0,0,0]], np.float32)
        recipe = engine.Recipe(offset=[9, -3, 4], exposure=.4, saturation=1.2)
        np.testing.assert_allclose(editors.cube_samples(engine.cube(recipe), samples), engine.transform(samples, recipe), atol=2e-6)
        with self.assertRaises(ValueError): editors.parse_cube(engine.cube(recipe).replace('LUT_3D_SIZE 33', 'LUT_3D_SIZE 32'))

    def test_profile_preserves_export_and_reports_actual_phases(self):
        source = np.random.default_rng(3).random((13, 19, 3), dtype=np.float32)
        raw = image_io.encode(source)
        recipe = engine.Recipe(look=engine.Look(enabled=True, glow=.3, diffusion=.2))
        a = measure(raw, recipe, profile=True)
        b = measure(raw, recipe, tile_rows=256)
        self.assertEqual(a['png_pixels_sha256'], b['png_pixels_sha256'])
        self.assertGreater(a['timings']['finishing_seconds'], 0)
        self.assertGreater(a['timings']['pipeline_seconds'], a['timings']['render_seconds'])


@unittest.skipUnless(os.name == 'nt', 'Windows PowerShell verifier')
class WindowsPreservationTests(unittest.TestCase):
    def invoke(self, *args):
        script = Path(__file__).resolve().parents[1]/'scripts/qa_windows_preservation.ps1'
        # Python launched from pwsh can inherit PS7-only module paths. Let PS5.1
        # initialize its own defaults in this child, without changing the system.
        env = {key: value for key, value in os.environ.items() if key.lower() != 'psmodulepath'}
        return subprocess.run(['powershell.exe', '-NoProfile', '-File', str(script), *map(str, args)], capture_output=True, env=env)

    def test_changed_missing_and_extra_files_are_distinguished(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); data = root/'data'; data.mkdir()
            (data/'preset.json').write_text('{}'); (data/'original.png').write_bytes(b'fixture-not-real-photo')
            baseline = root/'private.json'
            self.assertEqual(self.invoke('-Mode','Snapshot','-DataDirectory',data,'-Baseline',baseline).returncode, 0)
            (data/'new.json').write_text('new')
            report = root/'ok.json'
            self.assertEqual(self.invoke('-Mode','Verify','-DataDirectory',data,'-Baseline',baseline,'-Report',report).returncode, 0)
            self.assertTrue(json.loads(report.read_text(encoding='utf-8-sig'))['passed'])
            (data/'preset.json').write_text('changed'); (data/'original.png').unlink()
            report = root/'failed.json'
            self.assertEqual(self.invoke('-Mode','Verify','-DataDirectory',data,'-Baseline',baseline,'-Report',report).returncode, 2)
            result = json.loads(report.read_text(encoding='utf-8-sig'))
            self.assertEqual((result['changed'], result['missing']), (1,1))
            self.assertNotIn('preset', report.read_text())

    def test_untrusted_baseline_cannot_escape_data_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); data = root/'data'; data.mkdir()
            baseline = root/'private.json'; report = root/'report.json'
            baseline.write_text(json.dumps({'schema':'color-studio-private-data-baseline-v1','files':[{'relative':'../other.txt','sha256':'0'*64}]}))
            self.assertNotEqual(self.invoke('-Mode','Verify','-DataDirectory',data,'-Baseline',baseline,'-Report',report).returncode, 0)
            self.assertFalse(report.exists())
