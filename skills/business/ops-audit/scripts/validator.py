"""Canonical stdlib contract for ops-audit roadmap and state documents.
The adjacent JSON schema files describe this same public contract.
"""
from __future__ import annotations

import json
import re
from numbers import Real

LABELS = {"observed", "owner-reported", "inferred"}
VERDICTS = {"keep human", "leverage move", "automate with an agent"}
INTERVENTIONS = {"remove", "simplify", "deterministic rule", "leverage move", "agent automation"}
LANES = {"main", "parallel"}
KIND_BY_VERDICT = {"leverage move": "move", "automate with an agent": "automation", "keep human": "hold"}
STEP_STATUSES = ("proposed", "approved", "done")
HOLD_STATUSES = ("holding", "ended")
STATUSES_BY_KIND = {"move": STEP_STATUSES, "automation": STEP_STATUSES, "hold": HOLD_STATUSES}
COMPLETE = {"done"}
ID = re.compile(r"^[A-Za-z0-9_-]+$")


def fail(message: str) -> None:
    raise ValueError(message)


def obj(value, name):
    if not isinstance(value, dict): fail(f"{name} must be an object")
    return value


def string(value, name, allow_empty=False):
    if not isinstance(value, str) or (not allow_empty and not value.strip()): fail(f"{name} must be a non-empty string")
    return value


def identifier(value, name):
    string(value, name)
    if not ID.fullmatch(value): fail(f"{name} must contain only letters, digits, underscores, and hyphens")
    return value


