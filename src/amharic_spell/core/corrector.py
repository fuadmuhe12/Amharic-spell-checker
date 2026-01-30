from typing import List, Dict, Any, Tuple
from ..core.dictionary import Dictionary
from ..metrics.edit_distance import calculate_edit_distance
from ..models.ngram import InterpolatedLanguageModel
from ..preprocessing.tokenizer import AmharicTokenizer
from ..preprocessing.normalizer import AmharicNormalizer
from typing import Optional

class SpellCorrector:
    """
    Main Spell Corrector class.
    Combines Dictionary lookup, Edit Distance, and N-gram scoring.
    """
    def __init__(self, 
                 dictionary_path: str, 
                 model_path: Optional[str] = None, 
                 lm_model: Optional[InterpolatedLanguageModel] = None):
        
        self.dictionary = Dictionary(dictionary_path)
        self.tokenizer = AmharicTokenizer()
        self.normalizer = AmharicNormalizer()
        
        if lm_model:
            self.model = lm_model
        elif model_path:
            self.model = InterpolatedLanguageModel.load(model_path)
        else:
            raise ValueError("Must provide either model_path or lm_model")

    def correct(self, text: str) -> Dict[str, Any]:
        """
        Corrects a given text.
        Returns detailed result structure.
        """
        # 1. Preprocessing
        # We process sentence by sentence
        sentences = self.tokenizer.tokenize_sentence(text)
        corrected_sentences = []
        errors = []
        
        for sentence_raw in sentences:
            tokens = self.tokenizer.tokenize(sentence_raw)
            corrected_tokens = []
            
            for i, word in enumerate(tokens):
                # Check if word is correct
                if word in self.dictionary:
                    corrected_tokens.append(word)
                    continue
                
                # It's an error
                candidates = self._generate_candidates(word)
                if not candidates:
                    # No candidates found, keep original
                    corrected_tokens.append(word) 
                    errors.append({
                        "word": word,
                        "suggestions": [],
                        "context": tokens[max(0, i-2):i+3]
                    })
                    continue
                
                # Rank candidates
                # Context: previous 2 words
                context = corrected_tokens[-2:] 
                # (We use corrected tokens for context as we go left-to-right)
                
                ranked = self._rank_candidates(candidates, context)
                best_suggestion = ranked[0][0]
                corrected_tokens.append(best_suggestion)
                
                errors.append({
                    "word": word,
                    "suggestions": ranked[:5], # Top 5
                    "context": context
                })
            
            corrected_sentences.append(" ".join(corrected_tokens))
            
        return {
            "original_text": text,
            "corrected_text": " ".join(corrected_sentences),
            "errors": errors
        }

    def _generate_candidates(self, word: str, max_distance: int = 2) -> List[str]:
        """Generate candidates within max_distance."""
        candidates = []
        # Optimization: Scan dictionary? That's O(V). 
        # For a production system we'd use a BK-Tree or SymSpell. 
        # For this scale, scanning is acceptable but slow.
        # We can optimize by length filtering first.
        
        w_len = len(word)
        for cand in self.dictionary.words:
            if abs(len(cand) - w_len) > max_distance:
                continue
            
            dist = calculate_edit_distance(word, cand)
            if dist <= max_distance:
                candidates.append(cand)
        
        return candidates

    def _rank_candidates(self, candidates: List[str], context: List[str]) -> List[Tuple[str, float]]:
        """Rank candidates by LM score."""
        scores = []
        for cand in candidates:
            score = self.model.score(cand, context)
            scores.append((cand, score))
        
        # Sort by score descending
        return sorted(scores, key=lambda x: x[1], reverse=True)
