#!/usr/bin/env python3
"""Turn sampled agent sessions into bounded, redacted digests the audit can mine.

  digest.py --root DIR --harness NAME --out DIR [--recent 20] [--largest 10] [--max-chars 6000] [--min-bytes 2048]
  digest.py --self-test

One Markdown digest per sampled session: where and when, how many turns, which tools, then the
owner's turns and the agent's final message per turn, each capped. Emails, phone numbers, money,
URLs, and key-like tokens are redacted before anything is written. An index.json in the out
directory carries per-session counts and dates for the count-and-date-range step.
Parsers: claude-code, codex, pi-agent, hermes, and a generic JSONL reader for the rest.
"""
from __future__ import annotations
import argparse, datetime as dt, glob, hashlib, json, os, re, sys

RED = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "<email>"),
    (re.compile(r"(?<![\w+])\+\d{1,3}(?:[\s.-]?\(?\d{1,4}\)?){2,5}(?![\w])"), "<phone>"),
    (re.compile(r"(?<!\d)(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}(?!\d)"), "<phone>"),
    (re.compile(r"[$€£¥₹]\s?\d[\d,.]*"), "<amount>"),
    (re.compile(r"\b\d[\d,.]*\s?(?:USD|EUR|GBP|CAD|AUD|CHF|JPY|INR|SEK|NOK|DKK|kr|dollars|euros|pounds)\b"), "<amount>"),
    (re.compile(r"https?://\S+"), "<url>"),
    (re.compile(r"\b(?:sk|pk|ghp|xox[abp]|AKIA|AIza)[-_A-Za-z0-9]{12,}\b"), "<key>"),
    (re.compile(r"\b(?=[A-Za-z0-9_-]*\d)(?=[A-Za-z0-9_-]*[A-Za-z])[A-Za-z0-9_-]{24,}\b"), "<token>"),
    (re.compile(r"(?<![\w.:-])(?!\d{4}-\d{2}-\d{2}\b)\d[\d -]{6,}\d(?![\w.:-])"), "<number>"),
]


def redact(text):
    for pattern, sub in RED: text = pattern.sub(sub, text)
    return text


def cap(text, n): text = re.sub(r"\s+", " ", text or "").strip(); return text if len(text) <= n else text[:n] + " …"


def text_of(content):
    """Plain text from a string or a list of content blocks; tool names collected separately."""
    if isinstance(content, str): return content, []
    texts, tools = [], []
    if isinstance(content, list):
        for b in content:
            if isinstance(b, str): texts.append(b); continue
            if not isinstance(b, dict): continue
            t = b.get("type", "")
            if t in ("text", "input_text", "output_text") and b.get("text"): texts.append(b["text"])
            elif t in ("tool_use", "toolCall", "function_call", "tool_call") and b.get("name"): tools.append(b["name"])
            elif t == "tool_result": continue
    return "\n".join(texts), tools


def turns_claude(rows):
    for r in rows:
        if r.get("type") not in ("user", "assistant"): continue
        m = r.get("message") or {}; text, tools = text_of(m.get("content"))
        yield r["type"], text, tools, r.get("timestamp"), r.get("cwd")


def turns_codex(rows):
    cwd = None
    for r in rows:
        p = r.get("payload") or {}
        if r.get("type") == "session_meta": cwd = p.get("cwd"); continue
        if r.get("type") != "response_item": continue
        if p.get("type") == "message" and p.get("role") in ("user", "assistant"):
            text, tools = text_of(p.get("content")); yield p["role"], text, tools, r.get("timestamp"), cwd
        elif p.get("type") in ("function_call", "tool_call") and p.get("name"):
            yield "assistant", "", [p["name"]], r.get("timestamp"), cwd


def turns_pi(rows):
    cwd = None
    for r in rows:
        if r.get("type") == "session": cwd = r.get("cwd"); continue
        if r.get("type") != "message": continue
        m = r.get("message") or {}
        if m.get("role") in ("user", "assistant"):
            text, tools = text_of(m.get("content")); yield m["role"], text, tools, r.get("timestamp"), cwd


