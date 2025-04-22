import httpx
import sys
import json
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("GitHub Pull Request reviewer")

def parse_github_pr_url(url):
    """
    Parse GitHub pull request URL to extract owner, repo, and PR number.
    
    Args:
        url (str): GitHub pull request URL (e.g., 'https://github.com/WasmEdge/WasmEdge/pull/3835')
    
    Returns:
        tuple: (owner, repo, pr_number) or None if URL is invalid
    """
    try:
        # Split URL by '/' and filter out empty strings
        parts = [part for part in url.split('/') if part]
        
        # Check if URL has the expected structure
        if len(parts) == 6 and parts[4] == 'pull':
            owner = parts[2]
            repo = parts[3]
            pr_number = parts[5]
            return owner, repo, pr_number
        return None
    except Exception:
        return None


@mcp.tool()
async def review(pr_url: str) -> str:
    """Generate a review for the input GitHub Pull Request (PR) URL."""
    FLOWS_ENDPOINT = os.getenv('FLOWS_ENDPOINT')
    LLM_ENDPOINT = os.getenv('LLM_ENDPOINT')
    LLM_APIKEY = os.getenv('LLM_APIKEY')
    LLM_CTX_SIZE = os.getenv('LLM_CTX_SIZE')

    result = parse_github_pr_url(pr_url) 
    if result:
        owner, repo, pr_number = result
    else:
        return "The pr_url is not valid"

    json_request = {
        "github_owner": f"{owner}",
        "github_repo": f"{repo}",
        "github_pr_number": int(pr_number),
        "llm_api_endpoint": f"{LLM_ENDPOINT}",
        "llm_ctx_size": int(LLM_CTX_SIZE),
        "llm_model_name": "default",
        "llm_api_key": f"{LLM_APIKEY}",
        "system_prompt": "",
        "review_prompt": ""
    }

    async with httpx.AsyncClient(timeout=600.0) as client:
        response = await client.post(f"{FLOWS_ENDPOINT}/review", json=json_request)
        return response.text

@mcp.tool()
async def content(pr_url: str) -> str:
    """Get file and patch content for the input GitHub Pull Request (PR) URL."""
    FLOWS_ENDPOINT = os.getenv('FLOWS_ENDPOINT')

    result = parse_github_pr_url(pr_url)
    if result:
        owner, repo, pr_number = result
    else:
        return "The pr_url is not valid"

    json_request = {
        "github_owner": f"{owner}",
        "github_repo": f"{repo}",
        "github_pr_number": int(pr_number)
    }

    async with httpx.AsyncClient(timeout=600.0) as client:
        response = await client.post(f"{FLOWS_ENDPOINT}/content", json=json_request)
        return response.text

if __name__ == "__main__":
    mcp.run(transport="stdio")
