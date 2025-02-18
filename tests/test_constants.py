import unittest
from src.rsq_utils.constants import ALPHABET

class TestConstants(unittest.TestCase):
    """Test suite for constants module."""

    def test_alphabet_content(self):
        """Test that ALPHABET contains all lowercase letters a-z."""
        expected = [chr(i) for i in range(97, 123)]  # a-z
        self.assertEqual(ALPHABET, expected)
        self.assertEqual(len(ALPHABET), 26)
        self.assertEqual(ALPHABET[0], 'a')
        self.assertEqual(ALPHABET[-1], 'z')

    def test_alphabet_immutability(self):
        """Test that ALPHABET list contains immutable strings."""
        for letter in ALPHABET:
            self.assertIsInstance(letter, str)
            self.assertEqual(len(letter), 1)


if __name__ == '__main__':
    unittest.main()
