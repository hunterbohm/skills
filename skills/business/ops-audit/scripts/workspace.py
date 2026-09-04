#!/usr/bin/env python3
"""The one printer of the plan and the one writer of step status (Python 3).

  workspace.py plan <workspace> [--full]
  workspace.py step <workspace> <card> <status> --note "<the owner's words, or what was done and how it was checked>"

The plan prints as chat text. Step status moves forward only, in plan order, and never touches the plan revision.
"""
from __future__ import annotations
import argparse, json, os, sys, tempfile
from datetime import date
from pathlib import Path
from validator import COMPLETE, STATUSES_BY_KIND, step_kind, step_statuses, validate_roadmap, validate_state, validate_steps_against


def fail(message): raise ValueError(message)
def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def atomic(path, text):
    path = Path(path); fd, tmp = tempfile.mkstemp(prefix=".", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f: f.write(text); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
def documents(workspace):
    w = Path(workspace); roadmap = validate_roadmap(load(w / "roadmap.json")); state = validate_state(load(w / "state.json"))
    if state["roadmap_id"] != roadmap["roadmap_id"] or state["revision"] != roadmap["revision"]: fail("state and roadmap identity or revision differ")
    if not roadmap["incomplete"]: validate_steps_against(roadmap, state)
    return w, roadmap, state


def status_words(kind, status, eligible):
    if status in COMPLETE: return "Running" if kind == "automation" else "Done"
    if kind == "hold": return "On hold" if status == "holding" else "Hold ended"
    if status == "approved": return "Approved, in progress"
    return "Next: needs your go" if eligible else "Later"


WHO = {"move": "The agent does this once, after you say go.", "automation": "The agent builds this and it runs on its own, after you approve it.", "hold": "Nobody changes this yet."}


def plan_text(roadmap, state, full=False):
    approval = roadmap["owner_approval"]
    focus = f", focused on {roadmap['focus']}" if roadmap.get("focus") else ""
    head = f"{roadmap['business']}{focus}, plan revision {roadmap['revision']}, " + (f"approved by {approval['approved_by']} on {approval['approved_at']}." if approval else "not yet approved.")
    if roadmap["incomplete"]: return head + f"\n\nThe audit stopped at: {roadmap['stopping_point']}. There is no plan yet. Say when to continue.\n"
    by_id = {c["id"]: c for c in roadmap["cards"]}; statuses = step_statuses(roadmap, state)
    def block(step, prefix):
        card = by_id[step["card"]]; kind, status, eligible = statuses[step["card"]]
        lines = [f"{prefix}{step['title']}  [{status_words(kind, status, eligible)}]", f"   You decide: {step['you_decide']}"]
        if full:
            lines.insert(1, f"   {WHO[kind]}")
            lines[2:2] = [f"   - {line}" for line in step["do"]]
            lines.append(f"   Done when: {step['done_when']}")
            if step["never"]: lines.append(f"   Never: {step['never']}")
            if card["hours_per_month"] is not None:
                yearly = f", about ${card['annual_labor_value']:,.0f} a year" if card["annual_labor_value"] is not None else ""
                lines.append(f"   About {card['hours_per_month']:g} hours a month today{yearly}.")
        return "\n".join(lines)
    steps = roadmap["plan"]["steps"]
    main = [s for s in steps if s["lane"] == "main"]
    side = [s for s in steps if s["lane"] == "parallel" and step_kind(by_id[s["card"]]) != "hold"]
    holds = [s for s in steps if step_kind(by_id[s["card"]]) == "hold"]
    out = [head, "", "In order:"] + [block(s, f"{i + 1}. ") for i, s in enumerate(main)]
    if side: out += ["", "Any time, without waiting:"] + [block(s, "- ") for s in side]
    if holds: out += ["", "On hold:"] + [block(s, "- ") for s in holds]
    if roadmap["first_automation"] is None: out += ["", f"No automation is planned yet: {roadmap['first_automation_reason']}"]
    if roadmap.get("extensions"): out += ["", "If you add:"] + [f"- {e['add']}: {e['unlocks']}" for e in roadmap["extensions"]]
    return "\n".join(out) + "\n"


def step(w, roadmap, state, card_id, target, note):
    if roadmap["incomplete"]: fail("the audit is incomplete; there is no plan to work")
    if roadmap["owner_approval"] is None or state["owner_approval"] != roadmap["owner_approval"]: fail("the plan is not approved at this revision; no step may move")
    if card_id not in {s["card"] for s in roadmap["plan"]["steps"]}: fail("card is not a step in the plan")
    kind, current, eligible = step_statuses(roadmap, state)[card_id]; ladder = STATUSES_BY_KIND[kind]
    if target not in ladder: fail(f"{target} is not a {kind} status")
    if ladder.index(target) != ladder.index(current) + 1: fail(f"a step moves one status forward; {card_id} is {current}")
    if kind != "hold" and not eligible: fail("earlier main-lane steps are not done yet")
    if not note: fail("every status change records the owner's words or what was done; pass --note")
    state["steps"][card_id] = {"status": target, "note": note, "date": str(date.today())}
    validate_steps_against(roadmap, state)
    atomic(w / "state.json", json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def main():
    p = argparse.ArgumentParser(); q = p.add_subparsers(dest="cmd", required=True)
    a = q.add_parser("plan"); a.add_argument("workspace"); a.add_argument("--full", action="store_true")
    a = q.add_parser("step"); a.add_argument("workspace"); a.add_argument("card"); a.add_argument("status"); a.add_argument("--note", default="")
    a = p.parse_args()
    try:
        w, roadmap, state = documents(a.workspace)
        if a.cmd == "step": step(w, roadmap, state, a.card, a.status, a.note)
        sys.stdout.write(plan_text(roadmap, state, getattr(a, "full", False)))
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as error:
        print("ERROR: " + str(error), file=sys.stderr); raise SystemExit(1)


if __name__ == "__main__": main()
