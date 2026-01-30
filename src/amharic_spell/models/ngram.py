import math
import pickle
from collections import Counter, defaultdict
from typing import List, Tuple, Dict, Optional
from pathlib import Path

class InterpolatedLanguageModel:
    """
    A 3-gram Language Model using Linear Interpolation smoothing.
    P(w|u, v) = λ1 P(w|u, v) + λ2 P(w|v) + λ3 P(w)
    """
    def __init__(self, lambdas: Tuple[float, float, float] = (0.4, 0.4, 0.2)):
        self.lambdas = lambdas
        assert sum(self.lambdas) == 1.0, "Lambdas must sum to 1.0"
        
        self.unigrams: Counter[str] = Counter()
        self.bigrams: Counter[Tuple[str, str]] = Counter()
        self.trigrams: Counter[Tuple[str, str, str]] = Counter()
        
        self.total_words = 0
        self.vocab: Dict[str, int] = {}

    def train(self, tokenized_sentences: List[List[str]]) -> None:
        """
        Train the model on a list of tokenized sentences.
        """
        for sentence in tokenized_sentences:
            # Add start/end tokens
            # For trigram: <s> <s> w1 w2 ... </s>
            tokens = ["<s>", "<s>"] + sentence + ["</s>"]
            
            self.total_words += len(sentence)
            
            # Count N-grams
            for i in range(len(tokens)):
                token = tokens[i]
                self.unigrams[token] += 1
                
                if i >= 1:
                    bg = (tokens[i-1], token)
                    self.bigrams[bg] += 1
                
                if i >= 2:
                    tg = (tokens[i-2], tokens[i-1], token)
                    self.trigrams[tg] += 1

    def score(self, word: str, context: List[str]) -> float:
        """
        Calculate P(word | context) using interpolation.
        Context should be the previous 2 words [w_n-2, w_n-1].
        """
        # Ensure context has at least 2 words (pad with <s> if needed)
        padded_context = (["<s>"] * 2 + context)[-2:]
        u, v = padded_context[0], padded_context[1]
        w = word
        
        # 1. Trigram Prob: P(w | u, v) = C(u, v, w) / C(u, v)
        c_uvw = self.trigrams[(u, v, w)]
        c_uv = self.bigrams[(u, v)]
        p_tri = c_uvw / c_uv if c_uv > 0 else 0.0
        
        # 2. Bigram Prob: P(w | v) = C(v, w) / C(v)
        c_vw = self.bigrams[(v, w)]
        c_v = self.unigrams[v]
        p_bi = c_vw / c_v if c_v > 0 else 0.0
        
        # 3. Unigram Prob: P(w) = C(w) / N
        c_w = self.unigrams[w]
        p_uni = c_w / self.total_words if self.total_words > 0 else 0.0
        
        # Interpolate
        p_interpolated = (self.lambdas[0] * p_tri) + \
                         (self.lambdas[1] * p_bi) + \
                         (self.lambdas[2] * p_uni)
                         
        return p_interpolated

    def save(self, path: str) -> None:
        """Save model to file."""
        with open(path, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, path: str) -> 'InterpolatedLanguageModel':
        """Load model from file."""
        with open(path, 'rb') as f:
            return pickle.load(f)
