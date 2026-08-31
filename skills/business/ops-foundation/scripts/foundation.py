#!/usr/bin/env python3
"""Locked, stdlib-only workspace contracts for ops-foundation (POSIX Python 3)."""
from __future__ import annotations
import argparse, fcntl, json, os, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

STATUSES = ("candidate", "designed", "built", "proven", "live")
MODES = ("fixture", "real", "activation", "report")
def fail(s): raise ValueError(s)
def text(v, n):
 if not isinstance(v, str) or not v.strip(): fail(f"{n} must be a non-empty string")
def integer(v, n):
 if isinstance(v, bool) or not isinstance(v, int) or v < 1: fail(f"{n} must be a positive integer")
def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def locked(workspace):
 p=Path(workspace); p.mkdir(parents=True, exist_ok=True); f=(p/".ops-foundation.lock").open("a+"); fcntl.flock(f, fcntl.LOCK_EX); return f
def atomic(path, data, json_data=True):
 path=Path(path); path.parent.mkdir(parents=True, exist_ok=True); fd,tmp=tempfile.mkstemp(prefix=".",dir=path.parent)
 try:
  with os.fdopen(fd,"w",encoding="utf-8") as f:
   f.write(json.dumps(data, indent=2)+"\n" if json_data else data); f.flush(); os.fsync(f.fileno())
  os.replace(tmp,path); d=os.open(path.parent,os.O_DIRECTORY); os.fsync(d); os.close(d)
 finally:
  if os.path.exists(tmp): os.unlink(tmp)
def approval(value, where):
 if not isinstance(value, dict): fail(f"{where} must be an owner approval record")
 for k in ("roadmap_id","roadmap_revision","approved_by","approved_at"): text(value.get(k),f"{where}.{k}") if k not in ("roadmap_revision",) else integer(value.get(k),f"{where}.{k}")
def roadmap(workspace):
 r=load(Path(workspace)/"roadmap.json")
 for k in ("roadmap_id","revision","incomplete","first_automation","first_automation_reason","cards","pending_feedback","owner_approval"): 
  if k not in r: fail(f"roadmap missing {k}")
 text(r["roadmap_id"],"roadmap_id"); integer(r["revision"],"roadmap revision")
 if r["incomplete"]: fail("roadmap is incomplete")
 audit_fields=("business","date","stopping_point","consent","exclusions","first_move")
 if any(k not in r for k in audit_fields): fail("roadmap is not a complete audit handoff")
 if not isinstance(r["cards"],list) or not r["cards"]: fail("roadmap needs cards")
 card_fields=("id","version","group","action","hours_per_month","hourly_value","annual_labor_value","causal_path","evidence","existing_coverage","gaps","approval","intervention","diagnosis","proof","verdict")
 for c in r["cards"]:
  if not isinstance(c,dict) or any(k not in c for k in card_fields): fail("roadmap card is not a complete audit card")
  card_for({"cards":[c]},c["id"])
 if not isinstance(r["pending_feedback"],list) or r["pending_feedback"]: fail("roadmap has pending feedback")
 approval(r["owner_approval"], "roadmap.owner_approval")
 a=r["owner_approval"]
 if a["roadmap_id"] != r["roadmap_id"] or a["roadmap_revision"] != r["revision"]: fail("roadmap approval does not bind current identity and revision")
 return r
def state(workspace): return load(Path(workspace)/"state.json")
def handoff(workspace):
 r=roadmap(workspace); s=state(workspace)
 for k in ("roadmap_id","revision","owner_approval"): 
  if k not in s: fail(f"state missing {k}")
 if s["roadmap_id"] != r["roadmap_id"] or s["revision"] != r["revision"]: fail("roadmap and state identity/revision mismatch")
 approval(s["owner_approval"], "state.owner_approval")
 if s["owner_approval"] != r["owner_approval"]: fail("roadmap and state approval mismatch")
 return r,s
def card_for(r, card_id):
 matches=[c for c in r["cards"] if c.get("id")==card_id]
 if len(matches)!=1: fail("card is not in approved roadmap")
 c=matches[0]; integer(c.get("version"),"card version")
 if not isinstance(c.get("approval"),dict) or not isinstance(c["approval"].get("required"),bool): fail("card approval is invalid")
 return c
