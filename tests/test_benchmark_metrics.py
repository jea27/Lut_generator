import unittest
import io
import tempfile
from pathlib import Path
from scripts.benchmark_metrics import timing_summary

try:
    import numpy as np
except ImportError:
    np = None


class TimingTests(unittest.TestCase):
    def test_actual_sample_statistics(self):
        self.assertEqual(timing_summary([4, 1, 2, 3])["median_seconds"], 2.5)
        self.assertEqual(timing_summary([4, 1, 2, 3])["p95_nearest_rank_seconds"], 4)

    def test_missing_invalid_are_not_zero_measurements(self):
        for sample in ([], [True], [-1], [float("nan")], [float("inf")]):
            with self.subTest(sample=sample), self.assertRaises(ValueError):
                timing_summary(sample)


@unittest.skipUnless(np is not None, "Optional NumPy absent; local metric tests required")
class MetricTests(unittest.TestCase):
    def test_identity_and_finite_json_psnr(self):
        from scripts.benchmark_metrics import measure
        a = np.random.default_rng(42).random((16, 16, 3))
        result = measure(a, a)
        self.assertEqual(result["delta_e76_d65_mean"], 0)
        self.assertIsNone(result["psnr_db"])
        self.assertTrue(result["psnr_infinite"])
        self.assertAlmostEqual(result["ssim_uniform7_luma_valid_samplecov"], 1)
        self.assertAlmostEqual(result["gradient_correlation"], 1)

    def test_known_srgb_primary_d65(self):
        from scripts.benchmark_metrics import lab_d65
        red = np.zeros((7, 7, 3)); red[..., 0] = 1
        np.testing.assert_allclose(lab_d65(red)[0, 0], [53.2408, 80.0925, 67.2032], atol=.001)
        white = lab_d65(np.ones((7, 7, 3)))[0, 0]
        np.testing.assert_allclose(white, [100, 0, 0], atol=.001)

    def test_mismatch_nan_and_gamut_fail_closed(self):
        from scripts.benchmark_metrics import measure
        a = np.zeros((8, 8, 3))
        for b in (np.zeros((9, 8, 3)), np.full_like(a, np.nan), np.full_like(a, 1.01)):
            with self.assertRaises(ValueError):
                measure(a, b)

    def test_color_shift_and_flat_detail_undefined(self):
        from scripts.benchmark_metrics import measure
        a = np.zeros((8, 8, 3)); b = np.full_like(a, .5)
        result = measure(a, b)
        self.assertGreater(result["delta_e76_d65_mean"], 50)
        self.assertAlmostEqual(result["psnr_db"], 6.0205999, places=6)
        self.assertIsNone(result["gradient_correlation"])

    def test_repeatability_does_not_require_style_similarity(self):
        from scripts.benchmark_metrics import repeatability
        a = np.zeros((8, 8, 3))
        self.assertEqual(repeatability([a, a])["max_abs_encoded_srgb_from_first"], 0)
        self.assertEqual(repeatability([a, np.ones_like(a)])["max_abs_encoded_srgb_from_first"], 1)
        with self.assertRaises(ValueError):
            repeatability([a])

    def test_untagged_image_requires_record_and_preserves_source(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Optional Pillow unavailable")
        from scripts.benchmark_metrics import read_image
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.png"
            Image.new("RGB", (10, 10), "red").save(path)
            original = path.read_bytes()
            with self.assertRaises(ValueError):
                read_image(path, None)
            image, record = read_image(path, "COLOR-SYNTHETIC")
            self.assertEqual(image.size, (10, 10))
            self.assertIn("COLOR-SYNTHETIC", record["profile"])
            self.assertEqual(path.read_bytes(), original)
