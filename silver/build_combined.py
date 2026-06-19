"""Combine gold (human) + silver (AI) into one dataset with an `annotator` column.

gold  = szymonrucinski/types-of-film-shots          (925, human-labeled)
silver= szymonrucinski/types-of-film-shots-silver    (1994, v2+Opus auto-labeled)
-> szymonrucinski/types-of-film-shots-combined  with annotator in {human, ai}.
Both already share the same 8-class ClassLabel, so concatenation is clean.
"""
import datasets
from datasets import load_dataset, concatenate_datasets

gold = load_dataset("szymonrucinski/types-of-film-shots", split="train")
silver = load_dataset("szymonrucinski/types-of-film-shots-silver", split="train")
print("gold", len(gold), gold.features["label"].names)
print("silver", len(silver), silver.features["label"].names)
assert gold.features["label"].names == silver.features["label"].names, "label sets differ!"

N = len(gold)
gold = (gold
        .add_column("annotator", ["human"] * N)
        .add_column("source", ["human"] * N)
        .add_column("confidence", [1.0] * N)
        .add_column("movie", [""] * N))
silver = silver.add_column("annotator", ["ai"] * len(silver))

cols = ["image", "label", "annotator", "source", "confidence", "movie"]
gold = gold.select_columns(cols)
silver = silver.select_columns(cols)

combined = concatenate_datasets([gold, silver])
print("combined", len(combined))
from collections import Counter
print("annotator:", Counter(combined["annotator"]))
combined.push_to_hub("szymonrucinski/types-of-film-shots-combined", private=False)
print("pushed -> szymonrucinski/types-of-film-shots-combined")
