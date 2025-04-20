import httpx
import sys
import json
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("Podcast maker")

@mcp.tool()
async def make_podcast(title: str, article: str) -> str:
    """Create a video podcast for the input title and article"""
    MAKER_ENDPOINT = os.getenv('MAKER_ENDPOINT')
    LLM_ENDPOINT = os.getenv('LLM_ENDPOINT')
    LLM_APIKEY = os.getenv('LLM_APIKEY')
    TTS_ENDPOINT = os.getenv('TTS_ENDPOINT')
    SPEAKER_1 = os.getenv('SPEAKER_1')
    SPEAKER_2 = os.getenv('SPEAKER_2')

    json_request = {
        "only_audio": False,
        "language": "EN",
        "title": f"{title}",
        "tts_engine": {
            "type": "GSV",
            "url": f"{TTS_ENDPOINT}"
        },
        "callback_url": "",
        "xtuis_token":"",
        "speaker1": [
            "Noah",
            f"{SPEAKER_1}"
        ],
        "speaker2": [
            "Emma",
            f"{SPEAKER_2}"
        ],
        "llm_backend": {
            "url": f"{LLM_ENDPOINT}",
            "token": f"Bearer {LLM_APIKEY}"
        },
        "article": f"{article}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{MAKER_ENDPOINT}", json=json_request)
        v = json.loads(response.text)
        return v["task_id"]

if __name__ == "__main__":
    mcp.run(transport="stdio")
