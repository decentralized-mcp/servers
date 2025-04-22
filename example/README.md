# Example

## Prerequisites

```
pip install "mcp[cli]"
pip install mcp-proxy
pip install cmcp
```

Get an `OPENWEATHERMAP_API_KEY` [from here](https://openweathermap.org/api)

## The MCP server

It is in the [tools.py](tools.py) file.
It uses the [FastMCP](https://github.com/jlowin/fastmcp) package in the [official MCP SDK](https://github.com/modelcontextprotocol/python-sdk) to construct the server.
Notice that we will start the server in the `STDIO` mode if it is started directly from a Python command.

```
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Start an SSE server

The server is started on port 8081 using the [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) tool.

```
mcp-proxy --sse-host=0.0.0.0 --sse-port=8081 -- python3 tools.py OPENWEATHERMAP_API_KEY
```

Of course, you can start the MCP server in local `STDIO` mode as well.

```
python3 tools.py OPENWEATHERMAP_API_KEY
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
      "name": "calculate_bmi",
      "description": "Calculate BMI given weight in kg and height in meters",
      "inputSchema": {
        "properties": {
          "weight_kg": {
            "title": "Weight Kg",
            "type": "number"
          },
          "height_m": {
            "title": "Height M",
            "type": "number"
          }
        },
        "required": [
          "weight_kg",
          "height_m"
        ],
        "title": "calculate_bmiArguments",
        "type": "object"
      }
    },
    {
      "name": "fetch_weather",
      "description": "Fetch current weather for a city",
      "inputSchema": {
        "properties": {
          "city": {
            "title": "City",
            "type": "string"
          }
        },
        "required": [
          "city"
        ],
        "title": "fetch_weatherArguments",
        "type": "object"
      }
    }
  ]
}
```

Call a tool.

```
cmcp http://localhost:8081 tools/call -d '{"name": "calculate_bmi", "arguments": {"weight_kg": 120.0, "height_m": 1.85}}'
```

The result.

```
{
  "meta": null,
  "content": [
    {
      "type": "text",
      "text": "35.06208911614317",
      "annotations": null
    }
  ],
  "isError": false
}
```

Call another tool.

```
cmcp http://localhost:8081 tools/call -d '{"name": "fetch_weather", "arguments": {"city": "Austin, Texas"}}'
```

The result.

```
{
  "meta": null,
  "content": [
    {
      "type": "text",
      "text": "Temperature: 24.94C, feels like 25.34C. clear sky",
      "annotations": null
    }
  ],
  "isError": false
}
```

