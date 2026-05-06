# TrackTrim

TrackTrim is a Python library and CLI for trimming leading and trailing silence from MP3 songs.

It detects the first and last non-silent regions of a track, trims the file, writes MP3 output, and preserves common ID3 metadata.

## Features

- Detect leading and trailing silence
- MP3 input to MP3 output
- Preserve common metadata and cover art
- Stable bitrate policy for predictable output size
- Public Python API and command-line interface

## Installation

### PyPI

```bash
pip install tracktrim
```

### GitHub

```bash
pip install git+https://github.com/DrSopes/TrackTrim.git
```

## Python API

```python
from tracktrim import inspect_mp3, detect_content_bounds, trim_song

info = inspect_mp3("song.mp3")
print(info)

bounds = detect_content_bounds("song.mp3", top_db=35)
print(bounds)

result = trim_song("song.mp3", "song_trimmed.mp3", top_db=35)
print(result)
```

## CLI

```bash
tracktrim input.mp3 output.mp3 --top-db 35
```

Optional bitrate override:

```bash
tracktrim input.mp3 output.mp3 --bitrate 320
```

## Bitrate policy

TrackTrim uses a stable default policy:

- source bitrate <= 192 kbps -> output 192 kbps
- source bitrate 193 to 288 kbps -> output 256 kbps
- source bitrate > 288 kbps -> output 320 kbps

## Development

```bash
python -m venv .venv
```

Windows CMD:

```bash
.venv\Scripts\activate
```

Install in editable mode:

```bash
pip install -e .
```

## Build

```bash
python -m pip install --upgrade build
python -m build
```

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).