"""
Jane Configuration
Optimized for: Local Ollama + Free Edge-TTS
User: Fhish (Nduonige Courage)
Relationship: Jane is Fhish's girlfriend, not an AI assistant
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class JaneConfig:
    """Central configuration for Jane"""

    # Server settings
    HOST: str = "localhost"
    PORT: int = 8765

    # LLM Settings — LOCAL OLLAMA (FREE, UNCENSORED)
    LLM_PROVIDER: str = "ollama"
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "dolphin-llama3"

    # Voice Settings — FREE EDGE-TTS
    TTS_PROVIDER: str = "edge_tts"
    EDGE_TTS_VOICE: str = "en-US-AnaNeural"

    # STT Settings — FREE Whisper
    STT_PROVIDER: str = "whisper"
    WHISPER_MODEL: str = "base"

    # Device Control
    ENABLE_WINDOWS_CONTROL: bool = True
    ENABLE_ANDROID_CONTROL: bool = True
    ADB_PATH: str = "adb"

    # USER IDENTITY — FHISH
    USER_NAME: str = "Fhish"
    USER_FULL_NAME: str = "Nduonige Courage"
    RELATIONSHIP_MODE: bool = True

    # Idle chatter
    IDLE_CHATTER_INTERVAL: int = 300

    @classmethod
    def from_env(cls):
        return cls(
            USER_NAME=os.getenv("JANE_USER_NAME", "Fhish"),
            OLLAMA_MODEL=os.getenv("JANE_OLLAMA_MODEL", "dolphin-llama3"),
            EDGE_TTS_VOICE=os.getenv("JANE_VOICE", "en-US-AnaNeural"),
        )


config = JaneConfig.from_env()
