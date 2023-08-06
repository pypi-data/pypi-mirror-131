import click
from vidsnap.utils import run_video_extractor


@click.command()
@click.option("-i", "--input_path", help="Directory where the videos are located")
@click.option("-o", "--output_path", help="Directory where the snapshots will be stored")
@click.option(
    "-e",
    "--extension",
    "video_extension",
    help="Extension for the videos to process. (e.g. MP4)",
)
@click.option("-w", "--workers", default=4, help="Amount of threadworkers to spawn")
@click.option(
    "-s",
    "--seconds",
    "snap_every_x",
    default=120,
    help="Amount of seconds between every snap per video.",
)
def main(
    input_path: str = "./",
    output_path: str = "./snaps/",
    video_extension: str = "mp4",
    workers: int = 4,
    snap_every_x: int = 120,
):
    run_video_extractor(input_path, output_path, video_extension, workers, snap_every_x)


if __name__ == "__main__":
    main()
