from moviepy.editor import *
import sys


class Video_controller:
    def __init__(self, video_path):
        print(video_path)
        self.clip = VideoFileClip(video_path)

    def get_duration(self):
        return self.clip.duration

    def get_frames_count(self):
        return self.clip.reader.nframes

    def get_fps(self):
        return self.clip.reader.fps

    def get_seconds_count(self):
        return self.clip.reader.nframes / (self.clip.reader.fps * 1.0)

    def get_clip_size(self):
        return sys.getsizeof(self.clip)
