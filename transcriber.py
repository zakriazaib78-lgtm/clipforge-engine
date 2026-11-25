
import whisper
import os

_model = None

def load_model(model_size="base"):
    global _model

    if _model is None:
        _model = whisper.load_model(model_size)

    return _model


def transcribe_audio(audio_path, model_size="base"):
    if not os.path.exists(audio_path):
        raise FileNotFoundError("Audio file not found")

    model = load_model(model_size)

    result = model.transcribe(
        audio_path,
        verbose=False
    )

    segments = []

    for item in result.get("segments", []):
        text = item.get("text", "").strip()

        if not text:
            continue

        segments.append({
            "start": float(item["start"]),
            "end": float(item["end"]),
            "text": text
        })

    return segments
