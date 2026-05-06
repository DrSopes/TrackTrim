import argparse
from .core import trim_song


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tracktrim",
        description="Trim leading and trailing silence from MP3 files.",
    )
    parser.add_argument("input", help="Input MP3 file")
    parser.add_argument("output", help="Output MP3 file")
    parser.add_argument("--top-db", type=float, default=35.0, help="Silence threshold in dB")
    parser.add_argument("--frame-length", type=int, default=2048, help="Frame length")
    parser.add_argument("--hop-length", type=int, default=512, help="Hop length")
    parser.add_argument("--bitrate", type=int, default=None, help="Optional output bitrate in kbps")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    result = trim_song(
        input_path=args.input,
        output_path=args.output,
        top_db=args.top_db,
        frame_length=args.frame_length,
        hop_length=args.hop_length,
        target_bitrate_kbps=args.bitrate,
    )

    print(result)
    return 0