#!/usr/bin/env python3
"""Advisory ledger for the ask-hormozi skill — durable state across sessions.

One ledger per business at <root>/<business-slug>/advisory.json.

The root is resolved in this order, so it survives sessions and does not
depend on any single agent runtime's memory:

  1. $ASK_HORMOZI_ADVISORY_ROOT
  2. the root recorded in $XDG_CONFIG_HOME/ask-hormozi/config.json
     (default: ~/.config/ask-hormozi/config.json)

Exit codes: 0 ok · 2 usage or validation error · 3 no root recorded
            · 4 no ledger for that business

Stdlib only. Writes are atomic (temp file + rename).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
BRANCHES = ("advise", "audit")
CONSTRAINTS = ("leads", "sales", "delivery", "profit", "offer", "focus")
STATUSES = ("open", "tried", "done", "dropped")
FIT = ("direct", "translate", "override")

SCHEMA_KEYS = {
    "business", "fit", "model", "constraint_history",
    "prescriptions", "corrections", "runs",
}


def config_path() -> pathlib.Path:
    base = os.environ.get("XDG_CONFIG_HOME") or pathlib.Path.home() / ".config"
    return pathlib.Path(base) / "ask-hormozi" / "config.json"


def read_config() -> dict:
    p = config_path()
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        die(f"config at {p} is not valid JSON: {exc}")


def write_json(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def die(msg: str, code: int = 2):
    print(f"ledger: {msg}", file=sys.stderr)
    raise SystemExit(code)


def today() -> str:
    return dt.date.today().isoformat()


def resolve_root(require_exists: bool = True) -> pathlib.Path:
    raw = os.environ.get("ASK_HORMOZI_ADVISORY_ROOT") or read_config().get("advisory_root")
    if not raw:
        die("no advisory root recorded. Ask the owner where ledgers should live, "
            "then run: ledger.py root --set <path>", 3)
    root = pathlib.Path(raw).expanduser()
    if require_exists and not root.is_dir():
        die(f"recorded advisory root does not exist: {root}\n"
            "        Ask the owner again, then re-record it with root --set "
            "(do not silently start a fresh ledger elsewhere).", 3)
    return root


def ledger_path(slug: str) -> pathlib.Path:
    if not SLUG_RE.fullmatch(slug):
        die(f"'{slug}' is not a kebab-case business slug")
    return resolve_root() / slug / "advisory.json"


def load(slug: str) -> dict:
    p = ledger_path(slug)
    if not p.is_file():
        die(f"no ledger for '{slug}' at {p}. Offer to start one: ledger.py init {slug}", 4)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        die(f"{p} is not valid JSON: {exc}")
    validate(data, p)
    return data


def validate(data: dict, where: pathlib.Path) -> None:
    if not isinstance(data, dict):
        die(f"{where}: expected a JSON object")
    missing = SCHEMA_KEYS - set(data)
    if missing:
        die(f"{where}: missing key(s): {', '.join(sorted(missing))}")
    for key in ("constraint_history", "prescriptions", "corrections", "runs"):
        if not isinstance(data[key], list):
            die(f"{where}: '{key}' must be a list")
    if not isinstance(data["model"], dict):
        die(f"{where}: 'model' must be an object")
    for i, presc in enumerate(data["prescriptions"]):
        if presc.get("status") not in STATUSES:
            die(f"{where}: prescriptions[{i}].status must be one of {'|'.join(STATUSES)}")


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------
def cmd_root(args) -> None:
    if args.set:
        new = pathlib.Path(args.set).expanduser().resolve()
        cfg = read_config()
        old = cfg.get("advisory_root")
        if old and str(new) != old and not args.force:
            die(f"a different advisory root is already recorded:\n"
                f"          {old}\n"
                "        Moving it orphans existing ledgers. Confirm with the owner "
                "that the old history is moved or intentionally abandoned, then "
                "re-run with --force.")
        new.mkdir(parents=True, exist_ok=True)
        cfg["advisory_root"] = str(new)
        write_json(config_path(), cfg)
        print(f"advisory root recorded: {new}")
        return
    print(resolve_root())


def cmd_list(args) -> None:
    root = resolve_root()
    found = sorted(p.parent.name for p in root.glob("*/advisory.json"))
    print("\n".join(found) if found else "(no ledgers yet)")


def cmd_init(args) -> None:
    p = ledger_path(args.slug)
    if p.exists():
        die(f"a ledger already exists at {p} — open it instead of starting a new one")
    ledger = {
        "business": args.business or args.slug,
        "fit": args.fit or "",
        "model": {"offer": "", "price": None, "customers_per_month": None,
                  "cac": None, "gp_first_30d": None, "churn": "", "as_of": ""},
        "constraint_history": [],
        "prescriptions": [],
        "corrections": [],
        "runs": [],
    }
    write_json(p, ledger)
    print(f"created {p}")


def cmd_open(args) -> None:
    data = load(args.slug)
    data["_open_prescriptions"] = [
        dict(p, index=i) for i, p in enumerate(data["prescriptions"])
        if p.get("status") in ("open", "tried")
    ]
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_append(args) -> None:
    data = load(args.slug)
    unresolved = [i for i, p in enumerate(data["prescriptions"])
                  if p.get("status") == "open"]
    if unresolved and not args.allow_unresolved:
        die("open prescription(s) at index "
            f"{', '.join(map(str, unresolved))} have no recorded result. "
            "Ask what happened and run `resolve` first, or pass --allow-unresolved "
            "if the owner genuinely could not say.")
    for pair in args.model or []:
        key, _, value = pair.partition("=")
        if not _:
            die(f"--model expects key=value, got '{pair}'")
        data["model"][key] = value
        data["model"]["as_of"] = today()
    if args.fit:
        data["fit"] = args.fit
    if args.constraint:
        data["constraint_history"].append(
            {"date": today(), "constraint": args.constraint, "evidence": args.evidence or ""})
    if args.action:
        data["prescriptions"].append(
            {"date": today(), "constraint": args.constraint or "", "action": args.action,
             "framework": args.framework or "", "status": "open", "result": ""})
    if args.correction:
        data["corrections"].append({"date": today(), "rule": args.correction})
    data["runs"].append({"date": today(), "branch": args.branch, "summary": args.summary})
    write_json(ledger_path(args.slug), data)
    print(f"appended run to {ledger_path(args.slug)}")


def cmd_resolve(args) -> None:
    data = load(args.slug)
    try:
        presc = data["prescriptions"][args.index]
    except IndexError:
        die(f"no prescription at index {args.index} "
            f"(ledger has {len(data['prescriptions'])})")
    presc["status"] = args.status
    presc["result"] = args.result
    write_json(ledger_path(args.slug), data)
    print(f"prescription {args.index} -> {args.status}")


def cmd_validate(args) -> None:
    p = ledger_path(args.slug)
    load(args.slug)
    print(f"{p}: valid")


def main() -> None:
    ap = argparse.ArgumentParser(prog="ledger.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("root", help="show or record where ledgers live")
    p.add_argument("--set", metavar="PATH")
    p.add_argument("--force", action="store_true", help="allow moving an existing root")
    p.set_defaults(func=cmd_root)

    p = sub.add_parser("list", help="list businesses with a ledger")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("init", help="start a ledger for a business")
    p.add_argument("slug")
    p.add_argument("--business", help="display name")
    p.add_argument("--fit", choices=FIT)
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("open", help="read a ledger (adds _open_prescriptions)")
    p.add_argument("slug")
    p.set_defaults(func=cmd_open)

    p = sub.add_parser("append", help="record this run (the write rule)")
    p.add_argument("slug")
    p.add_argument("--branch", choices=BRANCHES, required=True)
    p.add_argument("--summary", required=True)
    p.add_argument("--constraint", choices=CONSTRAINTS)
    p.add_argument("--evidence")
    p.add_argument("--action", help="the one highest-leverage action given")
    p.add_argument("--framework")
    p.add_argument("--fit", choices=FIT)
    p.add_argument("--model", action="append", metavar="KEY=VALUE")
    p.add_argument("--correction")
    p.add_argument("--allow-unresolved", action="store_true")
    p.set_defaults(func=cmd_append)

    p = sub.add_parser("resolve", help="record what happened to a prescription")
    p.add_argument("slug")
    p.add_argument("--index", type=int, required=True)
    p.add_argument("--status", choices=STATUSES, required=True)
    p.add_argument("--result", required=True)
    p.set_defaults(func=cmd_resolve)

    p = sub.add_parser("validate", help="check a ledger against the schema")
    p.add_argument("slug")
    p.set_defaults(func=cmd_validate)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
