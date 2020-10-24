from conf import SAMPLE_INPUTS, SAMPLE_OUTPUTS
from moviepy.editor import *
from PIL import Image

source_path = os.path.join(SAMPLE_INPUTS, 'movie.mp4')
thumbnail_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails")
os.makedirs(thumbnail_dir, exist_ok=True)

thumbnail_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails")
thumbnail_per_frame_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails-per-frame")
thumbnail_per_half_second_dir = os.path.join(SAMPLE_OUTPUTS, "thumbnails-per-half-second")


clip = VideoFileClip(source_path)

print(clip.reader.fps)
print(clip.reader.nframes)
duration = clip.duration
max_duration = int(duration) + 1

for i in range(0, max_duration + 1):
    new_img_filepath = os.path.join(thumbnail_dir, f"{i}.png")
    frame = clip.get_frame(i)
    new_img = Image.fromarray(frame)
    new_img.save(new_img_filepath)
