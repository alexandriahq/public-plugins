---
name: ambient-context
description: "Use when an agent needs read-only Ambient workspace memory: discover current tasks/intents, inspect redacted evidence, or read markdown memory through the in-app Ambient Context MCP or the ambient-context CLI."
---

# Ambient Context

Ambient exposes an agent-visible local context vault. Prefer the in-app Ambient Context MCP (`http://127.0.0.1:8765/mcp`) when Ambient is running. The PATH `ambient-context` CLI is a compatibility fallback. Start with Markdown and follow its links. Do not look up opaque intent or handoff ids.

## Privacy Boundary

- Call MCP `vault_path` or run `ambient-context vault path` to locate the public vault, then read `README.md` first and `intents/_current.md` second.
- The public vault is not Ambient's private app library. Never discover or open `ambient.sqlite`, database generations, capture artifacts, screenshots, audio, keystrokes, raw outputs, or artifact paths.
- Generated intent and chunk Markdown is read-only. Do not edit, rename, delete, or regenerate it with shell/file tools.
- Memory files under `memories/projects/`, `memories/people/`, and `memories/workflows/` are user-visible and editable, but mutations must use Ambient's host-mediated memory tools so stable IDs, compare-and-swap, links, and the SQL index stay consistent. Do not mutate them directly with shell/file tools.
- New links use ordinary Markdown links. Follow links when they materially improve the answer; do not crawl the whole vault by default.
- Cite titles, vault paths, and timestamps when summarizing evidence. Do not ask the user for intent or handoff ids.

## Discovery Workflow

1. Call MCP `vault_path` or run `ambient-context vault path`, open `README.md`, then open `intents/_current.md`.
2. Follow the relevant intent's Markdown links to evidence chunks or memories.
3. Call MCP `list` with `kind=intent` (or `kind=memory`), or run `ambient-context list --kind intent`.
4. Call MCP `search` with a query, or run `ambient-context search <query> --json`.
5. Call MCP `show` with a title or relative vault path such as `intents/_current.md`, or run `ambient-context show "<title or vault path>" --json`.
6. Call MCP `backlinks` when reverse relationships matter, or run `ambient-context backlinks "<title or vault path>" --json`.
7. Call MCP `validate`, or run `ambient-context validate --json`, when links, generated ownership, or projection freshness appear inconsistent.

## Response Guidance

- MCP and CLI are public-vault-only. They have no private database path flags, private profile discovery, or mutation commands.
- Prefer the in-app HTTP MCP when Ambient is running. Prefer direct Markdown reads for normal context and JSON only when parsing tool or CLI results.
- If status says the public vault is not ready, ask the user to open Ambient and wait for projection, then retry MCP `status`.
- Ground summaries in projected context and linked evidence. Zero semantic links is valid; never invent a relationship just to add a link.
