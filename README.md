LLM Translation Reproduction (Minimal)

Contents:
- src/main_simulated.py : minimal reproduction runner
- data/sample_dataset.tsv : tiny example dataset (EN-DE)
- results/ : outputs produced after running
- All other files under /src/ are part of my unfinished attempts to get the program to work with actual API prompts and FLORES datasets. Please disregard them.

Setup:
- Recommended: create a Python 3.9+ virtualenv
- (Optional) Install dependencies:
    pip install -r requirements.txt

Run:
- Simulate mode (no API keys needed):
    python src/main.py --simulate
  This writes results/outputs.json with simulated translations and simple scores.

- To extend :
  * Replace data/sample_dataset.tsv with real datasets (FLORES-200, WMT subsets) in the same TSV format.
  * Finish creating main_real.py
  

