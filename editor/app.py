from basic_cut import init
import os

def main():
    directory_path = 'C:\\Users\\Szymon\\Desktop\\New folder (4)'
    files = os.listdir(directory_path)
    video_paths = []
    print(files)
    for file_path in files:
        video_paths.append(os.path.join(directory_path,file_path))

    init(video_paths)

main()