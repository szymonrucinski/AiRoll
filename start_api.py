"""Serve the model as a fastapi app with gradio client"""

import os

import gradio as gr
import torch
import torchvision.transforms as transforms
from datasets import load_dataset
from PIL import Image
import logging
from torchvision import transforms
from torch import nn
from torchsummary import summary


dataset = load_dataset("szymonindy/types-of-film-shots")
class_map = dataset["train"].features["label"].names
num_classes = len(class_map)
import os
import glob

import gradio as gr

# Load
logging.info("Loading model")
PATH = "./model/shot_clf.pt"
LABELS = dataset["train"].features["label"].names
DEVICE = torch.device("cpu")
MODEL = torch.load(PATH, map_location=DEVICE)
num_features = MODEL.fc.in_features
MODEL.fc = nn.Linear(num_features, len(LABELS))
image = gr.inputs.Image(shape=(224, 224))
label = gr.outputs.Label(num_top_classes=len(LABELS))
logging.info("Model loaded")


def predict(image) -> dict[str, float]:
    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    image = transform(image)
    image = image.unsqueeze(0)

    with torch.no_grad():
        # prediction = prediction[0]
        prediction = MODEL(image)
        print(prediction)
        print(prediction[0])
        prediction = torch.nn.functional.softmax(prediction[0])
        print(prediction)
        # prediction = torch.nn.functional.softmax(prediction)
        confidences = {LABELS[i]: float(prediction[i]) for i in range(8)}
        print(confidences)
        return confidences


demo = gr.Interface(
    fn=predict,
    inputs=gr.Image(type="pil"),
    outputs=gr.Label(num_top_classes=8),
    examples=glob.glob("./examples/*"),
    interpretation="default",
)
demo.launch(
    debug=True,
    ssl_verify=False,
    server_port=7860,
)
