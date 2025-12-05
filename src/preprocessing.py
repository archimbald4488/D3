import re

def basic_clean(text: str):
    """Minimal cleaning compatible with FLORES/WMT preprocessing."""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

def whitespace_tokenize(text: str):
    """Fallback tokenizer if SentencePiece/BPE not available."""
    return text.split()

def sentencepiece_tokenize(sp_model, text: str):
    """Wrapper for SentencePiece if available."""
    return sp_model.encode(text, out_type=str)

def preprocess_dataset(records, use_sentencepiece=False, sp_model=None):
    """
    Generic preprocessing pipeline.
    Hooks exist for expanding with lowercasing, punctuation normalization,
    or dataset-specific cleaning.
    """
    processed = []
    for r in records:
        src = basic_clean(r["src"])
        tgt = basic_clean(r["tgt"])
        if use_sentencepiece and sp_model is not None:
            src_tok = sentencepiece_tokenize(sp_model, src)
            tgt_tok = sentencepiece_tokenize(sp_model, tgt)
        else:
            src_tok = whitespace_tokenize(src)
            tgt_tok = whitespace_tokenize(tgt)

        processed.append({
            "src": src,
            "tgt": tgt,
            "src_tok": src_tok,
            "tgt_tok": tgt_tok,
            "lang_pair": r["lang_pair"],
        })
    return processed
