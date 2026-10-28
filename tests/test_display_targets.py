"""Check display build isolation without installing the ESP32 toolchain."""

import os
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).absolute().parents[1]


class DisplayTargetsTest(unittest.TestCase):
    def dispatch(self, target):
        result = subprocess.run(
            [os.environ.get("MAKE", "make"), "--no-print-directory", "-n",
             "MAKE=echo", target],
            cwd=ROOT, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_display_targets_use_separate_builds_and_board_selection(self):
        pocket = self.dispatch("s3-lcd")
        lilygo = self.dispatch("s3-tdongle")
        self.assertIn("LCD=1", pocket)
        self.assertIn('/build/lcd"', pocket)
        self.assertNotIn("LCD_TDONGLE", pocket)
        self.assertIn("LCD=1", lilygo)
        self.assertIn("LCD_TDONGLE=1", lilygo)
        self.assertIn('/build/tdongle-s3"', lilygo)
        self.assertIn("esp32-arduino.tdongle-s3.merged.bin", lilygo)
        self.assertNotIn('/build/lcd"', lilygo)


if __name__ == "__main__":
    unittest.main()
