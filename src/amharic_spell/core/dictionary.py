from pathlib import Path
from typing import Set, Union, Optional
from collections import Counter
from ..preprocessing.normalizer import AmharicNormalizer

class Dictionary:
    """
    Efficient Amharic Dictionary for O(1) lookups.
    Handles normalization internally to ensure consistency.
    """
    def __init__(self, dictionary_path: Union[str, Path]):
        self.dictionary_path = Path(dictionary_path)
        self.words: Set[str] = set()
        self.normalizer = AmharicNormalizer()
        
        self._load_dictionary()

    def _load_dictionary(self) -> None:
        """Loads words from the file, normalizing them."""
        if not self.dictionary_path.exists():
            raise FileNotFoundError(f"Dictionary file not found at: {self.dictionary_path}")

        try:
            with open(self.dictionary_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        # We normalize regular dictionary words to match input text
                        self.words.add(self.normalizer.normalize(word))
        except Exception as e:
            print(f"Error loading dictionary: {e}")
            raise

    def check(self, word: str) -> bool:
        """
        Check if a word exists in the dictionary.
        Input word is normalized before checking.
        """
        normalized_word = self.normalizer.normalize(word)
        return normalized_word in self.words

    def __contains__(self, word: str) -> bool:
        return self.check(word)

    def __len__(self) -> int:
        return len(self.words)