def validate_contract(c, r=None, card=None):
 for k in ("roadmap_id","roadmap_revision","card_id","card_version","runtime","baseline","fixture","spine","idempotency_key_basis","failure_destination","implementation"):
  if k not in c: fail(f"contract missing {k}")
 for k in ("roadmap_id","card_id","idempotency_key_basis","failure_destination"): text(c[k],k)
 for k in ("roadmap_revision","card_version"): integer(c[k],k)
 if not isinstance(c["runtime"],dict): fail("runtime must be an object")
 for k in ("machine_runtime","trigger_owner","agent_model","secret_store","output_destination","approver_gate","failure_destination","record_source") : text(c["runtime"].get(k),f"runtime.{k}")
 if not isinstance(c["implementation"],dict): fail("implementation must be an object")
 for k in ("location","run","switch","stop"): text(c["implementation"].get(k),f"implementation.{k}")
 if not isinstance(c["baseline"],dict): fail("baseline must be an object")
 if not isinstance(c["fixture"],dict) or not c["fixture"].get("input") or not c["fixture"].get("expected_dry_run_action"): fail("fixture needs input and expected_dry_run_action")
 required=("trigger","collect","agent_joint","gate","act","verify","log"); s=c["spine"]
 if not isinstance(s,dict) or set(s)!=set(required): fail("spine must contain exactly the fixed stages")
 for k in required: text(s[k],f"spine.{k}")
 if r is not None:
  if c["roadmap_id"] != r["roadmap_id"] or c["roadmap_revision"] != r["revision"] or c["card_id"] != card["id"] or c["card_version"] != card["version"]: fail("contract does not bind current approved roadmap card")
 return c
def validate_receipt(r):
 required=("receipt_id","workflow_id","run_id","idempotency_key","ts","mode","trigger","approved_by","action","dry_run","read_back","verified","failure","destination_ref","replay_verified","explicit_instruction")
 for k in required:
  if k not in r: fail(f"receipt missing {k}")
 for k in ("receipt_id","workflow_id","run_id","idempotency_key","ts","trigger","action","read_back","destination_ref"): text(r[k],k)
 if r["mode"] not in MODES or not isinstance(r["dry_run"],bool) or r["verified"] not in (True,False,"pending"): fail("invalid receipt state")
 if not isinstance(r["replay_verified"],bool) or not isinstance(r["explicit_instruction"],bool): fail("receipt proof fields must be boolean")
 if r["approved_by"] is not None: text(r["approved_by"],"approved_by")
 if r["failure"] is not None: text(r["failure"],"failure")
 if r["mode"]=="fixture" and not r["dry_run"]: fail("fixture must be dry-run")
 if r["mode"]=="real" and r["dry_run"]: fail("real run cannot be dry-run")
 if r["mode"]=="activation" and (r["dry_run"] or not r["explicit_instruction"]): fail("activation requires non-dry-run recorded instruction")
 return r
def receipts(workspace):
 p=Path(workspace)/"receipts.jsonl"; return [] if not p.exists() else [validate_receipt(json.loads(x)) for x in p.read_text().splitlines() if x.strip()]
def write_receipts(w, rs): atomic(Path(w)/"receipts.jsonl", "".join(json.dumps(r,separators=(",",":"))+"\n" for r in rs), False)
def workflow_state(s, card): return s.setdefault("workflows",{}).setdefault(card,{"status":"candidate","revision":0,"receipt_ids":[]})
def contract_for(w,r,card_id): return validate_contract(load(Path(w)/"workflows"/card_id/"contract.json"),r,card_for(r,card_id))
def proof_status(r, card_id, rs):
 card=card_for(r,card_id); real=[x for x in rs if x["workflow_id"]==card_id and x["mode"]=="real" and x["verified"] is True and not x["dry_run"] and x["failure"] is None]
 fixture=any(x["workflow_id"]==card_id and x["mode"]=="fixture" and x["verified"] is True and x["failure"] is None for x in rs)
 proven=any(x["replay_verified"] and (not card["approval"]["required"] or x["approved_by"] is not None) for x in real)
 active=any(x["workflow_id"]==card_id and x["mode"]=="activation" and x["verified"] is True and x["failure"] is None and x["explicit_instruction"] for x in rs)
 return "live" if fixture and proven and active else "proven" if fixture and proven else "built" if fixture else "designed"
def reconcile(s,r,card_id,rs):
 x=workflow_state(s,card_id); supported=proof_status(r,card_id,rs)
 if STATUSES.index(x["status"])>STATUSES.index(supported): x["status"]=supported; x["revision"]+=1
 x["receipt_ids"]=[q["receipt_id"] for q in rs if q["workflow_id"]==card_id]
 return x
def init(args):
 w=Path(args.workspace); lock=locked(w)
 try:
  r,s=handoff(w); first=r["first_automation"]
  if first: card_for(r,first)
  current=s.get("foundation",{}); s["foundation"]={"status":"installed","installed_at":current.get("installed_at") or datetime.now(timezone.utc).isoformat(),"revision":current.get("revision",0)+(0 if current.get("status")=="installed" else 1)}
  if first: workflow_state(s,first)
  atomic(w/"state.json",s)
  if not (w/"README.md").exists(): atomic(w/"README.md", "# Operations workspace\n\nStatus lives in `state.json` (`foundation`, `workflows.<card-id>.status`).\n\nRoadmap: roadmap.json; owner result: roadmap.html; state: state.json. Runtime implementation, record source, run, switch, and stop instructions live in workflows/<card-id>/contract.json.\n\nFile map: business.md, roadmap.json, roadmap.html, state.json, rules.md, receipts.jsonl, workflows/.\n", False)
  if not (w/"rules.md").exists(): atomic(w/"rules.md", "# Approved rules\n\n", False)
  if not (w/"receipts.jsonl").exists(): write_receipts(w,[])
  print("installed" if first else "installed; build stopped: "+str(r["first_automation_reason"]))
 finally: lock.close()
