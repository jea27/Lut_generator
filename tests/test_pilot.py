import hashlib
import io
import unittest
from scripts.prepare_pilot import FILES, inspect_bytes

try:
    from PIL import Image
except ImportError:
    Image = None


class PilotTests(unittest.TestCase):
    def test_allowlist_is_bounded(self):
        self.assertEqual(sum(len(v) for v in FILES.values()), 4)
        self.assertEqual(sum(size for v in FILES.values() for size, _ in v.values()), 34773100)

    @unittest.skipUnless(Image, "Optional Pillow unavailable; local image tests required")
    def test_reject_modified_download(self):
        with self.assertRaises(ValueError):
            inspect_bytes(b"bad", 3, "0" * 32)

    @unittest.skipUnless(Image, "Optional Pillow unavailable; local image tests required")
    def test_decode_and_hash_synthetic_fixture(self):
        stream = io.BytesIO()
        Image.new("RGB", (12, 8), "red").save(stream, format="JPEG")
        data = stream.getvalue()
        record = inspect_bytes(data, len(data), hashlib.md5(data).hexdigest())
        self.assertEqual((record["width"], record["height"]), (12, 8))
        self.assertEqual(record["sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(record["color_review"], "pending")
