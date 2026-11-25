
import subprocess
from pathlib import Path

from config import TEMP_DIR, OUTPUT_DIR, MAX_CLIPS
from transcriber import transcribe_audio
from detector import score_segment
from video_editor import create_clip


def extract_audio(video_path, audio_path):
    command = [
        "ffmpeg",
        "-y",
        "-i", str(video_path),
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        str(audio_path)
    ]

    subprocess.run(
        command,
        check=True,
        capture_output=True
    )


def find_highlights(segments, min_duration=15, max_duration=60):
    candidates = []

    for i, first in enumerate(segments):
        selected = []

        for segment in segments[i:]:
            selected.append(segment)

            duration = (
                selected[-1]["end"] - first["start"]
            )

            if duration > max_duration:
                break

            if duration >= min_duration:
                transcript = " ".join(
                    item["text"] for item in selected
                )

                candidates.append({
                    "start": first["start"],
                    "end": selected[-1]["end"],
                    "duration": round(duration, 2),
                    "transcript": transcript,
                    "score": score_segment(transcript)
                })

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    chosen = []

    for candidate in candidates:
        overlaps = any(
            candidate["start"] < item["end"]
            and candidate["end"] > item["start"]
            for item in chosen
        )

        if not overlaps:
            chosen.append(candidate)

        if len(chosen) >= MAX_CLIPS:
            break

    return chosen


def process_video(video_path):
    video_path = Path(video_path)

    if not video_path.is_file():
        raise FileNotFoundError("Video file not found")

    audio_path = TEMP_DIR / "audio.wav"

    extract_audio(video_path, audio_path)

    segments = transcribe_audio(str(audio_path))

    if not segments:
        return []

    highlights = find_highlights(segments)

    results = []

    for index, clip in enumerate(highlights, start=1):
        output_path = OUTPUT_DIR / f"clip_{index}.mp4"

        create_clip(
            str(video_path),
            str(output_path),
            clip["start"],
            clip["end"],
            vertical=True
        )

        results.append({
            "clip_id": index,
            "start_time": clip["start"],
            "end_time": clip["end"],
            "duration": clip["duration"],
            "score": clip["score"],
            "transcript": clip["transcript"],
            "file": str(output_path)
        })

    return results
