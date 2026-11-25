
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
TEMP_DIR = BASE_DIR / "temp"

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

MAX_CLIPS = 5
MIN_CLIP_DURATION = 15
MAX_CLIP_DURATION = 60

ALLOWED_VIDEO_EXTENSIONS = {
    ".mp4", ".mov", ".mkv", ".webm"
}

for directory in [UPLOAD_DIR, OUTPUT_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
