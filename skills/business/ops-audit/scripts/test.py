#!/usr/bin/env python3
"""Executable contract and safety tests (stdlib only)."""
import concurrent.futures, copy, json, os, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; FIXTURE = json.loads((ROOT / 'fixtures/roadmap.json').read_text())
def run(*args, env=None): return subprocess.run(args, text=True, capture_output=True, env=env)
def render(data, directory):
    path = directory / 'roadmap.json'; path.write_text(json.dumps(data)); return run(sys.executable, str(ROOT/'scripts/render.py'), str(path))
def state(road): return {'roadmap_id':road['roadmap_id'],'revision':road['revision'],'consent':road['consent'],'exclusions':road['exclusions'],'evidence':[],'feedback_ledger':[],'feedback_by_roadmap':{},'incomplete':False,'stopped_at':None,'owner_approval':None}
def feedback(road, line='- card meeting-actions version 1: change | note: Make it shorter'):
    return f"Feedback on roadmap {road['roadmap_id']} revision {road['revision']}.\nUpdate the ledger, then resume the audit to apply the requested semantic change and re-render.\n{line}\n"
def main():
 with tempfile.TemporaryDirectory() as tmp:
  d=Path(tmp)
  good=render(FIXTURE,d); assert good.returncode == 0 and '<script>' in good.stdout and 'Now' in good.stdout and 'Next' in good.stdout and 'Later' in good.stdout
  # The offline artifact has its own branded, accessible visual states; no external assets or UA-only controls.
  for marker in ('<html lang="en">', '--paper:#FFFCF0', 'class="chart-head"', 'class="route-rule"', 'class="metrics"', 'class="route-card first-move-card"', 'class="action-label first-move"', 'class="definition-grid"', 'class="clean"', 'class="note-label"', 'textarea.error', '#status.success', '@media print'):
   assert marker in good.stdout
  assert '#174ea6' not in good.stdout and '#777' not in good.stdout and '@import' not in good.stdout
  page=d/'roadmap.html'; page.write_text(good.stdout); assert run('node', str(ROOT/'scripts/browser_test.js'), str(page)).returncode == 0
  # Every complete-roadmap invariant is rejected by the renderer/one canonical validator.
  cases=[]
  for key in ('roadmap_id','business','date','revision','incomplete','stopping_point','consent','exclusions','cards','first_move','first_automation','first_automation_reason','pending_feedback'):
   bad=copy.deepcopy(FIXTURE); bad.pop(key); cases.append(bad)
  bad=copy.deepcopy(FIXTURE); bad['cards']=[]; cases.append(bad)
  for key in ('id','version','group','action','hours_per_month','hourly_value','annual_labor_value','causal_path','evidence','existing_coverage','gaps','approval','intervention','diagnosis','proof','verdict'):
   bad=copy.deepcopy(FIXTURE); bad['cards'][0].pop(key); cases.append(bad)
  bad=copy.deepcopy(FIXTURE); bad['first_move']='missing'; cases.append(bad)
  bad=copy.deepcopy(FIXTURE); bad['first_automation']='meeting-actions'; cases.append(bad)
  bad=copy.deepcopy(FIXTURE); bad['cards'][0]['annual_labor_value']=1; cases.append(bad)
  bad=copy.deepcopy(FIXTURE); bad['cards'][0]['hourly_value']=None; cases.append(bad)
  bad=copy.deepcopy(FIXTURE); bad['roadmap_id']='id with spaces'; cases.append(bad)
  bad=copy.deepcopy(FIXTURE); bad['cards'][0]['id']='card with spaces'; cases.append(bad)
  # Hours and rate may be independently unknown; annual value is only known when both are known.
  partial_cost=copy.deepcopy(FIXTURE); partial_cost['cards'][0].update({'hours_per_month':None,'annual_labor_value':None}); assert render(partial_cost,d).returncode == 0
  partial_cost=copy.deepcopy(FIXTURE); partial_cost['cards'][0].update({'hourly_value':None,'annual_labor_value':None}); assert render(partial_cost,d).returncode == 0
  partial_cost=copy.deepcopy(FIXTURE); partial_cost['cards'][0].update({'hours_per_month':None}); cases.append(partial_cost)
  bad=copy.deepcopy(FIXTURE); bad['cards'][0]['evidence'][0]['label']='guess'; cases.append(bad)
  bad=copy.deepcopy(FIXTURE); bad['cards'][0]['existing_coverage'].pop('outputs'); cases.append(bad)
  bad=copy.deepcopy(FIXTURE); bad['cards'][0]['causal_path'].pop('read_back'); cases.append(bad)
  bad=copy.deepcopy(FIXTURE); bad['cards'][0]['approval']={'required':True,'approver':None,'gate':None}; cases.append(bad)
  bad=copy.deepcopy(FIXTURE); bad['cards'][0]['intervention']='magic'; cases.append(bad)
  for item in cases: assert render(item,d).returncode != 0
  partial=copy.deepcopy(FIXTURE); partial.update({'incomplete':True,'stopping_point':'consent interview','cards':[],'first_move':None,'first_automation':None,'first_automation_reason':''})
  result=render(partial,d); assert result.returncode == 0 and 'Audit incomplete' in result.stdout and 'No recommendations' in result.stdout and 'Feedback for this action' not in result.stdout
  injected=copy.deepcopy(FIXTURE); injected['business']='</title><img src=x onerror=alert(1)>'; injected['cards'][0]['action']='</script><script>alert(1)</script>'; injected['cards'][0]['evidence'][0]['claim']='" onfocus="alert(2)'
  output=render(injected,d).stdout; assert '</script><script>alert' not in output and '&lt;img' in output and 'onfocus=&quot;' in output
  rp=d/'road.json'; sp=d/'state.json'; fp=d/'feedback.txt'; rp.write_text(json.dumps(FIXTURE)); sp.write_text(json.dumps(state(FIXTURE))); fp.write_text(feedback(FIXTURE))
  command=(sys.executable,str(ROOT/'scripts/apply_feedback.py'),str(sp),str(rp),str(fp))
  assert run(*command).returncode == 0
  road_after=json.loads(rp.read_text()); state_after=json.loads(sp.read_text()); assert road_after['revision']==state_after['revision']==2 and road_after['pending_feedback'][0]['status']=='pending' and state_after['feedback_by_roadmap'][FIXTURE['roadmap_id']]['cards']['meeting-actions'][0]['note']=='Make it shorter'
  # Boundary identifiers render and round-trip through the feedback grammar.
  boundary=copy.deepcopy(FIXTURE); boundary['roadmap_id']='Roadmap_9-x'; boundary['cards'][0]['id']='Card_9-x'; boundary['first_move']='Card_9-x'
  rp.write_text(json.dumps(boundary)); sp.write_text(json.dumps(state(boundary))); fp.write_text(feedback(boundary, '- card Card_9-x version 1: accept | note: Confirmed'))
  assert render(boundary,d).returncode == 0 and run(*command).returncode == 0
  assert run(*command).returncode != 0 # duplicate after coherent transaction
  # Cross-roadmap feedback and change-without-note are blocked before writing.
  rp.write_text(json.dumps(FIXTURE)); sp.write_text(json.dumps(state(FIXTURE))); fp.write_text(feedback(FIXTURE).replace(FIXTURE['roadmap_id'],'other-roadmap'))
  assert run(*command).returncode != 0; assert json.loads(sp.read_text())['revision']==1
  fp.write_text(feedback(FIXTURE, '- card meeting-actions version 1: change | note: ')); assert run(*command).returncode != 0
  # State contract (including consent/exclusion structure) is enforced before feedback writes.
  malformed=state(FIXTURE); malformed['consent']=[{'category':'documents'}]; sp.write_text(json.dumps(malformed)); fp.write_text(feedback(FIXTURE)); assert run(*command).returncode != 0
  sp.write_text(json.dumps(state(FIXTURE)))
  # Concurrent readers serialize: one write wins and no feedback event is lost/duplicated.
  fp.write_text(feedback(FIXTURE));
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: outcomes=list(pool.map(lambda _:run(*command).returncode, range(2)))
  assert outcomes.count(0)==1 and json.loads(sp.read_text())['revision']==2
  # Interrupted second-file write leaves a journal; next invocation recovers both revisions deterministically.
  rp.write_text(json.dumps(FIXTURE)); sp.write_text(json.dumps(state(FIXTURE))); env=dict(os.environ, OPS_AUDIT_TEST_FAIL_AFTER_ROADMAP='1'); assert run(*command,env=env).returncode != 0
  assert (d/'.ops-audit-feedback.transaction.json').exists(); assert run(*command).returncode != 0
  assert json.loads(rp.read_text())['revision']==json.loads(sp.read_text())['revision']==2 and not (d/'.ops-audit-feedback.transaction.json').exists()
 print('ops-audit tests passed')
if __name__=='__main__': main()
