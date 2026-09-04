#!/usr/bin/env python3
"""Find every account connection an agent on this machine can already use. Read-only, names and states only.

  connections.py inventory [--home DIR] [--json]
  connections.py inventory --host <ssh alias> [--json]      # runs this same file on the remote host

Three kinds: connector and vendor CLIs on PATH with their sign-in state, MCP servers configured per
harness, and secret stores. Values, tokens, URLs with keys, and account identities are never printed;
a status command's output is used only for its exit code.
"""
from __future__ import annotations
import argparse, json, os, re, shutil, subprocess, sys

# name, status command (read-only, exit 0 means signed in), what it is
CLIS = [
    ("composio", ["composio", "whoami"], "connector layer for many apps"),
    ("gog", ["gog", "auth", "list"], "Google CLI: Gmail, Calendar, Drive"),
    ("gh", ["gh", "auth", "status"], "GitHub CLI"),
    ("glab", ["glab", "auth", "status"], "GitLab CLI"),
    ("xurl", ["xurl", "auth", "status"], "X API CLI"),
    ("gcloud", ["gcloud", "auth", "list", "--format=value(account)"], "Google Cloud CLI"),
    ("az", ["az", "account", "show"], "Azure CLI"),
    ("vercel", ["vercel", "whoami"], "Vercel CLI"),
    ("wrangler", ["wrangler", "whoami"], "Cloudflare CLI"),
    ("stripe", ["stripe", "config", "--list"], "Stripe CLI"),
    ("slack", ["slack", "auth", "list"], "Slack CLI"),
    ("himalaya", ["himalaya", "account", "list"], "IMAP mail CLI"),
    ("infisical", ["infisical", "user", "get", "token"], "secret store"),
    ("op", ["op", "account", "list"], "secret store (1Password)"),
    ("bw", ["bw", "status"], "secret store (Bitwarden)"),
    ("vault", ["vault", "token", "lookup"], "secret store (HashiCorp)"),
    ("doppler", ["doppler", "me"], "secret store (Doppler)"),
]
# harness, config file relative to home, how to read server names
MCP_CONFIGS = [
    ("claude-code", ".claude.json", "json:mcpServers"),
    ("claude-code", ".claude/settings.json", "json:mcpServers"),
    ("codex", ".codex/config.toml", "toml:mcp_servers"),
    ("opencode", ".config/opencode/opencode.json", "json:mcp"),
    ("cursor", ".cursor/mcp.json", "json:mcpServers"),
    ("gemini-cli", ".gemini/settings.json", "json:mcpServers"),
    ("hermes", ".hermes/config.yaml", "yaml:mcp_servers"),
]


def cli_rows(home):
    rows = []
    for name, cmd, what in CLIS:
        if not shutil.which(cmd[0]): continue
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=12, env=dict(os.environ, HOME=home))
            status = "signed in" if proc.returncode == 0 else "present, not signed in"
        except (subprocess.TimeoutExpired, OSError): status = "present, state unknown"
        rows.append({"kind": "cli", "name": name, "status": status, "what": what, "harness": None, "where": shutil.which(cmd[0])})
    return rows


def mcp_names(path, how):
    kind, key = how.split(":", 1)
    text = open(path, encoding="utf-8").read()
    if kind == "json":
        data = json.loads(text); node = data.get(key) or {}
        return sorted(k for k in node) if isinstance(node, dict) else []
    if kind == "toml":
        try:
            import tomllib
            data = tomllib.loads(text); node = data.get(key) or {}
            return sorted(k for k in node) if isinstance(node, dict) else []
        except Exception:
            return sorted(set(re.findall(rf"^\[{re.escape(key)}\.([A-Za-z0-9_.-]+)\]", text, re.M)))
    if kind == "yaml":
        block = re.search(rf"^{re.escape(key)}:\s*\n((?:[ \t]+.*\n?)+)", text, re.M)
        return sorted(set(re.findall(r"^[ \t]{2,}([A-Za-z0-9_.-]+):\s*(?:\n|\{|$)", block.group(1), re.M))) if block else []
    return []


def mcp_rows(home):
    rows = []
    for harness, rel, how in MCP_CONFIGS:
        path = os.path.join(home, rel)
        if not os.path.isfile(path): continue
        try: names = mcp_names(path, how)
        except Exception as e: rows.append({"kind": "mcp", "name": f"(unreadable {rel})", "status": str(e)[:60], "what": "MCP config", "harness": harness, "where": path}); continue
        for n in names: rows.append({"kind": "mcp", "name": n, "status": "configured", "what": "MCP server", "harness": harness, "where": path})
    return rows


def inventory(home):
    home = os.path.abspath(os.path.expanduser(home))
    return cli_rows(home) + mcp_rows(home)


def table(rows, host):
    if not rows: return f"No account connections found on {host}.\n"
    out = [f"Account connections on {host}:"]
    for r in rows:
        who = f" ({r['harness']})" if r["harness"] else ""
        out.append(f"  {r['kind']:<4} {r['name']:<12} {r['status']:<24} {r['what']}{who}")
    return "\n".join(out) + "\n"


def remote(host, as_json):
    script = open(__file__, encoding="utf-8").read()
    proc = subprocess.run(["ssh", "-o", "ConnectTimeout=15", host, "python3", "-", "inventory", "--json"], input=script, capture_output=True, text=True, timeout=240)
    if proc.returncode != 0: raise SystemExit(f"remote inventory failed on {host}: {proc.stderr.strip()[:300]}")
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
