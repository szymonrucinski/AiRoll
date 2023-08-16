import logging

import torch
from torchvision import transforms
import torch.utils.data.dataloader

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
from datasets import load_dataset


def prepare_data():
    # Data augmentation and normalization for training
    # Just normalization for validation
    INPUT_SIZE = 224
    BATCH_SIZE = 32
    DEVICE = torch.cuda.device("cuda:0" if torch.cuda.is_available() else "cpu")
    logger.info(DEVICE)
    torch.manual_seed(42)
    dataset = load_dataset("szymonrucinski/types-of-film-shots")
    dataset = dataset.with_format("torch")
    dataset = dataset.map(lambda x: {"image": x["image"].type(torch.float)})
    # RESNET 34
    data_transforms = {
        "train": transforms.Compose(
            [
                transforms.RandomResizedCrop(INPUT_SIZE),
                # transforms.RandomHorizontalFlip(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        ),
    }
    # transfrom the dataset
    image_datasets = dataset.map(
        lambda x: {
            "image": data_transforms["train"](x["image"]),
            "label": x["label"],
        }
    )

    logger.info("Initializing Datasets and Dataloaders...")

    # Create training and validation datasets
    # print(len(image_datasets["train"]))
    image_datasets = image_datasets["train"]
    # split the dataset in train and test set
    train_size = int(0.8 * len(image_datasets))
    val_size = int(0.2 * train_size)
    train_size = train_size - val_size
    test_size = len(image_datasets) - train_size - val_size
    logger.info(
        "Train size: %d, Test size: %d, Val size: %d"
        % (train_size, test_size, val_size)
    )

    train_dataset, test_dataset, val_dataset = torch.utils.data.random_split(
        image_datasets, [train_size, test_size, val_size]
    )
    logger.info("Initializing Datasets and Dataloaders...")
    # Create training and validation dataloaders and test dataloader
    dataloaders_dict = {
        "train": torch.utils.data.DataLoader(
            train_dataset,
            batch_size=BATCH_SIZE,
            shuffle=True,
            num_workers=4,
        ),
        "test": torch.utils.data.DataLoader(
            test_dataset,
            batch_size=BATCH_SIZE,
            shuffle=True,
            num_workers=4,
        ),
        "val": torch.utils.data.DataLoader(
            val_dataset,
            batch_size=BATCH_SIZE,
            shuffle=True,
            num_workers=4,
        ),
    }
    logger.info(dataloaders_dict)
    return dataloaders_dict


prepare_data()
