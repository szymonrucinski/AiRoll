from basic_cut import init
import os

def run(directory_path, song_path, progress):
    files = os.listdir(directory_path)
    video_paths = []
    print(files)
    for file_path in files:
        video_paths.append(os.path.join(directory_path,file_path))
    
    init(video_paths, song_path, progress)