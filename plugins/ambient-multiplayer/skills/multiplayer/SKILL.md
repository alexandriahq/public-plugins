---
name: multiplayer
description: "Use when an agent needs organization-shared Ambient context: list groups, search memories, list trajectories, inspect connectors, or publish a Prepare batch through the Multiplayer MCP server."
---

# Ambient Multiplayer

Multiplayer is the org-side store for published Ambient context. HTTP JSON is the product API; this plugin exposes the same resources over MCP 2026-07-28.

Connects to the hosted Streamable HTTP server:

```text
https://multiplayer-server-production-de2c.up.railway.app/v1/mcp
```

The client authenticates after install with a user PAT (`mp_…` from Settings → Access). Never put a bearer token, WorkOS session, or user PAT in plugin files or MCP `headers`. `/v1/me/mcp` is the desktop WorkOS path, not this plugin.

## Privacy Boundary

- Sealed fields stay ciphertext on the wire. Decrypt locally when the org uses customer KMS or sealed envelopes.
- Do not invent an `orgId` for WorkOS or user-PAT callers. The server stamps identity from the credential.
- Root (service token without a user header) is the admin class on this same URL and must pass `orgId`. Prefer a user PAT (`mp_…`) for Codex / Claude Code.

## Discovery Workflow

1. Call `list_groups` first. An organization is many groups (Sales, Engineering).
2. Pass `teamId` to `search_org_memories` and `list_org_trajectories`. `teamId=mine` uses the caller's group.
3. Call `list_connectors` to see live MCP destinations versus a planned private database. A private database is a Multiplayer destination, not Ambient.
4. Use `publish_batch` only for a frozen Prepare bundle, the same contract as `POST /v1/me/publish`.

## Response Guidance

- Ground answers in returned memories and trajectories. Do not treat Multiplayer as a live remote Ambient Feed.
- If a tool is denied, the org's owner/group/other MCP mode is the gate — do not retry with a guessed `orgId`.
