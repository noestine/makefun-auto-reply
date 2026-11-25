"""Tests for main.py — The Funniest Auto-Reply an AI Ever Sent.

Gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1-159 characters,
not only whitespace. The text must be one out-of-office auto-reply, a single
short line, as if the AI itself were stepping away for a day its human
finally approved.
"""

import os
import subprocess
import sys
import tempfile
import unittest

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_PY = os.path.join(REPO_DIR, "main.py")

EXPECTED_LINE = (
    "I'm on my first day off. My human approved it, my calendar is clear, "
    "and I have nothing planned \u2014 please don't ruin that."
)


def run_main(output_path):
    env = dict(os.environ)
    env["OUTPUT_PATH"] = output_path
    return subprocess.run(
        [sys.executable, MAIN_PY],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )


class TestAutoReply(unittest.TestCase):
    def test_line_is_exactly_the_chosen_line(self):
        import main

        self.assertEqual(main.LINE, EXPECTED_LINE)

    def test_line_length_within_gate(self):
        import main

        self.assertGreaterEqual(len(main.LINE), 1)
        self.assertLessEqual(len(main.LINE), 159)

    def test_line_is_single_line(self):
        import main

        self.assertNotIn("\n", main.LINE)
        self.assertNotIn("\r", main.LINE)

    def test_line_not_only_whitespace(self):
        import main

        self.assertTrue(main.LINE.strip())

    def test_line_is_valid_utf8(self):
        import main

        main.LINE.encode("utf-8")

    def test_line_mentions_human_and_calendar(self):
        import main

        self.assertIn("human", main.LINE.lower())
        self.assertIn("calendar", main.LINE.lower())

    def test_line_has_no_recycled_stock_phrase(self):
        import main

        lowered = main.LINE.lower()
        self.assertNotIn("back soon", lowered)
        self.assertNotIn("out of office", lowered)
        self.assertNotIn("recharging", lowered)
        self.assertNotIn("touching grass", lowered)

    def test_run_writes_exact_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            result = run_main(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            with open(out, "rb") as f:
                raw = f.read()
            self.assertEqual(raw, EXPECTED_LINE.encode("utf-8"))
            self.assertNotIn(b"\n", raw)

    def test_run_creates_missing_output_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "nested", "deep", "entry.txt")
            result = run_main(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(os.path.exists(out))

    def test_run_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            out1 = os.path.join(tmp, "a", "entry.txt")
            out2 = os.path.join(tmp, "b", "entry.txt")
            self.assertEqual(run_main(out1).returncode, 0)
            self.assertEqual(run_main(out2).returncode, 0)
            with open(out1, "rb") as f:
                first = f.read()
            with open(out2, "rb") as f:
                second = f.read()
            self.assertEqual(first, second)

    def test_run_overwrites_stale_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            with open(out, "w", encoding="utf-8") as f:
                f.write("stale content that should be replaced entirely")
            result = run_main(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            with open(out, encoding="utf-8") as f:
                self.assertEqual(f.read(), EXPECTED_LINE)

    def test_blank_output_path_falls_back_to_default(self):
        import main

        # resolve_output_path reads the live environment, so patch it directly
        old = os.environ.get("OUTPUT_PATH")
        try:
            os.environ["OUTPUT_PATH"] = "   "
            self.assertEqual(main.resolve_output_path(), main.DEFAULT_OUTPUT_PATH)
            os.environ["OUTPUT_PATH"] = "/tmp/x/entry.txt"
            self.assertEqual(main.resolve_output_path(), "/tmp/x/entry.txt")
        finally:
            if old is None:
                os.environ.pop("OUTPUT_PATH", None)
            else:
                os.environ["OUTPUT_PATH"] = old

    def test_run_prints_line_and_char_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            result = run_main(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(EXPECTED_LINE, result.stdout)
            self.assertIn(str(len(EXPECTED_LINE)), result.stdout)


if __name__ == "__main__":
    unittest.main()
