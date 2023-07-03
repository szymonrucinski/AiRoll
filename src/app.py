from basic_cut import init
import os


def run(directory_path, song_path, progress):
    files = os.listdir(directory_path)
    video_paths = []
    # sort files in folder
    video_paths.sort()
    print(files)
    for file_path in files:
        # file = os.path.join(rootDir, filename).replace(" ", "\\ ")

        # video_paths.append(os.path.join(directory_path, file_path).replace(" ", "\\ "))
        video_paths.append(os.path.join(directory_path, file_path))

    # song_path = str(song_path).replace(" ", "\\ ")
    init(video_paths, song_path, progress)