def append_receipt(w, receipt):
 rs=receipts(w); r=validate_receipt(receipt); same=[x for x in rs if x["idempotency_key"]==r["idempotency_key"]]
 if any(x["receipt_id"]==r["receipt_id"] for x in rs) or (same and any(x["failure"] is None for x in same)): fail("duplicate receipt or successful idempotency key; replay must not act")
 rs.append(r); write_receipts(w,rs); return r
def append(args):
 lock=locked(args.workspace)
 try: print(append_receipt(args.workspace,load(args.receipt))["receipt_id"])
 finally: lock.close()
def import_records(w, card_id, source):
 source=Path(source); text(str(source),"record source")
 if not source.exists(): fail("external record source does not exist")
 for line in source.read_text().splitlines():
  if line.strip():
   r=validate_receipt(json.loads(line))
   if r["workflow_id"]!=card_id: fail("external receipt workflow mismatch")
   try: append_receipt(w,r)
   except ValueError as e:
    if "duplicate" not in str(e): raise
def transition(args):
 w=Path(args.workspace); lock=locked(w)
 try:
  r,s=handoff(w); card=card_for(r,args.card); contract_for(w,r,args.card); rs=receipts(w); x=reconcile(s,r,args.card,rs); old=x["status"]; target=args.status
  if target not in STATUSES: fail("invalid status")
  if STATUSES.index(target)>STATUSES.index(old)+1: fail("transition skips required predecessor")
  supported=proof_status(r,args.card,rs)
  if STATUSES.index(target)>STATUSES.index(supported): fail("transition lacks current contract-bound proof")
  x["status"]=target; x["revision"]+=1; x["receipt_ids"]=[q["receipt_id"] for q in rs if q["workflow_id"]==args.card]; atomic(w/"state.json",s); print(f"{old} -> {target}")
 finally: lock.close()
def report(args):
 w=Path(args.workspace); lock=locked(w)
 try:
  r,s=handoff(w); c=contract_for(w,r,args.card); source=c["runtime"]["record_source"]
  if source != "receipts.jsonl": import_records(w,args.card,source)
  rs=receipts(w); reconcile(s,r,args.card,rs); atomic(w/"state.json",s)
  good=[q for q in rs if q["workflow_id"]==args.card and q["mode"]=="real" and q["verified"] is True and q["failure"] is None and q["ts"].startswith(args.month)]
  b=c["baseline"]; hours=b.get("hours_per_run"); rate=b.get("hourly_value"); runs=b.get("runs_per_month")
  result={"reporting_month":args.month,"verified_real_runs":len(good),"failures":sum(q["workflow_id"]==args.card and q["failure"] is not None for q in rs),"pending":sum(q["workflow_id"]==args.card and q["verified"]=="pending" for q in rs),"realized_hours":len(good)*hours if isinstance(hours,(int,float)) else None,"realized_value":len(good)*hours*rate if isinstance(hours,(int,float)) and isinstance(rate,(int,float)) else None,"adoption_gap":runs-len(good) if isinstance(runs,(int,float)) else None}; print(json.dumps(result,sort_keys=True))
 finally: lock.close()
def main():
 p=argparse.ArgumentParser(); q=p.add_subparsers(dest="cmd",required=True)
 a=q.add_parser("init"); a.add_argument("workspace")
 a=q.add_parser("validate-contract"); a.add_argument("contract"); a.add_argument("--workspace")
 a=q.add_parser("append-receipt"); a.add_argument("workspace"); a.add_argument("receipt")
 a=q.add_parser("import-records"); a.add_argument("workspace"); a.add_argument("card"); a.add_argument("source")
 a=q.add_parser("transition"); a.add_argument("workspace"); a.add_argument("card"); a.add_argument("status")
 a=q.add_parser("report"); a.add_argument("workspace"); a.add_argument("card"); a.add_argument("month")
 a=p.parse_args()
 try:
  if a.cmd=="init": init(a)
  elif a.cmd=="validate-contract":
   if a.workspace: r,_=handoff(a.workspace); validate_contract(load(a.contract),r,card_for(r,load(a.contract).get("card_id")))
   else: validate_contract(load(a.contract))
   print("valid")
  elif a.cmd=="append-receipt": append(a)
  elif a.cmd=="import-records":
   lock=locked(a.workspace)
   try: import_records(a.workspace,a.card,a.source)
   finally: lock.close()
  elif a.cmd=="transition": transition(a)
  else: report(a)
 except (ValueError,FileNotFoundError,json.JSONDecodeError) as e: print("ERROR: "+str(e),file=sys.stderr); raise SystemExit(1)
if __name__=="__main__": main()
