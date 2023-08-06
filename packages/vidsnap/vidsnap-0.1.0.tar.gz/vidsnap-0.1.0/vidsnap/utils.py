from colorama import Fore, Style
import concurrent.futures
from pathlib import Path
import cv2
import click


def write_images_from_video(video_path, every_x_sec, out_path):
    capture = cv2.VideoCapture(video_path)
    framerate = capture.get(cv2.CAP_PROP_FPS)
    total_frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    current_frame = 1
    fnbase = video_path.split("\\")[-1].replace(".mp4", "")

    # Get a frame every x sec, means, every x sec we'll be y frames further

    while current_frame < total_frames:
        capture.set(1, current_frame)
        ret, frame = capture.read()
        if out_path[-1] != "/" or out_path[-1] != "\\":
            out_path += "/"
        if ret:
            file_name = f"{out_path}{fnbase}-{current_frame}.jpg"
            cv2.imwrite(file_name, frame)

        current_frame = int(current_frame + (every_x_sec * framerate))

    return f"Finished Video: {fnbase}"


def run_video_extractor(input_path, output_path, video_extension,
                        workers, snap_every_x):
    total_counter = 0
    complete_counter = 0
    video_pathlist = [
        path for path in Path(f"{input_path}").glob(f"*.{video_extension}")
    ]

    with concurrent.futures.ThreadPoolExecutor(workers) as executor:
        futures = []
        for path in video_pathlist:
            futures.append(
                executor.submit(
                    write_images_from_video, str(path), snap_every_x, output_path
                )
            )
            total_counter += 1

        for future in concurrent.futures.as_completed(futures):
            complete_counter += 1
            click.secho(
                f"[{Fore.CYAN}{complete_counter}{Style.RESET_ALL}/{total_counter}]"
                f"{Fore.YELLOW} {future.result()} {Style.RESET_ALL}"
            )
