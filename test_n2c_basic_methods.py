import pytest

from Not_200_Club import Not200Club



def test_can_instantiate_class():
    n2c = Not200Club(None)
    assert isinstance(n2c, Not200Club)

def test_idx_to_letter():
    n2c = Not200Club(None)
    assert n2c._Not200Club__idx_to_letter(0) == 'A'
    assert n2c._Not200Club__idx_to_letter(25) == 'Z'
    assert n2c._Not200Club__idx_to_letter(26) == 'AA'
    assert n2c._Not200Club__idx_to_letter(27) == 'AB'
    assert n2c._Not200Club__idx_to_letter(28) == 'AC'

def test_validate_url():
    n2c = Not200Club(None)
    assert n2c._Not200Club__validate_url('https://www.google.com') == 'https://www.google.com'
    assert n2c._Not200Club__validate_url('') == ''
    assert n2c._Not200Club__validate_url('www.google.com/search?q=python') == 'https://www.google.com/search?q=python'
    assert n2c._Not200Club__validate_url('http://www.google.com/search?q=python') == 'http://www.google.com/search?q=python'