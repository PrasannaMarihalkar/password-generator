import unittest
import string
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from password_generator import (
    build_character_pool,
    generate_password,
    calculate_entropy,
    get_strength_label,
    estimate_crack_time,
)


class TestCharacterPool(unittest.TestCase):

    def test_all_sets_enabled(self):
        pool, mandatory = build_character_pool(True, True, True, True)
        self.assertGreater(len(pool), 0)
        self.assertEqual(len(mandatory), 4)

    def test_only_digits(self):
        pool, mandatory = build_character_pool(False, False, True, False)
        self.assertEqual(pool, string.digits)
        self.assertEqual(len(mandatory), 1)
        self.assertIn(mandatory[0], string.digits)

    def test_digits_in_pool_when_selected(self):
        pool, _ = build_character_pool(False, False, True, False)
        for ch in string.digits:
            self.assertIn(ch, pool)

    def test_symbols_in_pool_when_selected(self):
        pool, _ = build_character_pool(False, False, False, True)
        for ch in string.punctuation:
            self.assertIn(ch, pool)


class TestPasswordGeneration(unittest.TestCase):

    def test_correct_length(self):
        pool, mandatory = build_character_pool(True, True, True, True)
        for target_len in [8, 15, 32, 64]:
            pw = generate_password(target_len, pool, mandatory)
            self.assertEqual(len(pw), target_len)

    def test_all_chars_in_pool(self):
        pool, mandatory = build_character_pool(True, True, True, True)
        pw = generate_password(20, pool, mandatory)
        for ch in pw:
            self.assertIn(ch, pool)

    def test_passwords_are_unique(self):
        pool, mandatory = build_character_pool(True, True, True, True)
        passwords = {generate_password(20, pool, mandatory) for _ in range(100)}
        self.assertGreater(len(passwords), 95)

    def test_mandatory_char_types_present(self):
        pool, mandatory = build_character_pool(True, True, True, True)
        pw = generate_password(20, pool, mandatory)
        has_upper  = any(c in string.ascii_uppercase for c in pw)
        has_lower  = any(c in string.ascii_lowercase for c in pw)
        has_digit  = any(c in string.digits for c in pw)
        has_symbol = any(c in string.punctuation for c in pw)
        self.assertTrue(has_upper and has_lower and has_digit and has_symbol)


class TestEntropy(unittest.TestCase):

    def test_entropy_formula(self):
        result = calculate_entropy(16, 62)
        expected = 16 * math.log2(62)
        self.assertAlmostEqual(result, expected, places=5)

    def test_longer_password_more_entropy(self):
        e1 = calculate_entropy(8, 62)
        e2 = calculate_entropy(16, 62)
        self.assertGreater(e2, e1)

    def test_larger_pool_more_entropy(self):
        e1 = calculate_entropy(16, 26)
        e2 = calculate_entropy(16, 94)
        self.assertGreater(e2, e1)

    def test_zero_edge_case(self):
        self.assertEqual(calculate_entropy(10, 1), 0.0)


class TestStrengthLabel(unittest.TestCase):

    def test_very_weak(self):
        label, _ = get_strength_label(20)
        self.assertEqual(label, "Very Weak")

    def test_strong(self):
        label, _ = get_strength_label(100)
        self.assertEqual(label, "Strong")

    def test_very_strong(self):
        label, _ = get_strength_label(200)
        self.assertEqual(label, "Very Strong")


class TestCrackTime(unittest.TestCase):

    def test_returns_string(self):
        result = estimate_crack_time(40)
        self.assertIsInstance(result, str)

    def test_very_high_entropy_is_long(self):
        result = estimate_crack_time(256)
        long_indicators = ["year", "infinite", "million", "billion"]
        self.assertTrue(any(word in result.lower() for word in long_indicators))


if __name__ == "__main__":
    unittest.main(verbosity=2)
