# Podcast maker

<div align="center">

[Watch a demo video](https://x.com/mcp_servers/status/1915426581524472097)
|
**[Try the service here](https://openmcp.app/apps/podcasts/)**

</div>

This MCP service provides the `make_podcast` tool. It takes two arguments `title` and `article`, generates a podcast video from it, and returns a natural language description that includes a video status link and a video download link. An agent can call this function using LLM-generated text, and then incorporate its answer into the final LLM response.

## Prerequisites

Install OpenMCP.

```
curl -sSfL 'https://raw.githubusercontent.com/decentralized-mcp/proxy/refs/heads/master/install.sh' | sudo bash
```

Install packages required by the MCP server itself.

```
pip install langdetect
pip install "mcp[cli]"
pip install cmcp
```

## The MCP server

It is in the [tools.py](tools.py) file.

```
cp .env.example .env
```

Edit the `.env` file to use your own Gaia node services.

## Start an SSE server

The server is started on port 8081 using the OpenMCP proxy tool.

```
openmcp run -p 0.0.0.0:8081 -- python3 tools.py
```

## Test the SSE server

Run the `cmcp` tool like `curl` to request a list of tools supported in this SSE server.

```
cmcp http://localhost:8081 tools/list
```

It gives the `make_podcast` tool spec in JSON format.

```
{
  "tools": [
    {
      "name": "make_podcast",
      "description": "Create a video podcast for the input title and article. Returns URL links to check the status and download the file video file.",
      "inputSchema": {
        "required": [
          "title",
          "article"
        ],
      }
    }
  ]
}
```

Call the `make_podcast` tool to generate a podcast episode from an article.

```
cmcp http://localhost:8081 tools/call -d '{"name": "make_podcast", "arguments": {"title": "Rare earths in America", "article": "The US has a single rare earths mine. Chinese export limits are energizing a push for more. America’s only rare earths mine heard from anxious companies soon after China responded to President Donald Trump’s tariffs this month by limiting exports of those minerals used for military applications and in many high-tech devices. “Based on the number of phone calls we’re receiving, the effects have been immediate,” said Matt Sloustcher, a spokesperson for MP Materials, the company that runs the Mountain Pass mine in California’s Mojave Desert. The trade war between the world’s two biggest economies could lead to a critical shortage of rare earth elements if China maintains its export controls long-term or expands them to seek an advantage in any trade negotiations. The California mine can’t meet all of the U.S. demand for rare earths, which is why Trump is trying to clear the way for new mines. Rare earth elements are important ingredients in electric vehicles, powerful magnets, advanced fighter jets, submarines, smartphones, television screens and many other products. Despite their name, the 17 elements aren’t actually rare, but it’s hard to find them in a high enough concentration to make a mine worth the investment."}}'
```

The response is as follows.

```
{
  "meta": null,
  "content": [
    {
      "type": "text",
      "text": "Your podcast video is in process.\n* Check its status at https://openmcp.app/apps/podcasts/?task_id=148\n* Once it is done, download the MP4 video file at http://159.138.158.109:8005/download/task_148.mp4",
      "annotations": null
    }
  ],
  "isError": false
}
```

