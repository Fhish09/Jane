"""
Speech-to-Text Engine using OpenAI Whisper (local, free)
"""

import tempfile
import os
from typing import Optional
from backend.config import config


class STTEngine:
    """Local speech recognition using Whisper. Completely free!"""

    def __init__(self):
        import whisper
        self.model_name = config.WHISPER_MODEL
        print(f"🎤 Loading Whisper model: {self.model_name}...")
        self.model = whisper.load_model(self.model_name)
        print("✅ Whisper loaded!")

    def transcribe(self, audio_data: bytes) -> dict:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_data)
            tmp_path = tmp.name

        try:
            result = self.model.transcribe(
                tmp_path,
                language=None,
                task="transcribe",
                fp16=False
            )

            return {
                "text": result["text"].strip(),
                "language": result.get("language", "unknown"),
                "confidence": result.get("confidence", 0.0),
                "segments": result.get("segments", [])
            }

        except Exception as e:
            print(f"❌ STT Error: {e}")
            return {"text": "", "language": "unknown", "confidence": 0.0}

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def transcribe_file(self, filepath: str) -> dict:
        try:
            result = self.model.transcribe(
                filepath,
                language=None,
                task="transcribe",
                fp16=False
            )

            return {
                "text": result["text"].strip(),
                "language": result.get("language", "unknown"),
                "confidence": 0.0
            }

        except Exception as e:
            print(f"❌ STT Error: {e}")
            return {"text": "", "language": "unknown", "confidence": 0.0}


_stt_engine = None

def get_stt_engine():
    global _stt_engine
    if _stt_engine is None:
        _stt_engine = STTEngine()
    return _stt_engine
