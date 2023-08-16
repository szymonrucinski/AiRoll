from datasets import load_dataset

dataset = load_dataset("imagefolder", data_dir="data/train/")
print(dataset)

dataset.align_labels_with_mapping