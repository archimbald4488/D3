# UNFINISHED

from data_loader import load_tsv_dataset
from preprocessing import preprocess_dataset
from prompts import zero_shot_prompt, cot_prompt, tot_prompt
from evaluation import simple_bleu
from model_real import call_openai
from tot_scoring import diversity_penalty
import json

DATA_PATH = "data/sample_dataset.tsv"
RESULT_PATH = "results/real_pipeline_outputs.json"

def run_real_pipeline():

    raw = load_tsv_dataset(DATA_PATH)
    data = preprocess_dataset(raw, use_sentencepiece=False)

    results = []

    for item in data:
        src = item["src"]
        tgt = item["tgt"]
        lp = item["lang_pair"]
        src_lang, tgt_lang = lp.split("-")

        prompt = tot_prompt(src, src_lang, tgt_lang, k=3)
        print("Calling LLM (DISABLED)...")

        response = call_openai(prompt)  # placeholder text
        hyp = response["translation"]

        entry = {
            "src": src,
            "tgt": tgt,
            "translation": hyp,
            "note": "LLM inference disabled in this version."
        }

        results.append(entry)

    with open(RESULT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Saved placeholder results to {RESULT_PATH}")


if __name__ == "__main__":
    run_real_pipeline()