def turns_generic(rows):
    for r in rows:
        role = r.get("role") or r.get("type") or (r.get("message") or {}).get("role")
        if role not in ("user", "assistant"): continue
        content = r.get("content") if "content" in r else (r.get("message") or {}).get("content")
        text, tools = text_of(content)
        for k in ("tool_calls", "toolCalls"):
            for c in r.get(k) or []:
                name = (c.get("function") or {}).get("name") or c.get("name")
                if name: tools.append(name)
        yield role, text, tools, r.get("timestamp") or r.get("ts") or r.get("time"), r.get("cwd")


PARSERS = {"claude-code": turns_claude, "codex": turns_codex, "pi-agent": turns_pi, "oh-my-pi": turns_pi, "hermes": turns_generic}


def read_jsonl(path):
    with open(path, "rb") as f:
        for line in f:
            try: yield json.loads(line)
            except Exception: continue


def digest_one(path, harness, max_chars):
    parser = PARSERS.get(harness, turns_generic)
    turns = list(parser(read_jsonl(path)))
    stamps = [t[3] for t in turns if t[3]]; cwds = [t[4] for t in turns if t[4]]
    tools = {}
    for _, _, names, _, _ in turns:
        for n in names: tools[n] = tools.get(n, 0) + 1
    user_turns = [(txt, ts) for role, txt, _, ts, _ in turns if role == "user" and txt.strip()]
    # The agent's final text per user turn: the last assistant text before the next user turn.
    finals, last, started = [], None, False
    for role, txt, _, ts, _ in turns:
        if role == "user" and txt.strip():
            if started: finals.append(last or "")
            started, last = True, None
        elif role == "assistant" and txt.strip(): last = txt
    if started: finals.append(last or "")
    head = [f"# {os.path.basename(path)}", f"harness: {harness}", f"file: {path}", f"size: {os.path.getsize(path)} bytes",
            f"when: {str(stamps[0])[:16] if stamps else '?'} to {str(stamps[-1])[:16] if stamps else '?'}", f"project: {redact(cwds[0]) if cwds else '?'}",
            f"turns: {len(user_turns)} owner, {sum(1 for r in turns if r[0] == 'assistant')} agent", "tools: " + (", ".join(f"{k}×{v}" for k, v in sorted(tools.items(), key=lambda x: -x[1])[:12]) or "none"), ""]
    body, budget = [], max_chars
    per_turn = max(120, max_chars // max(1, min(len(user_turns), 40)) // 2)
    for i, (txt, ts) in enumerate(user_turns[:60]):
        line = f"OWNER {str(ts)[11:16] if ts else ''}: {cap(redact(txt), per_turn)}"
        reply = f"  AGENT: {cap(redact(finals[i]), per_turn // 2)}" if i < len(finals) and finals[i] else ""
        chunk = line + ("\n" + reply if reply else "")
        if budget - len(chunk) < 0: body.append("… (digest capped)"); break
        body.append(chunk); budget -= len(chunk)
    return "\n".join(head + body) + "\n", {"file": path, "harness": harness, "bytes": os.path.getsize(path), "first": str(stamps[0])[:10] if stamps else None, "last": str(stamps[-1])[:10] if stamps else None, "owner_turns": len(user_turns), "tools": tools, "project": redact(cwds[0]) if cwds else None}


def record_pattern(harness):
    """The harness's own record file pattern from the inventory table, when it names JSONL files."""
    try:
        from harnesses import KNOWN
        for name, _, pattern, fmt in KNOWN:
            if name == harness and fmt == "jsonl" and pattern.endswith(".jsonl"): return pattern
    except ImportError: pass
    return os.path.join("**", "*.jsonl")


def sample(root, recent, largest, min_bytes, pattern=None):
    matched = glob.glob(os.path.join(glob.escape(root), pattern or os.path.join("**", "*.jsonl")), recursive=True)
    files = [f for f in matched if os.path.getsize(f) >= min_bytes]
    by_time = sorted(files, key=os.path.getmtime, reverse=True)[:recent]
    by_size = sorted(files, key=os.path.getsize, reverse=True)[:largest]
    seen, out = set(), []
    for f in by_time + by_size:
        if f not in seen: seen.add(f); out.append(f)
    return out, len(files), len(matched)


def run(root, harness, out, recent, largest, max_chars, min_bytes):
    os.makedirs(out, exist_ok=True)
    picked, eligible, matched = sample(root, recent, largest, min_bytes, record_pattern(harness))
    if not picked:
        raise SystemExit(f"{harness}: {matched} .jsonl files under {root}, none at least {min_bytes} bytes; nothing digested" if matched else f"{harness}: no .jsonl session records under {root}; this digester reads JSONL only. Record a stated limit.")
    index = {"harness": harness, "root": root, "eligible_files": eligible, "sampled": [], "generated": dt.date.today().isoformat()}
    for path in picked:
        text, meta = digest_one(path, harness, max_chars)
        rel = os.path.relpath(path, root)
        name = re.sub(r"[^A-Za-z0-9_.-]+", "_", rel)[:104] + "-" + hashlib.sha1(rel.encode()).hexdigest()[:8] + ".md"
        with open(os.path.join(out, name), "w", encoding="utf-8") as f: f.write(text)
        meta["digest"] = name; index["sampled"].append(meta)
    with open(os.path.join(out, "index.json"), "w", encoding="utf-8") as f: json.dump(index, f, indent=1)
    dates = [m["first"] for m in index["sampled"] if m["first"]] + [m["last"] for m in index["sampled"] if m["last"]]
    print(f"{harness}: {len(picked)} of {eligible} sessions digested into {out}; dates {min(dates) if dates else '?'} to {max(dates) if dates else '?'}")


def self_test():
    here = os.path.dirname(os.path.abspath(__file__)); fx = os.path.join(here, "..", "fixtures", "sessions")
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        import json as _j
        pair = os.path.join(tmp, "pair", "s"); os.makedirs(pair)
        with open(os.path.join(pair, "a.jsonl"), "w") as f:
            for role, text in (("user", "QUESTION-ONE"), ("user", "QUESTION-TWO"), ("assistant", "REPLY-TO-TWO"), ("user", "QUESTION-THREE ring +44 20 7946 0958 about 1,250.00 GBP"), ("assistant", "REPLY-TO-THREE")):
                f.write(_j.dumps({"type": role, "message": {"role": role, "content": text}}) + "\n")
        run(os.path.join(tmp, "pair"), "claude-code", os.path.join(tmp, "pair-out"), 20, 10, 6000, 0)
        d = open(glob.glob(os.path.join(tmp, "pair-out", "*.md"))[0], encoding="utf-8").read()
        assert "OWNER : QUESTION-ONE\nOWNER : QUESTION-TWO\n  AGENT: REPLY-TO-TWO\nOWNER : QUESTION-THREE" in d.replace("OWNER  :", "OWNER :"), d
        assert "REPLY-TO-THREE" in d and "+44 20" not in d and "1,250.00 GBP" not in d, d
        long_root = os.path.join(tmp, "long"); deep = os.path.join(long_root, "-Users-owner-Library-CloudStorage-GoogleDrive-owner-example-com-My-Drive-clients-acme-corporation-operations-platform-billing"); os.makedirs(deep)
        for n in range(3):
            with open(os.path.join(deep, f"{n}.jsonl"), "w") as f: f.write(_j.dumps({"type": "user", "message": {"role": "user", "content": f"MARKER number {n}"}}) + "\n")
        run(long_root, "claude-code", os.path.join(tmp, "long-out"), 20, 10, 6000, 0)
        assert len(glob.glob(os.path.join(tmp, "long-out", "*.md"))) == 3, "long project names must not collide"
        empty = os.path.join(tmp, "empty"); os.makedirs(empty); open(os.path.join(empty, "x.json"), "w").write("{}")
        try: run(empty, "gemini-cli", os.path.join(tmp, "empty-out"), 20, 10, 6000, 0); raise AssertionError("empty store must fail loudly")
        except SystemExit as e: assert "reads JSONL only" in str(e), e
        grok = os.path.join(tmp, "grok", "cwd", "sess"); os.makedirs(grok)
        for n in ("chat_history.jsonl", "events.jsonl", "updates.jsonl"):
            with open(os.path.join(grok, n), "w") as f: f.write(_j.dumps({"role": "user", "content": f"from {n}"}) + "\n")
        run(os.path.join(tmp, "grok"), "grok-build", os.path.join(tmp, "grok-out"), 20, 10, 6000, 0)
        assert len(glob.glob(os.path.join(tmp, "grok-out", "*.md"))) == 1, "grok-build digests chat_history only"
        bracket = os.path.join(tmp, "Client [Acme]", "sessions"); os.makedirs(bracket)
        with open(os.path.join(bracket, "b.jsonl"), "w") as f: f.write(_j.dumps({"type": "user", "message": {"role": "user", "content": "bracket ok"}}) + "\n")
        run(bracket, "claude-code", os.path.join(tmp, "bracket-out"), 20, 10, 6000, 0)
        assert glob.glob(os.path.join(tmp, "bracket-out", "*.md")), "bracketed root must digest"
        for harness, sub in (("claude-code", "claude-projects"), ("codex", "codex-sessions"), ("pi-agent", "pi-agent-sessions")):
            out = os.path.join(tmp, harness); run(os.path.join(fx, sub), harness, out, 20, 10, 6000, 0)
            digests = [open(os.path.join(out, f), encoding="utf-8").read() for f in os.listdir(out) if f.endswith(".md")]
            assert digests, harness; d = digests[0]
            for raw in ("owner@example.com", "555-123-4567", "$1,250.00", "sk-live-ABCDEFGHIJKLMNOPQRSTUVWXYZ1234", "https://console.example.com/x"): assert raw not in d, (harness, raw)
            for raw, sub in (("routing 021000021 account 123456789012", "<number>"), ("token q8Zx1Lm9Kp3Vt7Rw2Yb6Nc4Hd", "<token>"), ("card 4111 1111 1111 1111", "<number>")):
                red = redact(raw); assert sub in red and raw.split()[-1] not in red, (raw, red)
            assert redact("when 2026-09-01 22:40 ok") == "when 2026-09-01 22:40 ok", "dates and times survive"
            assert "OWNER" in d and "AGENT" in d, d
            idx = json.load(open(os.path.join(out, "index.json"))); assert idx["sampled"][0]["owner_turns"] >= 2, idx
        claude = open(glob.glob(os.path.join(tmp, "claude-code", "*.md"))[0], encoding="utf-8").read()
        assert "tools: Bash×1" in claude and "explain simpler" in claude and "<email>" in claude and "<key>" in claude and "<amount>" in claude, claude
        codex = open(glob.glob(os.path.join(tmp, "codex", "*.md"))[0], encoding="utf-8").read()
        assert "shell×1" in codex and "did that" in codex and "<url>" in codex, codex
        pi = open(glob.glob(os.path.join(tmp, "pi-agent", "*.md"))[0], encoding="utf-8").read()
        assert "bash×1" in pi and "reverting" in pi, pi
    print("digest self-test passed")


def main():
    p = argparse.ArgumentParser(); p.add_argument("--root"); p.add_argument("--harness"); p.add_argument("--out"); p.add_argument("--recent", type=int, default=20); p.add_argument("--largest", type=int, default=10); p.add_argument("--max-chars", type=int, default=6000); p.add_argument("--min-bytes", type=int, default=2048); p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test: return self_test()
    if not (a.root and a.harness and a.out): raise SystemExit("pass --root, --harness, and --out")
    run(os.path.abspath(os.path.expanduser(a.root)), a.harness, os.path.abspath(os.path.expanduser(a.out)), a.recent, a.largest, a.max_chars, a.min_bytes)


if __name__ == "__main__": main()
