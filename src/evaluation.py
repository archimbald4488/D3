def simple_bleu(reference: str, hypothesis: str):
    ref = set(reference.split())
    hyp = set(hypothesis.split())
    if not hyp:
        return 0.0
    return 100.0 * len(ref.intersection(hyp)) / len(hyp)
