"""
Simple test client for Jane
Run this to chat with Jane before building the Electron frontend
"""

import asyncio
import websockets
import json


async def chat_with_jane():
    uri = "ws://localhost:8765"

    print("💕 Connecting to Jane...")
    async with websockets.connect(uri) as websocket:
        welcome = await websocket.recv()
        data = json.loads(welcome)
        print(f"\n🌸 Jane: {data['message']}")

        while True:
            print("\n" + "="*40)
            message = input("Fhish: ")

            if message.lower() in ['exit', 'quit', 'bye']:
                print("👋 Goodbye Fhish!")
                break

            await websocket.send(json.dumps({
                "type": "text",
                "content": message
            }))

            response = await websocket.recv()
            data = json.loads(response)

            print(f"\n🌸 Jane ({data.get('emotion', 'calm')}): {data['text']}")

            if data.get('audio_url'):
                print(f"   🎙️  Audio generated: {data['audio_url']}")


if __name__ == "__main__":
    try:
        asyncio.run(chat_with_jane())
    except KeyboardInterrupt:
        print("\n👋 Bye Fhish!")
    except ConnectionRefusedError:
        print("\n❌ Cannot connect to Jane. Make sure the server is running!")
        print("   Run: python -m backend.server")
