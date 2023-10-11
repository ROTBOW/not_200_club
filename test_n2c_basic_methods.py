import pytest

from Not_200_Club import Not200Club



def test_can_instantiate_class():
    n2c = Not200Club(None)
    assert isinstance(n2c, Not200Club)

def test_validate_url():
    n2c = Not200Club(None)
    assert n2c._Not200Club__validate_url('https://www.google.com') == 'https://www.google.com'
    assert n2c._Not200Club__validate_url('') == ''
    assert n2c._Not200Club__validate_url('www.google.com/search?q=python') == 'https://www.google.com/search?q=python'
    assert n2c._Not200Club__validate_url('http://www.google.com/search?q=python') == 'http://www.google.com/search?q=python'