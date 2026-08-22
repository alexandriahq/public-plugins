# Alexandria public plugins

[Agent Plugins 1.0.0](https://agent-plugins.org/specification) marketplace for
Alexandria. Packaging only — no business logic.

| Plugin | What it loads | Needs |
| --- | --- | --- |
| `ambient-context` | Read-only local Ambient vault over loopback MCP | Ambient desktop running (`http://127.0.0.1:8765/mcp`) |
| `ambient-multiplayer` | Org memories / trajectories / publish | `multiplayer-mcp` on PATH after `multiplayer-mcp login` |

Product behavior stays in [`alexandriahq/ambient`](https://github.com/alexandriahq/ambient)
([agent-plugins.md](https://github.com/alexandriahq/ambient/blob/main/docs/app/agent-plugins.md)).
The packages here are the published copies.

## Install

**Claude Code**

```text
/plugin marketplace add alexandriahq/public-plugins
/plugin install ambient-context@alexandria
/plugin install ambient-multiplayer@alexandria
```

**Cursor**

Dashboard → Settings → Plugins → Import Marketplace, then paste
`https://github.com/alexandriahq/public-plugins`. Cursor reads
`.cursor-plugin/marketplace.json`.

**Any Agent Plugins client**

Load `plugins/ambient-context/` or `plugins/ambient-multiplayer/` as a plugin
root (`plugin.json` + `mcp.json` + `skills/*/SKILL.md`).

## Layout

Agent Plugins 1.0 is the portable core. Distribution files for Claude Code and
Cursor are generated from it — the spec does not define a marketplace format.

```text
marketplace.json                 # marketplace identity
plugins/<name>/
  plugin.json                    # Agent Plugins 1.0 manifest  ← edit this
  mcp.json                       # portable MCP
  skills/<skill>/SKILL.md
  .claude-plugin/plugin.json     # generated
  .cursor-plugin/plugin.json     # generated
.claude-plugin/marketplace.json  # generated
.cursor-plugin/marketplace.json  # generated
scripts/sync.py
```

```bash
python3 scripts/sync.py          # validate + write generated manifests
python3 scripts/sync.py --check  # CI: fail if generated files drifted
```

Do not put bearer tokens, WorkOS sessions, or PATs in `mcp.json` `headers` or
`env`. Multiplayer auth is `~/.multiplayer/` after login. Ambient Context MCP
is loopback-only.

## Source packages

| Marketplace plugin | Source in `alexandriahq/ambient` |
| --- | --- |
| `ambient-context` | `ambient-app/agent-plugin/` |
| `ambient-multiplayer` | `multiplayer-server/agent-plugin/` |
