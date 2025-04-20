# Podcast maker

## Prerequisites

```
pip install "mcp[cli]"
pip install mcp-proxy
pip install cmcp
```

## The MCP server

It is in the [tools.py](tools.py) file.

```
cp .env.example .env
```

Edit the `.env` file to use your own Gaia node services.

## Start an SSE server

The server is started on port 8081 using the [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) tool.

```
mcp-proxy --sse-port=8081 -- python3 tools.py
```

## Test the SSE server

Run the `cmcp` tool like `curl` to request a list of tools supported in this SSE server.

```
cmcp http://localhost:8081 tools/list
```

It gives the list in JSON format.

```
{
  "meta": null,
  "nextCursor": null,
  "tools": [
    {
      "name": "make_podcast",
      "description": "Create a video podcast for the input title and article",
      "inputSchema": {
        "properties": {
          "title": {
            "title": "Title",
            "type": "string"
          },
          "article": {
            "title": "Article",
            "type": "string"
          }
        },
        "required": [
          "title",
          "article"
        ],
        "title": "make_podcastArguments",
        "type": "object"
      }
    }
  ]
}
```

Call the tool to generate a podcast episode from an article.

```
cmcp http://localhost:8081 tools/call -d '{"name": "make_podcast", "arguments": {"title": "Rare earths in America", "article": "The US has a single rare earths mine. Chinese export limits are energizing a push for more. America’s only rare earths mine heard from anxious companies soon after China responded to President Donald Trump’s tariffs this month by limiting exports of those minerals used for military applications and in many high-tech devices. “Based on the number of phone calls we’re receiving, the effects have been immediate,” said Matt Sloustcher, a spokesperson for MP Materials, the company that runs the Mountain Pass mine in California’s Mojave Desert. The trade war between the world’s two biggest economies could lead to a critical shortage of rare earth elements if China maintains its export controls long-term or expands them to seek an advantage in any trade negotiations. The California mine can’t meet all of the U.S. demand for rare earths, which is why Trump is trying to clear the way for new mines. Rare earth elements are important ingredients in electric vehicles, powerful magnets, advanced fighter jets, submarines, smartphones, television screens and many other products. Despite their name, the 17 elements aren’t actually rare, but it’s hard to find them in a high enough concentration to make a mine worth the investment."}}'
```

The results is a task ID.

```
{
  "meta": null,
  "content": [
    {
      "type": "text",
      "text": "127",
      "annotations": null
    }
  ],
  "isError": false
}
```

The agent can check the status of the task.

```
curl http://159.138.158.109:8005/tasks/127
```

Or, load the URL in their browser: `https://openmcp.app/apps/podcasts/?task_id=127`

Upon completion, download the podcast video file.

```
curl -LO http://159.138.158.109:8005/download/task_127.mp4
```

