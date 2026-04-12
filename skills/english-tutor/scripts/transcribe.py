#!/usr/bin/env python3
"""
English Tutor - Audio Transcription Script
Uses faster-whisper to transcribe audio files for English learning.

Usage:
    python3 transcribe.py <audio_path> [--lang en] [--model tiny] [--format json|text]

Output: JSON (default) or plain text transcription with timestamps
"""

import argparse
import json
import sys
from faster_whisper import WhisperModel


def transcribe(audio_path: str, language: str = "en", model_size: str = "tiny", output_format: str = "json"):
    """Transcribe audio file using faster-whisper."""
    
    print(f"🎧 Loading model: {model_size}...", file=sys.stderr)
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    
    print(f"📝 Transcribing: {audio_path}", file=sys.stderr)
    segments, info = model.transcribe(audio_path, language=language)
    
    results = []
    full_text = []
    
    for segment in segments:
        entry = {
            "start": round(segment.start, 1),
            "end": round(segment.end, 1),
            "text": segment.text.strip()
        }
        results.append(entry)
        full_text.append(entry["text"])
    
    output = {
        "file": audio_path,
        "language": info.language,
        "language_probability": round(info.language_probability, 2),
        "model": model_size,
        "segments": results,
        "full_text": "\n".join(full_text)
    }
    
    if output_format == "json":
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(output["full_text"])
    
    return output


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio for English learning")
    parser.add_argument("audio_path", help="Path to audio file (mp3/m4a/wav/etc)")
    parser.add_argument("--lang", default="en", help="Language code (default: en)")
    parser.add_argument("--model", default="tiny", choices=["tiny", "base", "small", "medium", "large-v3"], 
                        help="Whisper model size (default: tiny)")
    parser.add_argument("--format", dest="output_format", default="json", choices=["json", "text"],
                        help="Output format (default: json)")
    
    args = parser.parse_args()
    transcribe(args.audio_path, args.lang, args.model, args.output_format)


if __name__ == "__main__":
    main()
