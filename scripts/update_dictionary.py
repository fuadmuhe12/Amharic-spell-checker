"""
Extract unique words from corpus and append to amharic_dictionary.txt.
Skips words already in the dictionary. Normalizes before adding.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "amharic_corpus.txt"
DICTIONARY = ROOT / "data" / "amharic_dictionary.txt"


def main() -> None:
    sys.path.insert(0, str(ROOT / "src"))
    from amharic_spell.preprocessing.tokenizer import AmharicTokenizer
    from amharic_spell.preprocessing.normalizer import AmharicNormalizer

    normalizer = AmharicNormalizer()
    tokenizer = AmharicTokenizer()

    existing = set()
    if DICTIONARY.exists():
        with open(DICTIONARY, "r", encoding="utf-8") as f:
            for line in f:
                w = normalizer.normalize(line.strip())
                if w:
                    existing.add(w)

    corpus_words = set()
    with open(CORPUS, "r", encoding="utf-8") as f:
        for line in f:
            text = line.strip()
            if not text:
                continue
            for word in tokenizer.tokenize(text):
                if word:
                    corpus_words.add(normalizer.normalize(word))

    new_words = sorted(corpus_words - existing)
    if not new_words:
        print("No new words to add.")
        return

    with open(DICTIONARY, "a", encoding="utf-8") as f:
        for w in new_words:
            f.write(w + "\n")
    print(f"Added {len(new_words)} new words to dictionary.")


if __name__ == "__main__":
    main()