def integer(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum: fail(f"{name} must be an integer >= {minimum}")
    return value


def number(value, name):
    if isinstance(value, bool) or not isinstance(value, Real) or value < 0: fail(f"{name} must be a non-negative number")
    return value


def required(data, names, where):
    for name in names:
        if name not in data: fail(f"{where} missing {name}")


def step_kind(card):
    return KIND_BY_VERDICT[card["verdict"]]


def validate_evidence(items, where):
    if not isinstance(items, list): fail(f"{where} must be an array")
    for index, item in enumerate(items):
        item = obj(item, f"{where}[{index}]")
        required(item, ("label", "claim", "source"), f"{where}[{index}]")
        if item["label"] not in LABELS: fail(f"{where}[{index}].label is invalid")
        string(item["claim"], f"{where}[{index}].claim")
        string(item["source"], f"{where}[{index}].source")


def validate_card(card):
    card = obj(card, "card")
    required(card, ("id", "version", "action", "hours_per_month", "hourly_value", "annual_labor_value", "causal_path", "evidence", "existing_coverage", "gaps", "approval", "intervention", "diagnosis", "proof", "verdict"), "card")
    identifier(card["id"], "card.id"); integer(card["version"], "card.version", 1)
    string(card["action"], "card.action")
    hours, rate, annual = (card["hours_per_month"], card["hourly_value"], card["annual_labor_value"])
    if hours is not None: number(hours, "hours_per_month")
    if rate is not None: number(rate, "hourly_value")
    if hours is None or rate is None:
        if annual is not None: fail("annual_labor_value must be null when hours or hourly value is unknown")
    else:
        number(annual, "annual_labor_value")
        if abs(annual - hours * rate * 12) > .001: fail("derived cost inconsistent")
    path = obj(card["causal_path"], "card.causal_path")
    stages = ("trigger", "collection", "judgment", "action", "destination", "read_back", "failure_visibility")
    required(path, stages, "card.causal_path")
    for stage in stages: string(path[stage], f"card.causal_path.{stage}")
    validate_evidence(card["evidence"], "card.evidence")
    coverage = obj(card["existing_coverage"], "card.existing_coverage")
    required(coverage, ("definitions", "recent_runs", "outputs", "failure_visibility"), "card.existing_coverage")
    for key in ("definitions", "recent_runs", "outputs", "failure_visibility"):
        if not isinstance(coverage[key], list): fail(f"card.existing_coverage.{key} must be an array")
        for item in coverage[key]: string(item, f"card.existing_coverage.{key} item")
    if not isinstance(card["gaps"], list): fail("card.gaps must be an array")
    for gap in card["gaps"]: string(gap, "card.gaps item")
    approval = obj(card["approval"], "card.approval")
    required(approval, ("required", "approver", "gate"), "card.approval")
    if not isinstance(approval["required"], bool): fail("card.approval.required must be boolean")
    if approval["required"]:
        string(approval["approver"], "card.approval.approver"); string(approval["gate"], "card.approval.gate")
    elif approval["approver"] is not None or approval["gate"] is not None: fail("non-required approval must have null approver and gate")
    if card["intervention"] not in INTERVENTIONS: fail("card.intervention is invalid")
    string(card["diagnosis"], "card.diagnosis")
    string(card["proof"], "card.proof")
    if card["verdict"] not in VERDICTS: fail("card.verdict is invalid")


def validate_plan(plan, cards, first_move, first_automation):
    plan = obj(plan, "plan")
    required(plan, ("steps",), "plan")
    steps = plan["steps"]
    if not isinstance(steps, list) or not steps: fail("plan.steps must be a non-empty array")
    by_id = {card["id"]: card for card in cards}
    seen = set()
    for index, step in enumerate(steps):
        where = f"plan.steps[{index}]"
        step = obj(step, where)
        required(step, ("card", "lane", "title", "do", "you_decide", "done_when", "never"), where)
        identifier(step["card"], f"{where}.card")
        if step["card"] not in by_id: fail(f"{where}.card does not name a card")
        if step["card"] in seen: fail(f"{where}.card appears more than once")
        seen.add(step["card"])
        if step["lane"] not in LANES: fail(f"{where}.lane must be main or parallel")
        string(step["title"], f"{where}.title")
        if not isinstance(step["do"], list) or not 1 <= len(step["do"]) <= 3: fail(f"{where}.do needs one to three lines")
        for line in step["do"]: string(line, f"{where}.do line")
        string(step["you_decide"], f"{where}.you_decide"); string(step["done_when"], f"{where}.done_when")
        if step["never"] is not None: string(step["never"], f"{where}.never")
        if step_kind(by_id[step["card"]]) == "hold" and step["lane"] != "parallel": fail(f"{where} is a hold and must sit in the parallel lane")
    missing = set(by_id) - seen
    if missing: fail("every card must appear in exactly one step; missing " + ", ".join(sorted(missing)))
    main = [step for step in steps if step["lane"] == "main"]
    if not main: fail("plan needs at least one main-lane step")
    if main[0]["card"] != first_move: fail("the first main-lane step must be first_move")
    automations = [step["card"] for step in steps if step_kind(by_id[step["card"]]) == "automation"]
    if automations and automations[0] != first_automation: fail("first_automation must be the first automation step in the plan")
    if not automations and first_automation is not None: fail("first_automation names a card that is not an automation step")
    return plan


def validate_roadmap(roadmap):
    roadmap = obj(roadmap, "roadmap")
    required(roadmap, ("roadmap_id", "business", "date", "revision", "incomplete", "stopping_point", "consent", "exclusions", "cards", "plan", "first_move", "first_automation", "first_automation_reason", "owner_approval"), "roadmap")
    identifier(roadmap["roadmap_id"], "roadmap_id")
    for key in ("business", "date"): string(roadmap[key], key)
    integer(roadmap["revision"], "revision", 1)
    if not isinstance(roadmap["incomplete"], bool): fail("incomplete must be boolean")
    if roadmap["stopping_point"] is not None: string(roadmap["stopping_point"], "stopping_point")
    if not isinstance(roadmap["consent"], list) or not isinstance(roadmap["exclusions"], list): fail("consent and exclusions must be arrays")
    for item in roadmap["consent"]: obj(item, "consent"); required(item, ("category", "scope"), "consent"); string(item["category"], "consent.category"); string(item["scope"], "consent.scope")
    for item in roadmap["exclusions"]: obj(item, "exclusion"); required(item, ("category", "declared_root_or_account"), "exclusion"); string(item["category"], "exclusion.category"); string(item["declared_root_or_account"], "exclusion.declared_root_or_account")
    if not isinstance(roadmap["cards"], list): fail("cards must be an array")
    ids = set()
    for card in roadmap["cards"]:
        validate_card(card)
        if card["id"] in ids: fail("duplicate card id")
        ids.add(card["id"])
    validate_owner_approval(roadmap["owner_approval"], roadmap["roadmap_id"], roadmap["revision"], "roadmap.owner_approval")
    if roadmap.get("focus") is not None: string(roadmap["focus"], "focus")
    extensions = roadmap.get("extensions") or []
    if not isinstance(extensions, list): fail("extensions must be an array")
    for index, item in enumerate(extensions):
        where = f"extensions[{index}]"; obj(item, where); required(item, ("add", "unlocks"), where); string(item["add"], f"{where}.add"); string(item["unlocks"], f"{where}.unlocks")
    if roadmap["incomplete"]:
        if not roadmap["stopping_point"]: fail("incomplete roadmap needs stopping_point")
        if roadmap["plan"] is not None: fail("incomplete roadmap cannot carry a plan")
        if roadmap["first_move"] is not None or roadmap["first_automation"] is not None: fail("incomplete roadmap cannot claim a first move or automation")
        if roadmap["first_automation_reason"] not in ("", None): fail("incomplete roadmap cannot claim an automation reason")
        return roadmap
    if not roadmap["cards"]: fail("complete roadmap needs cards")
    if roadmap["stopping_point"] is not None: fail("complete roadmap stopping_point must be null")
    if roadmap["first_move"] not in ids: fail("first_move must name a card")
    automation = roadmap["first_automation"]
    if automation is None:
        string(roadmap["first_automation_reason"], "first_automation_reason")
    else:
        if automation not in ids: fail("first_automation must name a card or null")
        if next(card for card in roadmap["cards"] if card["id"] == automation)["verdict"] != "automate with an agent": fail("first_automation must reference automate-with-agent")
        if roadmap["first_automation_reason"] not in ("", None): fail("first_automation_reason must be empty when automation exists")
    if roadmap["plan"] is None: fail("complete roadmap needs a plan")
    validate_plan(roadmap["plan"], roadmap["cards"], roadmap["first_move"], automation)
    return roadmap


def validate_owner_approval(value, roadmap_id, revision, where):
    if value is None: return
    value = obj(value, where)
    required(value, ("roadmap_id", "roadmap_revision", "approved_by", "approved_at"), where)
    identifier(value["roadmap_id"], f"{where}.roadmap_id"); integer(value["roadmap_revision"], f"{where}.roadmap_revision", 1)
    string(value["approved_by"], f"{where}.approved_by"); string(value["approved_at"], f"{where}.approved_at")
    if value["roadmap_id"] != roadmap_id or value["roadmap_revision"] != revision: fail(f"{where} must bind current roadmap identity and revision")


def validate_step_status(value, where, kind=None):
    value = obj(value, where)
    required(value, ("status", "note", "date"), where)
    allowed = STATUSES_BY_KIND[kind] if kind else STEP_STATUSES + HOLD_STATUSES
    if value["status"] not in allowed: fail(f"{where}.status is not a {kind or 'step'} status")
    string(value["note"], f"{where}.note"); string(value["date"], f"{where}.date")
    return value


def validate_state(state):
    state = obj(state, "state")
    required(state, ("roadmap_id", "revision", "consent", "exclusions", "evidence", "changes", "incomplete", "stopped_at", "owner_approval", "steps"), "state")
    identifier(state["roadmap_id"], "state.roadmap_id"); integer(state["revision"], "state.revision", 1)
    validate_owner_approval(state["owner_approval"], state["roadmap_id"], state["revision"], "state.owner_approval")
    for field in ("consent", "exclusions", "evidence", "changes"):
        if not isinstance(state[field], list): fail(f"state.{field} must be an array")
    for item in state["consent"]:
        obj(item, "state.consent"); required(item, ("category", "scope"), "state.consent"); string(item["category"], "state.consent.category"); string(item["scope"], "state.consent.scope")
    for item in state["exclusions"]:
        obj(item, "state.exclusions"); required(item, ("category", "declared_root_or_account"), "state.exclusions"); string(item["category"], "state.exclusions.category"); string(item["declared_root_or_account"], "state.exclusions.declared_root_or_account")
    for index, item in enumerate(state["changes"]):
        where = f"state.changes[{index}]"
        obj(item, where); required(item, ("revision", "date", "summary"), where)
        integer(item["revision"], f"{where}.revision", 2); string(item["date"], f"{where}.date"); string(item["summary"], f"{where}.summary")
    if {c["revision"] for c in state["changes"]} != set(range(2, state["revision"] + 1)): fail("state.changes needs exactly one entry per revision after the first")
    for index, item in enumerate(state["evidence"]):
        where = f"state.evidence[{index}]"
        obj(item, where); required(item, ("category", "status", "source"), where)
        for k in ("category", "status", "source"): string(item[k], f"{where}.{k}")
        if item.get("limit") is not None: string(item["limit"], f"{where}.limit")
    if not isinstance(state["incomplete"], bool): fail("state.incomplete must be boolean")
    if state["stopped_at"] is not None: string(state["stopped_at"], "state.stopped_at")
    steps = obj(state["steps"], "state.steps")
    for card_id, value in steps.items():
        identifier(card_id, "state.steps key"); validate_step_status(value, f"state.steps.{card_id}")
    return state


def validate_steps_against(roadmap, state):
    """Every recorded step status must name a plan card and use that card's kind of status."""
    by_id = {card["id"]: card for card in roadmap["cards"]}
    for card_id, value in state["steps"].items():
        if card_id not in by_id: fail(f"state.steps.{card_id} names no card")
        validate_step_status(value, f"state.steps.{card_id}", step_kind(by_id[card_id]))


def step_statuses(roadmap, state):
    """Return {card_id: (kind, status, eligible)} for every step, from state when present."""
    by_id = {card["id"]: card for card in roadmap["cards"]}
    recorded_steps = (state or {}).get("steps", {})
    result = {}
    main_clear = True
    for step in roadmap["plan"]["steps"]:
        card = by_id[step["card"]]; kind = step_kind(card)
        recorded = recorded_steps.get(step["card"])
        status = recorded["status"] if recorded else STATUSES_BY_KIND[kind][0]
        if step["lane"] == "main":
            eligible = main_clear and kind != "hold"
            main_clear = main_clear and status in COMPLETE
        else:
            eligible = kind != "hold"
        result[step["card"]] = (kind, status, eligible)
    return result


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))
