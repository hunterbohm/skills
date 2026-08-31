#!/usr/bin/env python3
"""Executable fixture coverage for the foundation contract."""
import concurrent.futures,json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; F=ROOT/'fixtures'; TOOL=ROOT/'scripts'/'foundation.py'
def run(*args): return subprocess.run([sys.executable,str(TOOL),*map(str,args)],capture_output=True,text=True)
def main():
 with tempfile.TemporaryDirectory() as d:
  w=Path(d); shutil.copy(F/'roadmap.json',w/'roadmap.json'); shutil.copy(F/'state.json',w/'state.json')
  # Install accepts only a fully approved, identity-matched audit handoff and is idempotent.
  assert run('init',w).returncode==0 and (w/'README.md').exists() and (w/'rules.md').exists()
  (w/'rules.md').write_text('# Approved rules\n\n- Preserve this\n')
  assert run('init',w).returncode==0 and 'Preserve this' in (w/'rules.md').read_text()
  bad_state=json.loads((w/'state.json').read_text()); bad_state['roadmap_id']='wrong'; (w/'state.json').write_text(json.dumps(bad_state)); assert run('init',w).returncode!=0
  shutil.copy(F/'state.json',w/'state.json')
  (w/'workflows/follow-up').mkdir(parents=True); shutil.copy(F/'contract.json',w/'workflows/follow-up/contract.json')
  assert run('validate-contract',w/'workflows/follow-up/contract.json','--workspace',w).returncode==0
  stale=json.loads((F/'contract.json').read_text()); stale['card_version']=2; x=w/'stale.json'; x.write_text(json.dumps(stale)); assert run('validate-contract',x,'--workspace',w).returncode!=0
  bad=json.loads((F/'contract.json').read_text()); bad['runtime'].pop('secret_store'); x=w/'bad.json'; x.write_text(json.dumps(bad)); assert run('validate-contract',x).returncode!=0
  # Ordered ladder rejects skipped proof, then accepts current fixture proof.
  assert run('transition',w,'follow-up','proven').returncode!=0
  assert run('transition',w,'follow-up','designed').returncode==0
  assert run('append-receipt',w,F/'dry-run-build.json').returncode==0
  assert run('transition',w,'follow-up','built').returncode==0
  # Current real run has structured approval and replay proof; duplicate replay is rejected.
  assert run('append-receipt',w,F/'proven-run.json').returncode==0
  assert run('append-receipt',w,F/'duplicate-replay.json').returncode!=0
  assert run('transition',w,'follow-up','proven').returncode==0
  # Pending and failed verification remain visible; activation requires explicit instruction/read-back.
  assert run('append-receipt',w,F/'verification-pending.json').returncode==0
  assert run('append-receipt',w,F/'verification-failure.json').returncode==0
  assert run('transition',w,'follow-up','live').returncode!=0
  assert run('append-receipt',w,F/'live-activation.json').returncode==0
  assert run('transition',w,'follow-up','live').returncode==0
  # Verified value only: two verified real runs against 4/month baseline -> two-run gap.
  assert run('append-receipt',w,F/'adoption-gap.json').returncode==0
  out=run('report',w,'follow-up','2026-09'); assert out.returncode==0 and '"realized_hours": 3.0' in out.stdout and '"adoption_gap": 2' in out.stdout and '"failures": 1' in out.stdout
  out=run('report',w,'follow-up','2026-10'); assert '"verified_real_runs": 0' in out.stdout and '"adoption_gap": 4' in out.stdout
  # Locked duplicate writes serialize: only one succeeds.
  r=json.loads((F/'failure-rule-proposal.json').read_text()); r['receipt_id']='concurrent'; r['idempotency_key']='concurrent'; q=w/'concurrent.json'; q.write_text(json.dumps(r))
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(lambda _:run('append-receipt',w,q).returncode,range(2)))
  assert results.count(0)==1
  # No-automation install stops Build with roadmap reason.
  n=Path(d)/'no'; n.mkdir(); shutil.copy(F/'no-automation-roadmap.json',n/'roadmap.json'); ns=json.loads((F/'state.json').read_text()); ns['roadmap_id']='no-auto'; ns['owner_approval']=json.loads((F/'no-automation-roadmap.json').read_text())['owner_approval']; (n/'state.json').write_text(json.dumps(ns)); assert 'build stopped' in run('init',n).stdout
 print('ops-foundation tests passed')
if __name__=='__main__': main()
