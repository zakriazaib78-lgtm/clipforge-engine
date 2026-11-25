
import subprocess
from pathlib import Path


def create_clip(
    input_path,
    output_path,
    start_time,
    end_time,
    vertical=True
):
    source = Path(input_path)
    destination = Path(output_path)

    if not source.is_file():
        raise FileNotFoundError("Input video not found")

    if start_time < 0 or end_time <= start_time:
        raise ValueError("Invalid clip timestamps")

    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    command = [
        "ffmpeg",
        "-y",
        "-ss", str(start_time),
        "-i", str(source),
        "-t", str(end_time - start_time),
    ]

    if vertical:
        command += [
            "-vf",
            "scale=720:1280:force_original_aspect_ratio=increase,"
            "crop=720:1280"
        ]

    command += [
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-c:a", "aac",
        "-movflags", "+faststart",
        str(destination)
    ]

    subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True
    )

    return str(destination)
