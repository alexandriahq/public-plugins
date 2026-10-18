# Alexandria plugins

Connect [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Cursor](https://docs.cursor.com), and other Agent Plugins clients to [Alexandria](https://alexandria.so).

## Install

**Claude Code**

```text
/plugin marketplace add alexandriahq/public-plugins
/plugin install ambient-context@alexandria
/plugin install confidential-nodes@alexandria
```

**Cursor**

Settings → Plugins → Import Marketplace, then paste `https://github.com/alexandriahq/public-plugins`.

## Ambient Context

Read-only local vault: current intents, redacted evidence, and markdown memory. The ambient-report skill uses the separately installed ambient-diagnostics command for bounded support reports. It checks the installed schema and loads the matching offline playbook; older apps without that command retain the public-vault workflow.

The Ambient desktop app serves MCP at `http://127.0.0.1:8765/mcp`. Open Ambient, then use the plugin.

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
| `confidential-nodes` | `https://confidentialnodes.com/public-mcp` |

Any Agent Plugins client can also load a directory under `plugins/` as a plugin root.
