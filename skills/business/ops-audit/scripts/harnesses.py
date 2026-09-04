#!/usr/bin/env python3
"""Find every agent harness with session records on a machine. Read-only, metadata only.

  harnesses.py inventory [--home DIR] [--json]
  harnesses.py inventory --host <ssh alias> [--json]      # runs this same file on the remote host

Known harnesses come from a table of published storage conventions. Anything else with a
sessions-like folder full of records is reported as "unknown" so the owner can name it.
Nothing is opened beyond file names, sizes, and modification times.
"""
from __future__ import annotations
import argparse, datetime as dt, glob, json, os, subprocess, sys

# name, roots (globs relative to home), record glob inside a root, format
KNOWN = [
    ("claude-code", ["~/.claude/projects", "~/Library/Application Support/Claude/claude-code-sessions", "~/Library/Application Support/Claude/local-agent-mode-sessions"], "**/*.jsonl", "jsonl"),
    ("codex", ["~/.codex/sessions", "~/.codex/archived_sessions"], "**/*.jsonl", "jsonl"),
    ("pi-agent", ["~/.pi/agent/sessions"], "**/*.jsonl", "jsonl"),
    ("oh-my-pi", ["~/.omp/agent/sessions", "~/.omp/profiles/*/agent/sessions"], "**/*.jsonl", "jsonl"),
    ("hermes", ["~/.hermes/sessions", "~/.hermes*/profiles/*/sessions"], "*.jsonl", "jsonl"),
    ("hermes-state", ["~/.hermes"], "state.db", "sqlite"),
    ("gemini-cli", ["~/.gemini/tmp"], "**/*.json", "json"),
    ("qwen-code", ["~/.qwen/tmp"], "*/chats/session-*.json", "json"),
    ("cursor", ["~/Library/Application Support/Cursor/User", "~/.config/Cursor/User"], "**/state.vscdb", "sqlite"),
    ("chatgpt-desktop", ["~/Library/Application Support/com.openai.chat"], "**/*.json", "json"),
    ("aider", ["~"], ".aider.chat.history.md", "markdown"),
    ("copilot-cli", ["~/.copilot/session-state", "~/.copilot/history-session-state"], "**/*", "jsonl"),
    ("opencode", ["~/.local/share/opencode"], "opencode.db", "sqlite"),
    ("openclaw", ["~/.openclaw/agents/*/sessions"], "**/*.jsonl", "jsonl"),
    ("clawdbot", ["~/.clawdbot/sessions"], "**/*.jsonl", "jsonl"),
    ("amp", ["~/.local/share/amp"], "**/*", "mixed"),
    ("vibe", ["~/.vibe/logs/session"], "*/messages.jsonl", "jsonl"),
    ("goose", ["~/.local/share/goose/sessions", "~/.goose/sessions"], "**/*", "mixed"),
    ("crush", ["~/.crush"], "crush.db", "sqlite"),
    ("kimi-code", ["~/.kimi-code/sessions", "~/.kimi/sessions"], "**/wire.jsonl", "jsonl"),
    ("muse-code", ["~/.local/share/muse/sessions"], "**/session.jsonl", "jsonl"),
    ("factory-droid", ["~/.factory/sessions"], "**/*.jsonl", "jsonl"),
    ("antigravity", ["~/.gemini/antigravity-cli/brain"], "*/.system_generated/logs/transcript.jsonl", "jsonl"),
    ("openhands", ["~/.openhands/conversations"], "*/events/*.json", "json"),
    ("grok-build", ["~/.grok/sessions"], "*/*/chat_history.jsonl", "jsonl"),
]
GENERIC_DIRS = ("sessions", "transcripts", "conversations", "chats", "history")
GENERIC_EXT = (".jsonl", ".json", ".db", ".sqlite", ".md")
SKIP = ("/Library/Caches", "node_modules", "/.git/", "chromium-profile", "chrome-profile", "Session Storage", "/Sessions/", "/.mutagen/", "/nvim/", "/.Trash/")


