#!/usr/bin/env python3
"""Validate Agent Plugins 1.0 packages and emit Claude Code + Cursor manifests.

Source of truth per plugin: plugins/<name>/plugin.json + skills/ + mcp.json
Generated (do not hand-edit):
  plugins/<name>/.claude-plugin/plugin.json
  plugins/<name>/.cursor-plugin/plugin.json
  .claude-plugin/marketplace.json
  .cursor-plugin/marketplace.json

Usage:
  python3 scripts/sync.py         # validate + write generated files
  python3 scripts/sync.py --check # fail if generated files are stale
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SPEC_VERSION = "1.0.0"
PLUGIN_SCHEMA = f"https://agent-plugins.org/schemas/{SPEC_VERSION}/plugin.schema.json"
MCP_SCHEMA = f"https://agent-plugins.org/schemas/{SPEC_VERSION}/mcp.schema.json"
MANIFEST_FIELDS = {
    "$schema", "name", "version", "description", "author",
    "homepage", "repository", "license", "keywords", "extensions",
}
AUTHOR_FIELDS = {"name", "email", "url"}
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9.-]{0,62}[a-z0-9])?$")
STDIO_FIELDS = {"type", "command", "args", "env", "cwd"}
REMOTE_FIELDS = {"type", "url", "headers"}
ROOT = Path(__file__).resolve().parent.parent


class Problems:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


def read_json(path: Path, problems: Problems, where: str):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        problems.error(where, f"unreadable JSON ({exc})")
        return None


def frontmatter(text: str):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fields = {}
    for line in text[3:end].splitlines():
        line = line.split("#", 1)[0].rstrip()
        if not line or line.startswith(" ") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip("'\"")
    return fields


def validate_manifest(manifest, where: str, problems: Problems) -> bool:
    if not isinstance(manifest, dict):
        problems.error(where, "manifest must be a JSON object")
        return False
    fatal = False
    for key in sorted(set(manifest) - MANIFEST_FIELDS):
        problems.warn(where, f"unknown top-level field '{key}' (put client data under 'extensions')")
    if manifest.get("$schema") != PLUGIN_SCHEMA:
        problems.error(where, f"$schema must be '{PLUGIN_SCHEMA}'")
        fatal = True
    name = manifest.get("name")
    if not isinstance(name, str) or not NAME_RE.match(name) or "--" in name or ".." in name:
        problems.error(where, f"invalid name {name!r}")
        fatal = True
    for key in ("version", "description", "homepage", "repository", "license"):
        if key in manifest and not isinstance(manifest[key], str):
            problems.error(where, f"'{key}' must be a string")
            fatal = True
    author = manifest.get("author")
    if author is not None:
        if not isinstance(author, dict):
            problems.error(where, "'author' must be an object")
            fatal = True
        else:
            for key, value in author.items():
                if key not in AUTHOR_FIELDS or not isinstance(value, str):
                    problems.error(where, f"invalid author field '{key}'")
                    fatal = True
    keywords = manifest.get("keywords")
    if keywords is not None and not (
        isinstance(keywords, list) and all(isinstance(item, str) for item in keywords)
    ):
        problems.error(where, "'keywords' must be an array of strings")
        fatal = True
    return not fatal


def discover_skills(plugin_dir: Path, problems: Problems) -> list[str]:
    skills_dir = plugin_dir / "skills"
    if not skills_dir.exists():
        return []
    if not skills_dir.is_dir():
        problems.error(f"{plugin_dir.name}/skills", "exists but is not a directory")
        return []
    found = []
    for child in sorted(skills_dir.iterdir()):
        skill_md = child / "SKILL.md"
        if not child.is_dir() or not skill_md.is_file():
            continue
        where = f"{plugin_dir.name}/skills/{child.name}/SKILL.md"
        meta = frontmatter(skill_md.read_text())
        if meta is None or not meta.get("name") or not meta.get("description"):
            problems.error(where, "SKILL.md needs YAML frontmatter with name and description")
            continue
        if meta["name"] != child.name:
            problems.warn(where, f"frontmatter name '{meta['name']}' != directory '{child.name}'")
        found.append(child.name)
    return found


def validate_mcp(plugin_dir: Path, problems: Problems):
    path = plugin_dir / "mcp.json"
    if not path.exists():
        return None
    where = f"{plugin_dir.name}/mcp.json"
    if not path.is_file():
        problems.error(where, "exists but is not a regular file")
        return None
    config = read_json(path, problems, where)
    if config is None:
        return None
    if not isinstance(config, dict) or set(config) != {"$schema", "mcpServers"}:
        problems.error(where, "top level must be exactly {$schema, mcpServers}")
        return None
    if config["$schema"] != MCP_SCHEMA:
        problems.error(where, f"$schema must be '{MCP_SCHEMA}'")
        return None
    if not isinstance(config["mcpServers"], dict):
        problems.error(where, "'mcpServers' must be an object")
        return None
    servers = {}
    for name, server in config["mcpServers"].items():
        if validate_server(server, f"{where}[{name}]", problems):
            servers[name] = server
    return servers


def validate_server(server, where: str, problems: Problems) -> bool:
    if not isinstance(server, dict):
        problems.error(where, "server entry must be an object")
        return False
    kind = server.get("type")
    if kind == "stdio":
        if set(server) - STDIO_FIELDS:
            problems.error(where, f"unknown stdio field(s) {sorted(set(server) - STDIO_FIELDS)}")
            return False
        command = server.get("command")
        if not isinstance(command, str) or not command:
            problems.error(where, "stdio 'command' must be a non-empty string")
            return False
        bare = "/" not in command and "\\" not in command
        if not (bare or command.startswith("./")):
            problems.error(where, "'command' must be a bare name or a './' plugin-relative path")
            return False
        return True
    if kind in ("streamable-http", "sse"):
        if set(server) - REMOTE_FIELDS:
            problems.error(where, f"unknown {kind} field(s) {sorted(set(server) - REMOTE_FIELDS)}")
            return False
        url = server.get("url", "")
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            problems.error(where, "'url' must be an absolute http(s) URL")
            return False
        authority = url.split("/")[2] if len(url.split("/")) > 2 else ""
        host = authority.split(":")[0]
        if url.startswith("http://") and host not in ("localhost", "127.0.0.1", "::1"):
            problems.error(where, "non-loopback endpoints must use HTTPS")
            return False
        headers = server.get("headers", {})
        if not isinstance(headers, dict):
            problems.error(where, "'headers' must be an object")
            return False
        lowered = [name.lower() for name in headers]
        if any(name in ("authorization", "cookie", "proxy-authorization") for name in lowered):
            problems.error(where, "headers must not carry credentials")
            return False
        return True
    problems.error(where, f"unknown transport type {kind!r}")
    return False


def claude_mcp(servers):
    out = {}
    for name, server in servers.items():
        if server["type"] == "stdio":
            command = server["command"]
            entry = {
                "type": "stdio",
                "command": "${CLAUDE_PLUGIN_ROOT}/" + command[2:] if command.startswith("./") else command,
            }
            if server.get("args"):
                entry["args"] = list(server["args"])
        else:
            entry = {
                "type": "http" if server["type"] == "streamable-http" else "sse",
                "url": server["url"],
            }
            if server.get("headers"):
                entry["headers"] = dict(server["headers"])
        out[name] = entry
    return out


def client_manifest(manifest, servers):
    base = {"name": manifest["name"]}
    for key in ("description", "version", "author", "homepage", "repository", "license", "keywords"):
        if key in manifest:
            base[key] = manifest[key]
    claude = dict(base)
    if servers:
        claude["mcpServers"] = claude_mcp(servers)
    return claude, dict(base)


def build(problems: Problems) -> dict[Path, str]:
    market = read_json(ROOT / "marketplace.json", problems, "marketplace.json")
    if not isinstance(market, dict) or "name" not in market or "owner" not in market:
        problems.error("marketplace.json", "needs at least 'name' and 'owner'")
        return {}
    files = {}
    claude_entries = []
    cursor_entries = []
    plugins_root = ROOT / "plugins"
    if not plugins_root.is_dir():
        problems.error("plugins/", "directory is missing")
        return {}
    for plugin_dir in sorted(path for path in plugins_root.iterdir() if path.is_dir()):
        where = f"plugins/{plugin_dir.name}/plugin.json"
        manifest = read_json(plugin_dir / "plugin.json", problems, where)
        if manifest is None or not validate_manifest(manifest, where, problems):
            continue
        if manifest["name"] != plugin_dir.name:
            problems.error(where, f"name '{manifest['name']}' must match directory '{plugin_dir.name}'")
            continue
        skills = discover_skills(plugin_dir, problems)
        servers = validate_mcp(plugin_dir, problems)
        if not skills and not servers:
            problems.warn(f"plugins/{plugin_dir.name}", "no skills and no MCP servers")
        claude, cursor = client_manifest(manifest, servers or {})
        files[plugin_dir / ".claude-plugin" / "plugin.json"] = claude
        files[plugin_dir / ".cursor-plugin" / "plugin.json"] = cursor
        entry = {"name": manifest["name"]}
        for key in ("description", "version", "author", "license", "keywords"):
            if key in manifest:
                entry[key] = manifest[key]
        claude_entries.append({**entry, "source": f"./plugins/{plugin_dir.name}"})
        cursor_entries.append({**entry, "source": f"./plugins/{plugin_dir.name}"})
    catalog = {
        "name": market["name"],
        "owner": market["owner"],
        "metadata": {"description": market.get("description", "")},
    }
    files[ROOT / ".claude-plugin" / "marketplace.json"] = {**catalog, "plugins": claude_entries}
    files[ROOT / ".cursor-plugin" / "marketplace.json"] = {**catalog, "plugins": cursor_entries}
    return {path: json.dumps(data, indent=2) + "\n" for path, data in files.items()}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail if generated files are stale")
    args = parser.parse_args(argv)
    problems = Problems()
    files = build(problems)
    stale = [path for path, text in files.items() if not path.exists() or path.read_text() != text]
    if args.check:
        for path in stale:
            problems.error(str(path.relative_to(ROOT)), "out of date — run `python3 scripts/sync.py`")
    elif not problems.errors:
        for path, text in files.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    for warning in problems.warnings:
        print(f"warn: {warning}", file=sys.stderr)
    for error in problems.errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if problems.errors:
        return 1
    print(f"ok: {len(files)} generated file(s) {'verified' if args.check else 'written'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
