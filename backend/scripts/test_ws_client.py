import asyncio
import websockets
import os

async def test():
    # Construct an absolute path or correct relative path to the file
    file_path = os.path.join(os.path.dirname(__file__), "..", "..", "ml", "data", "demo_test_set", "sample1_pair0_mismatched_small_room_vs_medium_room.wav")
    async with websockets.connect("ws://localhost:8000/ws/predict") as ws:
        with open(file_path, "rb") as f:
            await ws.send(f.read())
        async for message in ws:
            print(message)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