def scan_root(root, pattern):
    files = [f for f in glob.glob(os.path.join(glob.escape(root), pattern), recursive=True) if os.path.isfile(f)]
    if not files: return None
    stats = [(os.path.getsize(f), os.path.getmtime(f)) for f in files]
    return {"files": len(files), "bytes": sum(s for s, _ in stats), "oldest": dt.date.fromtimestamp(min(m for _, m in stats)).isoformat(), "newest": dt.date.fromtimestamp(max(m for _, m in stats)).isoformat()}


def inventory(home):
    home = os.path.abspath(os.path.expanduser(home)); home_real = os.path.realpath(home); found = []; claimed = set()
    for name, roots, pattern, fmt in KNOWN:
        for root_glob in roots:
            for root in glob.glob(glob.escape(home) + root_glob[1:]):
                if not os.path.isdir(root) and not os.path.isfile(root): continue
                stat = scan_root(root, pattern) if os.path.isdir(root) else scan_root(os.path.dirname(root), os.path.basename(root))
                if stat:
                    found.append({"harness": name, "root": root, "format": fmt, **stat})
                    if os.path.realpath(root) != home_real: claimed.add(os.path.realpath(root))  # a store rooted at home must not claim the whole home
    # Generic fallback: a sessions-like folder under a dot directory, holding records, not already claimed.
    for dot in sorted(glob.glob(os.path.join(glob.escape(home), ".*"))):
        if not os.path.isdir(dot) or any(s in dot for s in SKIP): continue
        for cur, dirs, files in os.walk(dot):
            depth = cur[len(dot):].count(os.sep)
            if depth > 3: dirs[:] = []; continue
            if any(s in cur for s in SKIP): dirs[:] = []; continue
            if os.path.basename(cur).lower() in GENERIC_DIRS and os.path.realpath(cur) not in claimed and not any(os.path.realpath(cur).startswith(c + os.sep) for c in claimed):
                records = [os.path.join(cur, f) for f in files if f.endswith(GENERIC_EXT)]
                if len(records) >= 3:
                    stat = scan_root(cur, "**/*")
                    found.append({"harness": "unknown", "root": cur, "format": "mixed", **stat}); claimed.add(os.path.realpath(cur)); dirs[:] = []
    return found


def table(rows, host):
    if not rows: return f"No agent session stores found on {host}.\n"
    width = max(len(r["harness"]) for r in rows)
    out = [f"Agent session stores on {host}:"]
    for r in rows:
        out.append(f"  {r['harness']:<{width}}  {r['files']:>6} files  {r['bytes'] / 1e6:8.1f} MB  {r['oldest']} to {r['newest']}  {r['root']}")
    return "\n".join(out) + "\n"


def remote(host, as_json):
    script = open(__file__, encoding="utf-8").read()
    proc = subprocess.run(["ssh", "-o", "ConnectTimeout=15", host, "python3", "-", "inventory", "--json"], input=script, capture_output=True, text=True, timeout=180)
    if proc.returncode != 0: raise SystemExit(f"remote inventory failed on {host}: {proc.stderr.strip()[:300]}")
    # A login banner or MOTD may precede the JSON; take the first list that decodes.
    dec = json.JSONDecoder(); rows = None
    for i, ch in enumerate(proc.stdout):
        if ch == "[":
            try: rows, _ = dec.raw_decode(proc.stdout, i); break
            except ValueError: continue
    if rows is None: raise SystemExit(f"remote inventory on {host} returned no list: {proc.stdout.strip()[:300]}")
    for r in rows: r["host"] = host
    return json.dumps(rows, indent=1) if as_json else table(rows, host)


def main():
    p = argparse.ArgumentParser(); q = p.add_subparsers(dest="cmd", required=True)
    a = q.add_parser("inventory"); a.add_argument("--home", default="~"); a.add_argument("--host"); a.add_argument("--json", action="store_true")
    a = p.parse_args()
    if a.host: sys.stdout.write(remote(a.host, a.json)); return
    rows = inventory(a.home)
    for r in rows: r["host"] = "local"
    sys.stdout.write(json.dumps(rows, indent=1) if a.json else table(rows, "this machine"))


if __name__ == "__main__": main()
