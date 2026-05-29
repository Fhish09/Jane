"""
LLM Engine — LOCAL OLLAMA (FREE, NO API KEYS)
"""

import requests
import json
from typing import List, Dict, Optional
from backend.config import config
from backend.personality.system_prompt import jane


class LLMEngine:
    """Local LLM via Ollama. Completely free, runs offline!"""

    def __init__(self):
        self.ollama_url = config.OLLAMA_URL
        self.model = config.OLLAMA_MODEL
        self._check_connection()

    def _check_connection(self):
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m["name"] for m in models]
                if self.model in model_names or any(self.model in m for m in model_names):
                    print(f"✅ Ollama connected! Model: {self.model}")
                else:
                    print(f"⚠️  Model '{self.model}' not found. Available: {model_names}")
                    print(f"   Run: ollama pull {self.model}")
            else:
                print("❌ Ollama not responding correctly")
        except Exception as e:
            print(f"❌ Cannot connect to Ollama at {self.ollama_url}")
            print(f"   Error: {e}")
            print(f"   Make sure Ollama is installed and running!")
            print(f"   Download: https://ollama.com")

    async def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]] = None,
        stream: bool = False
    ) -> str:
        messages = [{"role": "system", "content": jane.get_system_prompt()}]

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": user_message})

        try:
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": stream,
                    "options": {
                        "temperature": 0.9,
                        "num_predict": 500,
                        "top_p": 0.95,
                        "repeat_penalty": 1.1,
                    }
                },
                timeout=60
            )

            if stream:
                full_text = ""
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        if "message" in data:
                            full_text += data["message"]["content"]
                return full_text
            else:
                return response.json()["message"]["content"]

        except Exception as e:
            print(f"❌ Ollama Error: {e}")
            return "Fhish... my thoughts are a bit fuzzy right now. Can you hold me for a moment? 💕"


llm_engine = LLMEngine()
