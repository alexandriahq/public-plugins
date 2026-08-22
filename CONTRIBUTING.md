# Contributing

This repository is the public marketplace. Edit the portable package under `plugins/<name>/`, then regenerate client catalogs:

```bash
python3 scripts/sync.py          # validate + write generated manifests
python3 scripts/sync.py --check  # CI: fail if generated files drifted
```

```text
marketplace.json                 # marketplace identity
plugins/<name>/
  plugin.json                    # Agent Plugins 1.0 manifest
  mcp.json                       # portable MCP
  skills/<skill>/SKILL.md
  .claude-plugin/plugin.json     # generated
  .cursor-plugin/plugin.json     # generated
.claude-plugin/marketplace.json  # generated
.cursor-plugin/marketplace.json  # generated
```

Do not put bearer tokens, WorkOS sessions, or user PATs in `mcp.json` `headers` or `env`.
