
"""Tests for the QR code prototype."""

import tempfile
import unittest
from pathlib import Path

from PIL import Image

from qr_prototype import generate_qr


class TestQRPrototype(unittest.TestCase):

    def test_generates_png(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "location.png"

            result = generate_qr(
                "https://example.com/locations/123",
                output
            )

            self.assertEqual(result, output)

            with Image.open(output) as image:
                self.assertEqual(image.format, "PNG")
                self.assertGreater(image.width, 0)
                self.assertEqual(image.width, image.height)

    def test_rejects_relative_url(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "invalid.png"

            with self.assertRaises(ValueError):
                generate_qr("/locations/123", output)


if __name__ == "__main__":
    unittest.main()
