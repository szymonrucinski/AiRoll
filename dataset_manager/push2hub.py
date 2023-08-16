from datasets import load_dataset

dataset = load_dataset("imagefolder", data_dir="../data/train/", split="train")
dataset.push_to_hub("szymonindy/types-of-film-shots")
