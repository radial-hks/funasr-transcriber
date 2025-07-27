# -*- encoding: utf-8 -*-
import asyncio
import json
import ssl
import websockets

async def transcribe(audio_bytes: bytes, server: str, port: int) -> str:
    """
    Connects to a FunASR WebSocket server and transcribes the given audio bytes.
    """
    uri = f"wss://{server}:{port}"

    async with websockets.connect(uri, subprotocols=["binary"], ping_interval=None) as websocket:
        # Send connection header
        await websocket.send(json.dumps({
            "mode": "offline",
            "chunk_size": [5, 10, 5],
            "chunk_interval": 10,
            "wav_name": "dify-plugin",
            "is_speaking": True,
        }))

        # Send audio data in chunks
        stride = 960  # 60ms * 16000Hz * 1 channel * 2 bytes/sample / 1000
        for i in range(0, len(audio_bytes), stride):
            await websocket.send(audio_bytes[i:i+stride])
            await asyncio.sleep(0.01)  # Simulate real-time streaming

        # Send end-of-speech signal
        await websocket.send(json.dumps({"is_speaking": False}))

        # Receive transcription results
        full_text = ""
        while True:
            try:
                message = await websocket.recv()
                result = json.loads(message)
                if result.get("text"):
                    full_text += result["text"]
                if result.get("is_final"):
                    break
            except websockets.exceptions.ConnectionClosed:
                break

        return full_text