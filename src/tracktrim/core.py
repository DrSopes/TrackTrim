from pathlib import Path

import librosa
import numpy as np
import soundfile as sf
import lameenc

from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen.mp3 import MP3


def detect_content_bounds(
    input_path: str | Path,
    top_db: float = 35,
    frame_length: int = 2048,
    hop_length: int = 512,
):
    input_path = Path(input_path)

    y, sr = librosa.load(str(input_path), sr=None, mono=False)

    intervals = librosa.effects.split(
        y,
        top_db=top_db,
        frame_length=frame_length,
        hop_length=hop_length,
    )

    if len(intervals) == 0:
        raise ValueError("No non-silent content detected.")

    start_sample = int(intervals[0][0])
    end_sample = int(intervals[-1][1])

    return {
        "sample_rate": sr,
        "start_sample": start_sample,
        "end_sample": end_sample,
        "start_sec": start_sample / sr,
        "end_sec": end_sample / sr,
    }


def _load_audio_preserve_sr(input_path: Path):
    data, sr = sf.read(str(input_path), always_2d=True, dtype="float32")
    return data, sr


def _float_to_pcm16_interleaved(data: np.ndarray) -> bytes:
    clipped = np.clip(data, -1.0, 1.0)
    pcm16 = (clipped * 32767.0).astype(np.int16)
    return pcm16.tobytes()


def _copy_id3_tags(src_mp3: Path, dst_mp3: Path) -> bool:
    try:
        tags = ID3(str(src_mp3))
        tags.save(str(dst_mp3), v2_version=3)
        return True
    except ID3NoHeaderError:
        return False


def _read_mp3_info(path: Path) -> dict:
    audio = MP3(str(path))
    info = audio.info
    return {
        "bitrate_kbps": int(round(info.bitrate / 1000)),
        "duration_sec": float(info.length),
        "bitrate_mode": str(getattr(info, "bitrate_mode", None)),
        "sample_rate": getattr(info, "sample_rate", None),
        "channels": getattr(info, "channels", None),
    }


def _choose_target_bitrate(source_bitrate_kbps: int) -> tuple[int, str]:
    if source_bitrate_kbps <= 192:
        return 192, "band_<=192_to_192"
    if source_bitrate_kbps <= 288:
        return 256, "band_193_288_to_256"
    return 320, "band_>288_to_320"


def _encode_mp3_cbr(trimmed_data: np.ndarray, sr: int, bitrate_kbps: int) -> bytes:
    channels = trimmed_data.shape[1]

    encoder = lameenc.Encoder()
    encoder.set_bit_rate(bitrate_kbps)
    encoder.set_in_sample_rate(sr)
    encoder.set_channels(channels)
    encoder.set_quality(2)

    pcm_bytes = _float_to_pcm16_interleaved(trimmed_data)
    mp3_data = encoder.encode(pcm_bytes)
    mp3_data += encoder.flush()
    return mp3_data


def trim_song(
    input_path: str | Path,
    output_path: str | Path,
    top_db: float = 35,
    frame_length: int = 2048,
    hop_length: int = 512,
    target_bitrate_kbps: int | None = None,
):
    input_path = Path(input_path)
    output_path = Path(output_path)

    if input_path.suffix.lower() != ".mp3" or output_path.suffix.lower() != ".mp3":
        raise ValueError("Input and output must be .mp3 files.")

    before_info = _read_mp3_info(input_path)
    data, sr = _load_audio_preserve_sr(input_path)

    if data.shape[1] == 1:
        y_for_detect = data[:, 0]
    else:
        y_for_detect = data.T

    intervals = librosa.effects.split(
        y_for_detect,
        top_db=top_db,
        frame_length=frame_length,
        hop_length=hop_length,
    )

    if len(intervals) == 0:
        raise ValueError("No non-silent content detected.")

    start_sample = int(intervals[0][0])
    end_sample = int(intervals[-1][1])

    trimmed = data[start_sample:end_sample, :]

    if trimmed.size == 0:
        raise ValueError("Trimmed audio is empty.")

    if target_bitrate_kbps is None:
        final_bitrate_kbps, bitrate_strategy = _choose_target_bitrate(before_info["bitrate_kbps"])
    else:
        final_bitrate_kbps = int(target_bitrate_kbps)
        bitrate_strategy = "manual_override"

    mp3_bytes = _encode_mp3_cbr(trimmed, sr, final_bitrate_kbps)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(mp3_bytes)

    metadata_ok = _copy_id3_tags(input_path, output_path)
    after_info = _read_mp3_info(output_path)

    return {
        "input": str(input_path),
        "output": str(output_path),
        "sample_rate": sr,
        "channels": int(trimmed.shape[1]),
        "start_sample": start_sample,
        "end_sample": end_sample,
        "start_sec": start_sample / sr,
        "end_sec": end_sample / sr,
        "original_duration_sec": before_info["duration_sec"],
        "trimmed_duration_sec": trimmed.shape[0] / sr,
        "source_bitrate_kbps": before_info["bitrate_kbps"],
        "source_bitrate_mode": before_info["bitrate_mode"],
        "target_bitrate_kbps": final_bitrate_kbps,
        "bitrate_strategy": bitrate_strategy,
        "output_bitrate_kbps": after_info["bitrate_kbps"],
        "output_bitrate_mode": after_info["bitrate_mode"],
        "metadata_ok": metadata_ok,
    }