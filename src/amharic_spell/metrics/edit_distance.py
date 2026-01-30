from typing import List

# Try to import optimized library
try:
    from rapidfuzz.distance import DamerauLevenshtein
    HAS_OPTIMIZED = True
except ImportError:
    HAS_OPTIMIZED = False

def calculate_edit_distance(s1: str, s2: str) -> int:
    """
    Calculates the Damerau-Levenshtein distance between two strings.
    Uses rapidfuzz (C++ optimized) if available, otherwise pure Python implementation.
    """
    if HAS_OPTIMIZED:
        return DamerauLevenshtein.distance(s1, s2)
    
    return _damerau_levenshtein_pure_python(s1, s2)

def _damerau_levenshtein_pure_python(s1: str, s2: str) -> int:
    """
    Pure Python implementation of Damerau-Levenshtein distance.
    Source: https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
    """
    len1 = len(s1)
    len2 = len(s2)
    infinite = len1 + len2
    
    # 2D array: d[len1+2][len2+2]
    d = [[0] * (len2 + 2) for _ in range(len1 + 2)]
    
    da: dict[str, int] = {}
    
    d[0][0] = infinite
    for i in range(len1 + 1):
        d[i+1][0] = infinite
        d[i+1][1] = i
    for j in range(len2 + 1):
        d[0][j+1] = infinite
        d[1][j+1] = j
        
    for i in range(1, len1 + 1):
        db = 0
        for j in range(1, len2 + 1):
            i1 = da.get(s2[j-1], 0)
            j1 = db
            cost = 1
            if s1[i-1] == s2[j-1]:
                cost = 0
                db = j
            
            d[i+1][j+1] = min(
                d[i][j] + cost,              # substitution
                d[i+1][j] + 1,              # insertion
                d[i][j+1] + 1,              # deletion
                d[i1][j1] + (i-i1-1) + 1 + (j-j1-1) # transposition
            )
        da[s1[i-1]] = i
        
    return d[len1+1][len2+1]
