"""
Text-to-Speech Engine using FREE Microsoft Edge-TTS
High-quality neural voices, no API key needed!
"""

import asyncio
import edge_tts
import os
from typing import Optional
from backend.config import config


class TTSEngine:
    """Free TTS using Edge-TTS (Microsoft voices). No API keys!"""

    VOICE_PROFILES = {
        "jane_default": "en-US-AnaNeural",
        "jane_warm": "en-US-JennyNeural",
        "jane_soft": "en-GB-SoniaNeural",
        "jane_playful": "en-US-AriaNeural",
        "jane_shy": "en-US-AnaNeural",
    }

    def __init__(self):
        self.voice = config.EDGE_TTS_VOICE
        self.output_dir = "backend/voice/audio_cache"
        os.makedirs(self.output_dir, exist_ok=True)
        self.audio_counter = 0

    async def speak(self, text: str, emotion: str = "calm") -> str:
        clean_text = self._clean_text_for_speech(text)
        voice = self._select_voice(emotion)

        self.audio_counter += 1
        filename = f"jane_{self.audio_counter:04d}.mp3"
        filepath = os.path.join(self.output_dir, filename)

        try:
            communicate = edge_tts.Communicate(clean_text, voice)
            await communicate.save(filepath)
            print(f"🎙️  Generated audio: {filename} (voice: {voice})")
            return filepath

        except Exception as e:
            print(f"❌ TTS Error: {e}")
            return None

    def _clean_text_for_speech(self, text: str) -> str:
        import re
        text = re.sub(r'\*[^*]+\*', '', text)
        text = re.sub(r'[😀-🙏🌀-🗿🚀-🛿🇠-🇿]+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        text = text.replace("...", ", ")
        return text

    def _select_voice(self, emotion: str) -> str:
        emotion_voice_map = {
            "happy": "en-US-AriaNeural",
            "loving": "en-US-AnaNeural",
            "shy": "en-US-AnaNeural",
            "sad": "en-GB-SoniaNeural",
            "hurt": "en-GB-SoniaNeural",
            "calm": "en-US-JennyNeural",
            "excited": "en-US-AriaNeural",
            "pout": "en-US-AnaNeural",
            "unresponsive": "en-GB-SoniaNeural",
        }
        return emotion_voice_map.get(emotion, self.voice)

    async def list_available_voices(self):
        voices = await edge_tts.list_voices()
        female_english = [
            v for v in voices 
            if v["Gender"] == "Female" and "en-" in v["Locale"]
        ]

        print("\n🎙️  Available Female English Voices for Jane:")
        print("-" * 60)
        for v in female_english[:10]:
            print(f"  {v['ShortName']} — {v['Locale']}")
        print("-" * 60)

        return female_english


tts_engine = TTSEngine()
