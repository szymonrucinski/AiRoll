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

fps = clip.reader.fps
nframes = clip.reader.nframes
seconds = nframes / (fps*1.0)

#getAll frames
# for i in range(0, max_duration):
# # for i in range(0, max_duration + 1):
#     current_ms = int((i/fps) * 1000)
#     print(current_ms)
#     # if i % fps == 0:
#     # current_ms = int((i/fps) * 1000)
#     new_img_filepath = os.path.join(thumbnail_dir, f"{current_ms}.png")
#     frame = clip.get_frame(i)
#     new_img = Image.fromarray(frame)
#     new_img.save(new_img_filepath)

def saveFramesToImages():
    for i, frame in enumerate(clip.iter_frames()):
        # print(i, frame)
        fphs = int(fps/2)
        if i % fphs == 0:
            current_ms = int((i / fps) * 1000)
            new_img_filepath = os.path.join(SAMPLE_OUTPUTS, f"{current_ms}.jpg")
            # print(f"frame at {i} seconds saved at {new_img_filepath}")
            new_img = Image.fromarray(frame)
            new_img.save(new_img_filepath)

 