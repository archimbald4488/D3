from itertools import combinations

def ngram_overlap(a: str, b: str, n=2):
    def make_ngrams(text):
        tokens = text.split()
        return set(tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1))
    A = make_ngrams(a)
    B = make_ngrams(b)
    if not A or not B:
        return 0.0
    overlap = len(A.intersection(B))
    return overlap / max(len(A), len(B))

def diversity_penalty(candidates):
    """
    Computes a diversity penalty: higher penalty = more similar candidates.
    """
    total_overlap = 0.0
    pairs = list(combinations(candidates, 2))
    if not pairs:
        return 0.0

    for a, b in pairs:
        total_overlap += ngram_overlap(a, b)

    # Return average overlap (lower is better)
    return total_overlap / len(pairs)
