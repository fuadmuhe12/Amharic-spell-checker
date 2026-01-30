import re
import string
from typing import List, Optional

class AmharicTokenizer:
    """
    Tokenizer for Amharic text, handling specific punctuation and sentence segmentation.
    """

    def __init__(self, sent_punct: Optional[List[str]] = None, word_punct: Optional[List[str]] = None):
        self.sent_punct = sent_punct or ["።", "፥", "፨", "::", "፡፡", "?", "!"]
        self.word_punct = word_punct or ["።", "፥", "፤", "፨", "?", "!", ":", "፡", "፦", "፣"]
        
        # Punctuation to remove from words
        self.remove_punct_list = ["።", "፥", "፤", "፨", "?", "!", ":", "፡", "፦", "፣", "›", "‹"]
        self.remove_punct_list.extend(string.punctuation)
        
        # Pre-compile regex for performance
        self.remove_pattern = re.compile('|'.join(map(re.escape, self.remove_punct_list)))

    def _remove_punc(self, text: str) -> str:
        """Removes punctuation from a word."""
        return self.remove_pattern.sub("", text)

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenizes text into words, removing punctuation.
        """
        tokens = []
        word = ""
        prev_char = ''

        for char in text:
            if char == " ":
                if word:
                    if word not in self.word_punct:
                        tokens.append(self._remove_punc(word))
                word = ""
            elif char in self.word_punct:
                if word and prev_char != char:
                    if word not in self.word_punct:
                        tokens.append(self._remove_punc(word))
                    word = ""
                prev_char = char
                word += char
            else:
                word += char

        if word and word not in self.word_punct:
            tokens.append(self._remove_punc(word))

        # Filter out empty tokens
        return [t for t in tokens if t]

    def tokenize_sentence(self, text: str) -> List[str]:
        """
        Splits text into sentences based on Amharic sentence punctuation.
        """
        text = text.replace("\n", "።").replace("\r", " ")
        text = re.sub(r"\s+", " ", text)

        # Create a regex pattern to split by any sentence punctuation
        # We wrap in () to keep the delimiter if needed, but here we usually strip it or handle it.
        # The original logic kept the text between separators.
        
        pattern = '|'.join(map(re.escape, self.sent_punct))
        sentences = re.split(pattern, text)
        
        return [s.strip() for s in sentences if s.strip()]
