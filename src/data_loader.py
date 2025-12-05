import csv
from pathlib import Path

def load_tsv_dataset(path: str):
    """
    Load a TSV dataset with columns: src, tgt, lang_pair.
    Compatible with both small synthetic datasets and large FLORES/WMT files.
    """
    records = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if len(row) != 3:
                continue
            src, tgt, lp = row
            records.append({"src": src, "tgt": tgt, "lang_pair": lp})
    return records
