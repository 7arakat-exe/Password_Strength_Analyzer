import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from password_analyzer.analyzer import analyze_password, calculate_entropy, get_character_pool
from password_analyzer.breaches import (
    check_password_against_hash_file,
    normalize_hash_line,
    sha1_password,
)
from password_analyzer.generator import generate_password


class AnalyzerTests(unittest.TestCase):
    def test_character_pool_detects_sets_used(self):
        pool_size, sets_used = get_character_pool("Password123!")

        self.assertEqual(pool_size, 94)
        self.assertEqual(sets_used, ["lowercase", "uppercase", "digits", "symbols"])

    def test_empty_password_has_zero_entropy(self):
        self.assertEqual(calculate_entropy(""), 0.0)

    def test_analysis_contains_recommendations(self):
        result = analyze_password("short")

        self.assertEqual(result["length"], 5)
        self.assertIn(
            "Use at least 8 characters. NIST requires a minimum of 8.",
            result["recommendations"],
        )

    def test_sha1_password_uses_uppercase_hex(self):
        self.assertEqual(
            sha1_password("password"),
            "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8",
        )

    def test_normalize_hash_line_accepts_hash_count_format(self):
        line = "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8:3303003"

        self.assertEqual(
            normalize_hash_line(line),
            "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8",
        )

    def test_breach_hash_file_detects_known_password(self):
        with TemporaryDirectory() as directory:
            hash_file = Path(directory) / "breaches.txt"
            hash_file.write_text(
                "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8\n",
                encoding="utf-8",
            )

            result = check_password_against_hash_file("password", hash_file)

        self.assertTrue(result["breached"])
        self.assertEqual(result["hashes_checked"], 1)
    
    def test_generate_password_uses_requested_length(self):
        password = generate_password(length=20)

        self.assertEqual(len(password),20)
    
    def test_generate_password_rejects_short_length(self):
        with self.assertRaises(ValueError):
            generate_password(length=4)


if __name__ == "__main__":
    unittest.main()
