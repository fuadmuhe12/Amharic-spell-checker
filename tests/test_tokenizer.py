import pytest
from amharic_spell.preprocessing.tokenizer import AmharicTokenizer

def test_tokenize_simple():
    tokenizer = AmharicTokenizer()
    text = "ሰላም አለህ?"
    tokens = tokenizer.tokenize(text)
    assert tokens == ["ሰላም", "አለህ"]

def test_tokenize_punctuation():
    tokenizer = AmharicTokenizer()
    text = "ሰላም:: እንዴት ነህ?"
    tokens = tokenizer.tokenize(text)
    assert tokens == ["ሰላም", "እንዴት", "ነህ"]

def test_tokenize_sentence():
    tokenizer = AmharicTokenizer()
    text = "ሰላም ነው:: እንዴት ነህ? ደህና ነኝ።"
    sentences = tokenizer.tokenize_sentence(text)
    assert len(sentences) == 3
    assert sentences[0] == "ሰላም ነው"
    assert sentences[1] == "እንዴት ነህ"
    assert sentences[2] == "ደህና ነኝ"
