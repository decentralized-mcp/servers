# GitHub PR reviewer

**[Try the service here](https://openmcp.app/apps/pr-reviewer/)**

This MCP service provides two tools.

* The `review` tool takes a single argument `pr_url`, the public URL for a GitHub Pull Request, and returns the review in markdown text.
* The `content` tool takes a single argument `pr_url`, and returns the cotent for all files and patches in this PR.

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

It gives the list of tools.

```
{
  "tools": [
    {
      "name": "review",
      "description": "Generate a review for the input GitHub Pull Request (PR) URL.",
      "inputSchema": {
        "required": [
          "pr_url"
        ],
      }
    },
    {
      "name": "content",
      "description": "Get file and patch content for the input GitHub Pull Request (PR) URL.",
      "inputSchema": {
        "required": [
          "pr_url"
        ],
      }
    }
  ]
}
```

Call the `review` tool to review a GitHub Pull Request.

```
cmcp http://localhost:8081 tools/call -d '{"name": "review", "arguments": {"pr_url":"https://github.com/WasmEdge/WasmEdge/pull/4083"}}'
```

The results is the review in markdown format

```
{
  "meta": null,
  "content": [
    {
      "type": "text",
      "text": "## [.github/workflows/misc-linters.yml](https://github.com/WasmEdge/WasmEdge/blob/4d37fe6a61fa82a1c19e283672c0bd14a41ab90b/.github%2Fworkflows%2Fmisc-linters.yml)\n\n**Major Issues:**\n\n*   **`linelint` job failure on PRs from forks:** The `git diff` command in the `Get changed files` step attempts to access `origin/$BASE_REF`. On pull requests *from forks*, `origin` will not exist, causing this script to fail. It should gracefully handle cases where `origin/$BASE_REF` is unavailable (e.g., using a default value or skipping linelint on PRs from forks).\n\n**Minor Issues:**\n\n*   **Unnecessary Checkout in `linelint`**: The `linelint` job checks out the code again, duplicating the checkout step already present in the main `misc` job. This is redundant and increases workflow execution time.  Consider using the workspace from the initial checkout.\n*    **Hardcoded branch name origin/$BASE_REF**: It may be more robust to use `${{ github.event.pull_request.base.ref }}` instead of relying on potentially incorrect `origin/$BASE_REF` in pull request scenarios, particularly forks.\n\n## [.linelint.yml](https://github.com/WasmEdge/WasmEdge/blob/4d37fe6a61fa82a1c19e283672c0bd14a41ab90b/.linelint.yml)\n\nThe patch and the resulting code are identical: a new `.linelint.yml` file is added with basic configuration for `linelint`.\n\n**Issues:**\n\n1.  **No functional change, only addition of config.** This isn't inherently *wrong*, but warrants questioning if this commit adds value on its own or should have been bundled with another feature/change.\n2.  **Limited Configuration:** The current configuration only enforces a single newline at the end of files. Consider adding more rules to enforce consistent code style.\n3. **Missing shebang**: While not strictly required for YAML, consider adding `---` at the beginning of the file for explicit document separation in some tools/editors.\n\n",
      "annotations": null
    }
  ],
  "isError": false
}
```

Call the `content` tool to get file and patch content from a GitHub Pull Request.

```
cmcp http://localhost:8081 tools/call -d '{"name": "content", "arguments": {"pr_url":"https://github.com/WasmEdge/WasmEdge/pull/4083"}}'
```

The results is the raw content.


```
{ 
  "meta": null,
  "content": [
    {
      "type": "text",
      "text": "The filename is Cargo.toml\n\n<code>...</code>\n\n<patch>...</patch>",
      "annotations": null
    }
  ],
  "isError": false
}
```

## Add the MCP server to Claude for Desktop

Since Claude for Desktop only supports STDIO natively, we'll need to install `mcp-remote` to enable SSE compatibility.

First, install the package on your machine:
```
npm i mcp-remote
```

Next, update your `claude_desktop_config.json` with the following configuration:

```
{
  "mcpServers": {
    "github-pr-review-openmcp": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:8081/sse"]
    }
  }
}
```

After that, restart Claude for Desktop. You should now be able to connect to and use the MCP server via SSE.

