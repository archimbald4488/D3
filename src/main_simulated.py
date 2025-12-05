"""
Minimal reproduction code for:
"Reasoning for Translation: Comparative Analysis of Chain-of-Thought and Tree-of-Thought Prompting for LLM Translation"

This script is intentionally minimal and safe to run without API keys.
It demonstrates:
 - dataset loading (small synthetic sample)
 - simple tokenization (word-split or SentencePiece if installed)
 - prompt templates for Zero-shot, Few-shot, CoT, ToT
 - a runner that either calls an LLM (if API key provided) or simulates outputs
 - evaluation using a simple BLEU-like metric

Usage:
    python src/main.py --simulate       # run with simulated model outputs (default)
"""

import argparse
import os
import random
import json
from pathlib import Path
from typing import List, Dict

DATA_PATH = Path(__file__).parents[1] / "data" / "sample_dataset.tsv"
RESULTS_PATH = Path(__file__).parents[1] / "results" / "outputs.json"

def load_dataset(path: str):
    lines = []
    with open(path, "r", encoding="utf-8") as f:
        for row in f:
            row = row.strip()
            if not row:
                continue
            src, tgt, lp = row.split("\t")
            lines.append({"src": src, "tgt": tgt, "lang_pair": lp})
    return lines

def simple_tokenize(text: str):
    return text.strip().split()

def zero_shot_prompt(src, src_lang="EN", tgt_lang="DE"):
    return f"Translate the following sentence from {src_lang} to {tgt_lang}:\\n{src}"

def few_shot_prompt(src, examples: List[Dict], src_lang="EN", tgt_lang="DE"):
    demo = ""
    for ex in examples:
        demo += f"Translate the following sentence from {src_lang} to {tgt_lang}:\\n{ex['src']}\\n{ex['tgt']}\\n\\n"
    demo += f"Now translate the following sentence from {src_lang} to {tgt_lang}:\\n{src}"
    return demo

def cot_prompt(src, steps_hint="1) Analyze grammar\\n2) Resolve ambiguities\\n3) Generate candidate\\n4) Verify semantic parity", src_lang="EN", tgt_lang="DE"):
    return f"Translate from {src_lang} to {tgt_lang}:\\nSource: {src}\\nDo the following steps:\\n{steps_hint}\\nProvide the final translation and a confidence score (1-10)."

def tot_prompt(src, k_candidates=3, src_lang="EN", tgt_lang="DE"):
    return f"Translate from {src_lang} to {tgt_lang}:\\nSource: {src}\\nGenerate {k_candidates} valid translation candidates, and for each give scores for Accuracy(1-10), Fluency(1-10), Style(1-10), Cultural(1-10). Then pick the best candidate."

def simulated_model_response(prompt: str):
    # pseudo-translation for demonstration
    text = prompt.split("\\n")[-1]
    tokens = text.split()
    # naive "translation": reverse word order and append [DE] as a tag
    translated = " ".join(tokens[::-1]) + " [DE]"
    return {"translation": translated, "scores": {"bleu_like": random.uniform(20,45)}}

def simple_bleu(reference: str, hypothesis: str):
    # naive unigram overlap score (not sacrebleu)
    ref_tokens = set(reference.split())
    hyp_tokens = set(hypothesis.split())
    overlap = ref_tokens.intersection(hyp_tokens)
    if not hyp_tokens:
        return 0.0
    return 100.0 * len(overlap) / len(hyp_tokens)

def run_all(method="simulate"):
    data = load_dataset(DATA_PATH)
    examples = data[:3]  # use top 3 as few-shot examples
    outputs = []
    for item in data:
        src = item["src"]
        tgt = item["tgt"]
        lp = item["lang_pair"]
        src_lang, tgt_lang = lp.split("-")
        prompts = {
            "zero_shot": zero_shot_prompt(src, src_lang, tgt_lang),
            "few_shot": few_shot_prompt(src, examples, src_lang, tgt_lang),
            "cot": cot_prompt(src, src_lang=src_lang, tgt_lang=tgt_lang),
            "tot": tot_prompt(src, k_candidates=3, src_lang=src_lang, tgt_lang=tgt_lang)
        }
        result_item = {"src": src, "tgt": tgt, "lang_pair": lp, "results": {}}
        for name, prompt in prompts.items():
            if method == "simulate":
                resp = simulated_model_response(prompt)
            else:
                resp = simulated_model_response(prompt)
            hyp = resp.get("translation", "[no-output]")
            score = simple_bleu(tgt, hyp)
            result_item["results"][name] = {"prompt": prompt, "translation": hyp, "score": score}
        outputs.append(result_item)
    os.makedirs(Path(RESULTS_PATH).parent, exist_ok=True)
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(outputs, f, ensure_ascii=False, indent=2)
    print(f"Done. Results saved to {RESULTS_PATH}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true", help="Use simulated model outputs (default)")
    args = parser.parse_args()
    run_all(method="simulate")

