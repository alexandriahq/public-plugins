# Alexandria plugins

Connect [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Cursor](https://docs.cursor.com), and other Agent Plugins clients to [Alexandria](https://alexandria.so).

## Install

**Claude Code**

```text
/plugin marketplace add alexandriahq/public-plugins
/plugin install ambient-context@alexandria
/plugin install ambient-multiplayer@alexandria
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
https://lighthouse-server-production-de2c.up.railway.app/v1/me/mcp
```

After install, authenticate in the client with a Multiplayer user access token (`mp_…` from Settings → Access). Do not put tokens in this repository.

Manual setup in any Streamable HTTP client:

```json
{
  "mcpServers": {
    "multiplayer": {
      "url": "https://lighthouse-server-production-de2c.up.railway.app/v1/me/mcp"
    }
  }
}
```

## Plugins in this marketplace

| Plugin | MCP |
| --- | --- |
| `ambient-context` | `http://127.0.0.1:8765/mcp` |
| `ambient-multiplayer` | `https://lighthouse-server-production-de2c.up.railway.app/v1/me/mcp` |

Any Agent Plugins client can also load `plugins/ambient-context/` or `plugins/ambient-multiplayer/` as a plugin root.
