from dataclasses import dataclass


@dataclass(slots=True)
class DetectionResult:
    sample_rate: int
    start_sample: int
    end_sample: int
    start_sec: float
    end_sec: float


@dataclass(slots=True)
class AudioInfo:
    bitrate_kbps: int
    duration_sec: float
    bitrate_mode: str
    sample_rate: int | None
    channels: int | None
    size_bytes: int
    size_mb: float


@dataclass(slots=True)
class TrimResult:
    input: str
    output: str
    sample_rate: int
    channels: int
    start_sample: int
    end_sample: int
    start_sec: float
    end_sec: float
    original_duration_sec: float
    trimmed_duration_sec: float
    source_bitrate_kbps: int
    source_bitrate_mode: str
    target_bitrate_kbps: int
    bitrate_strategy: str
    output_bitrate_kbps: int
    output_bitrate_mode: str
    metadata_ok: bool