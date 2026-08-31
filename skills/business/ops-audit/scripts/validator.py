"""Canonical stdlib contract for ops-audit roadmap and state documents.
The adjacent JSON schema files describe this same public contract; render and feedback
both call these validators rather than implementing partial checks.
"""
from __future__ import annotations

import json
import re
from numbers import Real

LABELS = {"observed", "owner-reported", "inferred"}
GROUPS = {"Now", "Next", "Later"}
VERDICTS = {"keep human", "leverage move", "automate with an agent"}
INTERVENTIONS = {"remove", "simplify", "deterministic rule", "leverage move", "agent automation"}
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
    required(card, ("id", "version", "group", "action", "hours_per_month", "hourly_value", "annual_labor_value", "causal_path", "evidence", "existing_coverage", "gaps", "approval", "intervention", "diagnosis", "proof", "verdict"), "card")
    identifier(card["id"], "card.id"); integer(card["version"], "card.version", 1)
    if card["group"] not in GROUPS: fail("card.group is invalid")
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
    required(path, ("trigger", "collection", "judgment", "action", "destination", "read_back", "failure_visibility"), "card.causal_path")
    for stage in ("trigger", "collection", "judgment", "action", "destination", "read_back", "failure_visibility"): string(path[stage], f"card.causal_path.{stage}")
    validate_evidence(card["evidence"], "card.evidence")
    coverage = obj(card["existing_coverage"], "card.existing_coverage")
    required(coverage, ("definitions", "recent_runs", "outputs", "failure_visibility"), "card.existing_coverage")
    for key in coverage:
        if key not in ("definitions", "recent_runs", "outputs", "failure_visibility"): continue
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


def validate_roadmap(roadmap):
    roadmap = obj(roadmap, "roadmap")
    required(roadmap, ("roadmap_id", "business", "date", "revision", "incomplete", "stopping_point", "consent", "exclusions", "cards", "first_move", "first_automation", "first_automation_reason", "pending_feedback", "owner_approval"), "roadmap")
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
    if not isinstance(roadmap["pending_feedback"], list): fail("pending_feedback must be an array")
    validate_owner_approval(roadmap["owner_approval"], roadmap["roadmap_id"], roadmap["revision"], "roadmap.owner_approval")
    for event in roadmap["pending_feedback"]: validate_feedback_event(event, roadmap["roadmap_id"])
    if roadmap["incomplete"]:
        if not roadmap["stopping_point"]: fail("incomplete roadmap needs stopping_point")
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
    return roadmap


def validate_owner_approval(value, roadmap_id, revision, where):
    if value is None: return
    value = obj(value, where)
    required(value, ("roadmap_id", "roadmap_revision", "approved_by", "approved_at"), where)
    identifier(value["roadmap_id"], f"{where}.roadmap_id"); integer(value["roadmap_revision"], f"{where}.roadmap_revision", 1)
    string(value["approved_by"], f"{where}.approved_by"); string(value["approved_at"], f"{where}.approved_at")
    if value["roadmap_id"] != roadmap_id or value["roadmap_revision"] != revision: fail(f"{where} must bind current roadmap identity and revision")

def validate_feedback_event(event, roadmap_id):
    event = obj(event, "feedback event")
    required(event, ("event_id", "roadmap_id", "roadmap_revision", "card_id", "card_version", "choice", "note", "status"), "feedback event")
    identifier(event["event_id"], "feedback event.event_id")
    identifier(event["roadmap_id"], "feedback event.roadmap_id")
    identifier(event["card_id"], "feedback event.card_id")
    string(event["note"], "feedback event.note", True)
    if event["roadmap_id"] != roadmap_id: fail("feedback event roadmap_id mismatch")
    integer(event["roadmap_revision"], "feedback event.roadmap_revision", 1); integer(event["card_version"], "feedback event.card_version", 1)
    if event["choice"] not in ("accept", "change", "reject") or event["status"] != "pending": fail("feedback event is invalid")
    if event["choice"] == "change" and not event["note"].strip(): fail("change needs note")


def validate_state(state):
    state = obj(state, "state")
    required(state, ("roadmap_id", "revision", "consent", "exclusions", "evidence", "feedback_ledger", "feedback_by_roadmap", "incomplete", "stopped_at", "owner_approval"), "state")
    identifier(state["roadmap_id"], "state.roadmap_id"); integer(state["revision"], "state.revision", 1)
    validate_owner_approval(state["owner_approval"], state["roadmap_id"], state["revision"], "state.owner_approval")
    for field in ("consent", "exclusions", "evidence", "feedback_ledger"):
        if not isinstance(state[field], list): fail(f"state.{field} must be an array")
    for item in state["consent"]:
        obj(item, "state.consent"); required(item, ("category", "scope"), "state.consent"); string(item["category"], "state.consent.category"); string(item["scope"], "state.consent.scope")
    for item in state["exclusions"]:
        obj(item, "state.exclusions"); required(item, ("category", "declared_root_or_account"), "state.exclusions"); string(item["category"], "state.exclusions.category"); string(item["declared_root_or_account"], "state.exclusions.declared_root_or_account")
    if not isinstance(state["feedback_by_roadmap"], dict): fail("state.feedback_by_roadmap must be an object")
    bucket = state["feedback_by_roadmap"].get(state["roadmap_id"], {})
    if bucket:
        obj(bucket, "feedback bucket"); required(bucket, ("revision", "cards"), "feedback bucket"); integer(bucket["revision"], "feedback bucket.revision", 1); obj(bucket["cards"], "feedback bucket.cards")
        for card_events in bucket["cards"].values():
            if not isinstance(card_events, list): fail("feedback card events must be arrays")
            for event in card_events: validate_feedback_event(event, state["roadmap_id"])
    if not isinstance(state["incomplete"], bool): fail("state.incomplete must be boolean")
    if state["stopped_at"] is not None: string(state["stopped_at"], "state.stopped_at")
    return state


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))
