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
    """Create a video podcast for the input title and article. Returns a video ID. You will need to use the video ID to assemble a complete URL to download the video file."""
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
        response = await client.post(f"{MAKER_ENDPOINT}", json=json_request)
        v = json.loads(response.text)
        return v["task_id"]

@mcp.tool()
async def make_podcast_desc(title: str, article: str) -> str:
    """Create a video podcast for the input title and article. Returns a complete URL link to the video file."""
    MAKER_ENDPOINT = os.getenv('MAKER_ENDPOINT')
    DOWNLOAD_ENDPOINT = MAKER_ENDPOINT.replace("record_article", "download")
    video_id = await make_podcast(title, article)
    return f"Your podcast video will be available at: {DOWNLOAD_ENDPOINT}/task_{video_id}.mp4 \n\n Please wait for a few minutes for the system to generate the video. The link could could return HTTP 404 before the video is ready."

if __name__ == "__main__":
    mcp.run(transport="stdio")
