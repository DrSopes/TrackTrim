from .core import detect_content_bounds, inspect_mp3, trim_song
from .exceptions import TrackTrimError, NoContentDetectedError, InvalidFormatError
from .models import AudioInfo, DetectionResult, TrimResult

__all__ = [
    "AudioInfo",
    "DetectionResult",
    "TrimResult",
    "TrackTrimError",
    "NoContentDetectedError",
    "InvalidFormatError",
    "inspect_mp3",
    "detect_content_bounds",
    "trim_song",
]

__version__ = "0.1.2"