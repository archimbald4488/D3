def zero_shot_prompt(src, src_lang, tgt_lang):
    return f"Translate from {src_lang} to {tgt_lang}:\n{src}"

def few_shot_prompt(src, examples, src_lang, tgt_lang):
    demos = ""
    for ex in examples:
        demos += f"ENGLISH: {ex['src']}\nGERMAN: {ex['tgt']}\n\n"
    demos += f"Translate from {src_lang} to {tgt_lang}:\n{src}"
    return demos

def cot_prompt(src, src_lang, tgt_lang):
    return f"""
Translate from {src_lang} to {tgt_lang}.
Source: {src}

Think step-by-step:
1. Analyze grammar and meaning
2. Resolve ambiguity
3. Propose a translation
4. Verify semantic alignment

Provide final translation at the end.
"""

def tot_prompt(src, src_lang, tgt_lang, k=3):
    return f"""
Translate from {src_lang} to {tgt_lang}.
Source: {src}

Generate {k} candidate translations.
For each candidate, assign scores:
- Accuracy (1–10)
- Fluency (1–10)
- Style (1–10)
- Cultural Fit (1–10)

Then select the best candidate and justify your choice.
"""
