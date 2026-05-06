# TrackTrim

TrackTrim is a Python library for trimming leading and trailing silence from MP3 songs while preserving MP3 output and common ID3 metadata.

## Features

- Detects non-silent content at the beginning and end of a track
- Trims MP3 files and writes MP3 output
- Preserves common metadata and cover art through ID3 tag copying
- Uses a stable bitrate policy for predictable output size and quality
- Designed to be imported from other Python scripts

## Installation

### From GitHub

```bash
pip install git+https://github.com/DrSopes/tracktrim.git
```

### Local editable install

```bash
pip install -e .
```

## Usage

```python
from tracktrim import trim_song, detect_content_bounds

info = detect_content_bounds("song.mp3", top_db=35)
print(info)

result = trim_song(
    "song.mp3",
    "song_trimmed.mp3",
    top_db=35,
)
print(result)
```

## Bitrate policy

TrackTrim uses a simple stable output policy:

- source bitrate <= 192 kbps -> output 192 kbps
- source bitrate 193 to 288 kbps -> output 256 kbps
- source bitrate > 288 kbps -> output 320 kbps

This avoids unpredictable VBR output and keeps file sizes consistent.

## Development

Create a virtual environment and install the project in editable mode:

```bash
python -m venv .venv
```

On Windows CMD:

```bash
.venv\Scripts\activate
```

Then install:

```bash
pip install -e .
```

## Build

```bash
python -m pip install --upgrade build
python -m build
```

This creates distribution files in `dist/`.

## Publishing

This repository can publish to PyPI automatically through GitHub Actions using Trusted Publishing.

## License

This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).