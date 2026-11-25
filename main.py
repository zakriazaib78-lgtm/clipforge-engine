
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI(
    title="ClipForge AI Engine",
    description="Our own AI video clipping backend",
    version="0.1.0"
)

class VideoRequest(BaseModel):
    video_url: HttpUrl

@app.get("/")
def home():
    return {
        "message": "Welcome to ClipForge AI Engine",
        "status": "running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/analyze-url")
def analyze_video(request: VideoRequest):
    return {
        "message": "Video URL received",
        "video_url": str(request.video_url),
        "processing": "not_started",
        "next_step": "Connect authorized video processing"
    }
