import pytest
from amharic_spell.preprocessing.normalizer import AmharicNormalizer

def test_normalize_chars():
    normalizer = AmharicNormalizer()
    # "ሀ" -> "ሃ", "ሠ" -> "ሰ"
    assert normalizer.normalize("ሀገር") == "ሃገር"
    assert normalizer.normalize("ሠላም") == "ሰላም"

def test_normalize_complex():
    normalizer = AmharicNormalizer()
    # "ፀሐይ" -> "ጸሃይ"
    assert normalizer.normalize("ፀሐይ") == "ጸሃይ"

def test_normalize_whitespace():
    normalizer = AmharicNormalizer()
    assert normalizer.normalize("ሰላም    ነው") == "ሰላም ነው"
