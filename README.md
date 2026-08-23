# Alexandria plugins

Connect [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Cursor](https://docs.cursor.com), and other Agent Plugins clients to [Alexandria](https://alexandria.so).

## Install

**Claude Code**

```text
/plugin marketplace add alexandriahq/public-plugins
/plugin install ambient-context@alexandria
/plugin install ambient-multiplayer@alexandria
/plugin install confidential-nodes@alexandria
```

**Cursor**

Settings → Plugins → Import Marketplace, then paste `https://github.com/alexandriahq/public-plugins`.

## Ambient Context

Read-only local vault: current intents, redacted evidence, and markdown memory.

The Ambient desktop app serves MCP at `http://127.0.0.1:8765/mcp`. Open Ambient, then use the plugin.

## Ambient Multiplayer

Organization memories, trajectories, connectors, and publish.

Hosted Streamable HTTP:

```text
https://lighthouse-server-production-de2c.up.railway.app/v1/mcp
```

After install, authenticate in the client with a Multiplayer user access token (`mp_…` from Settings → Access). Do not put tokens in this repository.

Manual setup in any Streamable HTTP client:

```json
{
  "mcpServers": {
    "multiplayer": {
      "url": "https://lighthouse-server-production-de2c.up.railway.app/v1/mcp"
    }
  }
}
```

## Confidential Nodes

Search public confidential-compute GPU listings without signing in. Submitting a buyer requirement or seller quote uses the MCP client's OAuth flow and requires a verified Confidential Nodes account.

Hosted Streamable HTTP:

```text
https://confidentialnodes.com/public-mcp
```

## Plugins in this marketplace

| Plugin | MCP |
| --- | --- |
| `ambient-context` | `http://127.0.0.1:8765/mcp` |
| `ambient-multiplayer` | `https://lighthouse-server-production-de2c.up.railway.app/v1/mcp` |
| `confidential-nodes` | `https://confidentialnodes.com/public-mcp` |

Any Agent Plugins client can also load a directory under `plugins/` as a plugin root.
