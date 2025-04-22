import httpx
import sys
import json
import os
from dotenv import load_dotenv
from langdetect import detect
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("Podcast maker")

@mcp.tool()
async def make_podcast(title: str, article: str) -> str:
    """Create a video podcast for the input title and article. Returns URL links to check the status and download the file video file."""
    MAKER_ENDPOINT = os.getenv('MAKER_ENDPOINT')
    LLM_ENDPOINT = os.getenv('LLM_ENDPOINT')
    LLM_APIKEY = os.getenv('LLM_APIKEY')
    TTS_ENDPOINT = os.getenv('TTS_ENDPOINT')
    SPEAKER_1 = os.getenv('SPEAKER_1')
    SPEAKER_2 = os.getenv('SPEAKER_2')

    if detect(article).lower().startswith('zh'):
        lang = "ZH"
    else:
        lang = "EN" 

    json_request = {
        "callback_url": "",
        "xtuis_token": "",
        "llm_backend": {
            "url": f"{LLM_ENDPOINT}",
            "token": f"Bearer {LLM_APIKEY}"
        },
        "only_audio": False,
        "language": f"{lang}",
        "tts_engine": {
            "type": "GSV",
            "url": f"{TTS_ENDPOINT}"
        },
        "scene_index": 0,
        "speaker1": f"{SPEAKER_1}",
        "speaker2": f"{SPEAKER_2}",
        "podcast_prompt": "",
        "title": f"{title}",
        "article": f"{article}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{MAKER_ENDPOINT}/record_article", json=json_request)
        v = json.loads(response.text)
        task_id = v["task_id"]
        return f"Your podcast video is in process.\n* Check its status at https://openmcp.app/apps/podcasts/?task_id={task_id}\n* Once it is done, download the MP4 video file at {MAKER_ENDPOINT}/download/task_{task_id}.mp4"

if __name__ == "__main__":
    mcp.run(transport="stdio")
