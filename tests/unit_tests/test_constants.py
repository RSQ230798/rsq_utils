import pytest

from src.rsq_utils.constants import alphabet

def test_alphabet_content():
    """Test that alphabet contains all lowercase letters a-z."""
    expected = [chr(i) for i in range(97, 123)]  # a-z
    assert alphabet == expected
    assert len(alphabet) == 26
    assert alphabet[0] == 'a'
    assert alphabet[-1] == 'z'

    for letter in alphabet:
        assert isinstance(letter, str)
        assert len(letter) == 1
