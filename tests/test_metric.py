import pytest
from amharic_spell.metrics.edit_distance import calculate_edit_distance

def test_edit_distance_same():
    assert calculate_edit_distance("ሰላም", "ሰላም") == 0

def test_edit_distance_insertion():
    assert calculate_edit_distance("ሰላም", "ሰላምም") == 1

def test_edit_distance_substitution():
    assert calculate_edit_distance("ሰላም", "ሰለም") == 1

def test_edit_distance_transposition():
    # "abcd" -> "acbd" = 1 transposition
    assert calculate_edit_distance("1234", "1324") == 1
