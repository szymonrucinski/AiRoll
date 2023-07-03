import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
DATA_DIR = os.path.join(BASE_DIR, "data")
SAMPLE_DIR = os.path.join(DATA_DIR, "samples")
SAMPLE_INPUTS = os.path.join(SAMPLE_DIR, "inputs")
SAMPLE_OUTPUTS = os.path.join(SAMPLE_DIR, "outputs")
AUDIO_DEPT = os.path.join(SAMPLE_DIR, "audio_component")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
MODEL_PATH = os.path.join(BASE_DIR, "shot_classifier.onnx")
