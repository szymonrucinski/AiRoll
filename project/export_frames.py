from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS
from moviepy.editor import *
from PIL import Image

source_path = os.path.join(SAMPLE_INPUTS, 'movie.mp4')
thumbnail_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails")
thumbnail_per_frame_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails-per-frame")
thumbnail_per_half_second_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails-per-half-second")

os.makedirs(thumbnail_dir, exist_ok=True)
os.makedirs(thumbnail_per_frame_dir, exist_ok=True)
os.makedirs(thumbnail_per_half_second_dir, exist_ok=True)
print("Niech spadnie z nieba złoty deszcz........")