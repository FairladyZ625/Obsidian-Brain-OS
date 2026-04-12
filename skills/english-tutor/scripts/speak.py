#!/usr/bin/env python3
"""
English Tutor - Text-to-Speech Script
Uses edge-tts to generate spoken audio from text for English learning.

Usage:
    python3 speak.py "<text>" --voice en-US-GuyNeural --rate -10% --output output.mp3

Supported voices (recommended for English learning):
    Male US: en-US-GuyNeural, en-US-EricNeural, en-US-AndrewNeural, en-US-BrianNeural
    Female US: en-US-JennyNeural, en-US-AriaNeural, en-US-EmmaNeural, en-US-MichelleNeural  
    Male UK: en-GB-RyanNeural, en-GB-WilliamNeural, en-GB-OliverNeural
    Female UK: en-GB-SoniaNeural, en-GB-LibbyNeural, en-GB-MaisieNeural
"""

import argparse
import asyncio
import sys

try:
    import edge_tts
except ImportError:
    print("ERROR: edge-tts not installed. Run: pip install edge-tts", file=sys.stderr)
    sys.exit(1)


async def speak(text: str, voice: str = "en-US-GuyNeural", rate: str = "-10%", 
               output: str = "/tmp/english_tutor_output.mp3"):
    """Generate speech from text using edge-tts."""
    
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    await communicate.save(output)
    print(f"✅ Audio saved to: {output}", file=sys.stderr)
    return output


def main():
    parser = argparse.ArgumentParser(description="TTS for English learning")
    parser.add_argument("text", help="Text to speak")
    parser.add_argument("--voice", default="en-US-GuyNeural", help="Edge TTS voice name")
    parser.add_argument("--rate", default="-10%", help="Speech rate (e.g., -10%, +0%, +10%)")
    parser.add_argument("--output", default="/tmp/english_tutor_output.mp3", help="Output file path")
    
    args = parser.parse_args()
    asyncio.run(speak(args.text, args.voice, args.rate, args.output))


if __name__ == "__main__":
    main()
