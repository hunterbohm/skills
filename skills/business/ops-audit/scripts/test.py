#!/usr/bin/env python3
"""Executable contract tests (stdlib only).

Seam under test: `workspace.py plan <workspace> [--full]` prints the plan as chat text or exits non-zero on any
contract violation; `workspace.py step <workspace> <card> <status> --note ...` is the only writer of step status.
"""
import copy, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / 'fixtures/roadmap.json').read_text())
STATE = json.loads((ROOT / 'fixtures/state.json').read_text())


def ws(*args): return subprocess.run([sys.executable, str(ROOT / 'scripts/workspace.py'), *map(str, args)], text=True, capture_output=True)
def workspace(directory, roadmap, state, name='w'):
    w = directory / name; w.mkdir(exist_ok=True)
    (w / 'roadmap.json').write_text(json.dumps(roadmap)); (w / 'state.json').write_text(json.dumps(state)); return w
def plan(directory, roadmap, state=STATE, *flags): return ws('plan', workspace(directory, roadmap, state), *flags)
def rejected(directory, roadmap, why, state=STATE):
    result = plan(directory, roadmap, state)
    assert result.returncode != 0 and result.stdout == '', why


def main():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)

        # The plan prints as chat text: main lane numbered and in order, then any-time steps, then holds.
        good = plan(d, FIXTURE); assert good.returncode == 0, good.stderr
        text = good.stdout
        first, second = FIXTURE['plan']['steps'][0], FIXTURE['plan']['steps'][1]
        assert text.index('1. ' + first['title']) < text.index('2. ' + second['title']) < text.index('Any time') < text.index('On hold')
        assert 'Next: needs your go' in text and 'Later' in text and text.index('Next: needs your go') < text.index('Later')
        for card in FIXTURE['cards']: assert card['id'] not in text, card['id']
        for word in ('WP-', 'UNKNOWN', 'verdict', 'causal', 'register'): assert word not in text, word
        assert first['do'][0] not in text and first['you_decide'] in text, 'the short plan is the title and the one decision per step'
        full = plan(d, FIXTURE, STATE, '--full'); assert full.returncode == 0, full.stderr
        for line in first['do'] + [first['you_decide'], first['done_when'], second['never']]: assert line in full.stdout, line
        assert '4 hours a month today, about $2,400 a year' in full.stdout
        assert 'not yet approved' in text
        # A focus names the audit's scope in the head line; extensions print as what the owner could add.
        assert 'If you add:' in text and 'a browser tool the agent can drive' in text, text
        focused = copy.deepcopy(FIXTURE); focused['focus'] = 'email triage'
        assert 'focused on email triage' in plan(d, focused).stdout
        bad = copy.deepcopy(FIXTURE); bad['extensions'] = [{'add': 'x'}]; rejected(d, bad, 'an extension names what it unlocks')
        bad = copy.deepcopy(FIXTURE); bad['focus'] = 7; rejected(d, bad, 'focus is a string or null')

        # Plan invariants are rejected before anything prints.
        bad = copy.deepcopy(FIXTURE); bad.pop('plan'); rejected(d, bad, 'missing plan')
        bad = copy.deepcopy(FIXTURE); bad['plan'] = None; rejected(d, bad, 'complete roadmap needs a plan')
        bad = copy.deepcopy(FIXTURE); bad['plan']['steps'].pop(); rejected(d, bad, 'every card must be in a step')
        bad = copy.deepcopy(FIXTURE); bad['plan']['steps'].append(copy.deepcopy(bad['plan']['steps'][0])); rejected(d, bad, 'a card may appear once')
        bad = copy.deepcopy(FIXTURE); bad['plan']['steps'][0]['card'] = 'ghost'; rejected(d, bad, 'a step must name a card')
        bad = copy.deepcopy(FIXTURE); bad['plan']['steps'][0], bad['plan']['steps'][1] = bad['plan']['steps'][1], bad['plan']['steps'][0]; rejected(d, bad, 'first main step must be first_move')
        bad = copy.deepcopy(FIXTURE); bad['first_automation'] = None; bad['first_automation_reason'] = 'none'; rejected(d, bad, 'an automation step needs first_automation')
        bad = copy.deepcopy(FIXTURE); bad['plan']['steps'][0]['lane'] = 'side'; rejected(d, bad, 'lane is main or parallel')
        bad = copy.deepcopy(FIXTURE); bad['plan']['steps'][0]['do'] = []; rejected(d, bad, 'a step needs one to three do lines')
        bad = copy.deepcopy(FIXTURE); bad['plan']['steps'][0]['do'] = ['a', 'b', 'c', 'd']; rejected(d, bad, 'a step needs one to three do lines')
        bad = copy.deepcopy(FIXTURE); bad['plan']['steps'][0]['title'] = ''; rejected(d, bad, 'a step needs a title')
        bad = copy.deepcopy(FIXTURE); bad['plan']['steps'][0]['lane'] = 'parallel'; rejected(d, bad, 'first_move must sit in the main lane')
        bad = copy.deepcopy(FIXTURE)
        for step in bad['plan']['steps']: step['lane'] = 'parallel'
        rejected(d, bad, 'a plan needs a main lane')
        manual = copy.deepcopy(FIXTURE); manual['cards'][1]['verdict'] = 'leverage move'; manual['cards'][1]['intervention'] = 'leverage move'
        manual['first_automation'] = None; manual['first_automation_reason'] = 'No safe automation has evidence yet.'
        result = plan(d, manual); assert result.returncode == 0 and 'No safe automation has evidence yet.' in result.stdout

        # Card and roadmap contracts hold.
        for key in ('roadmap_id', 'business', 'date', 'revision', 'incomplete', 'stopping_point', 'consent', 'exclusions', 'cards', 'first_move', 'first_automation', 'first_automation_reason', 'owner_approval'):
            bad = copy.deepcopy(FIXTURE); bad.pop(key); rejected(d, bad, f'missing {key}')
        for key in ('id', 'version', 'action', 'hours_per_month', 'hourly_value', 'annual_labor_value', 'causal_path', 'evidence', 'existing_coverage', 'gaps', 'approval', 'intervention', 'diagnosis', 'proof', 'verdict'):
            bad = copy.deepcopy(FIXTURE); bad['cards'][0].pop(key); rejected(d, bad, f'missing card {key}')
        bad = copy.deepcopy(FIXTURE); bad['cards'][0]['annual_labor_value'] = 1; rejected(d, bad, 'derived cost must agree')
        bad = copy.deepcopy(FIXTURE); bad['cards'][0]['hours_per_month'] = None; rejected(d, bad, 'annual must be null when hours unknown')
        bad = copy.deepcopy(FIXTURE); bad['cards'][0]['evidence'][0]['label'] = 'guess'; rejected(d, bad, 'evidence label')
        bad = copy.deepcopy(FIXTURE); bad['cards'][0]['approval'] = {'required': True, 'approver': None, 'gate': None}; rejected(d, bad, 'required approval names approver and gate')
        bad = copy.deepcopy(FIXTURE); bad['roadmap_id'] = 'id with spaces'; rejected(d, bad, 'identifier')

        # An incomplete audit prints the stopping point and carries no plan.
        partial = copy.deepcopy(FIXTURE); partial.update({'incomplete': True, 'stopping_point': 'consent interview', 'cards': [], 'plan': None, 'first_move': None, 'first_automation': None, 'first_automation_reason': None})
        pstate = copy.deepcopy(STATE); pstate.update({'incomplete': True, 'stopped_at': 'consent interview'})
        result = plan(d, partial, pstate); assert result.returncode == 0 and 'consent interview' in result.stdout and '1. ' not in result.stdout
        partial['plan'] = FIXTURE['plan']; rejected(d, partial, 'incomplete roadmap cannot carry a plan', pstate)

        # State must match the roadmap and keep its own contract.
        stale = copy.deepcopy(STATE); stale['revision'] = 2; rejected(d, FIXTURE, 'revision mismatch', stale)
        wrong = copy.deepcopy(STATE); wrong['steps'] = {'meeting-actions': {'status': 'live', 'note': 'x', 'date': 'y'}}; rejected(d, FIXTURE, 'unknown status', wrong)
        wrong = copy.deepcopy(STATE); wrong['steps'] = {'report-format': {'status': 'done', 'note': 'x', 'date': 'y'}}; rejected(d, FIXTURE, 'a hold cannot be done', wrong)
        malformed = copy.deepcopy(STATE); malformed['changes'] = [{'revision': 1, 'date': 'x', 'summary': 'y'}]; rejected(d, FIXTURE, 'change revision', malformed)
        for key in ('changes', 'steps'):
            malformed = copy.deepcopy(STATE); malformed.pop(key); rejected(d, FIXTURE, key, malformed)

        # A revision with no change entry, or a malformed evidence entry, is rejected.
        rev = copy.deepcopy(FIXTURE); rev['revision'] = 3; rstate = copy.deepcopy(STATE); rstate['revision'] = 3; rstate['changes'] = [{'revision': 2, 'date': 'x', 'summary': 'y'}]
        rejected(d, rev, 'one change entry per revision', rstate)
        rstate['changes'].append({'revision': 3, 'date': 'x', 'summary': 'z'}); assert plan(d, rev, rstate).returncode == 0
        bad_ev = copy.deepcopy(STATE); bad_ev['evidence'] = [1, 'x']; rejected(d, FIXTURE, 'evidence items', bad_ev)

        # No step moves on an unapproved plan; steps move forward only, in plan order, on the owner's recorded words.
        assert ws('step', workspace(d, FIXTURE, STATE, 'unapproved'), 'meeting-actions', 'approved', '--note', 'no approval yet').returncode != 0
        APPROVAL = {'roadmap_id': FIXTURE['roadmap_id'], 'roadmap_revision': FIXTURE['revision'], 'approved_by': 'Owner', 'approved_at': '2026-08-31'}
        approved = copy.deepcopy(FIXTURE); approved['owner_approval'] = APPROVAL
        astate = copy.deepcopy(STATE); astate['owner_approval'] = APPROVAL
        w = workspace(d, approved, astate, 'steps')
        assert ws('step', w, 'meeting-actions', 'approved').returncode != 0
        assert ws('step', w, 'lead-follow-up', 'approved', '--note', 'too early').returncode != 0
        assert ws('step', w, 'meeting-actions', 'done', '--note', 'skipping approval').returncode != 0
        out = ws('step', w, 'meeting-actions', 'approved', '--note', 'Owner said go in chat, 2026-09-02'); assert out.returncode == 0, out.stderr
        assert 'Approved, in progress' in out.stdout, 'a step change prints the plan'
        assert json.loads((w / 'state.json').read_text())['steps']['meeting-actions']['note'] == 'Owner said go in chat, 2026-09-02'
        assert ws('step', w, 'meeting-actions', 'done', '--note', 'Page made; seven actions moved; page reopened and read.').returncode == 0
        assert ws('step', w, 'meeting-actions', 'approved', '--note', 'backwards').returncode != 0
        after = ws('plan', w).stdout; assert f"1. {first['title']}  [Done]" in after and f"2. {second['title']}  [Next: needs your go]" in after
        assert ws('step', w, 'lead-follow-up', 'approved', '--note', 'Owner approved the draft job, 2026-09-03').returncode == 0
        assert 'Running' in ws('step', w, 'lead-follow-up', 'done', '--note', 'Draft job runs on the owner cron; switch off with the cron toggle.').stdout
        assert ws('step', w, 'report-format', 'ended').returncode != 0
        assert ws('step', w, 'report-format', 'ended', '--note', 'Owner: two cycles done, decide now').returncode == 0
        assert ws('step', w, 'calendar-prep-check', 'live', '--note', 'x').returncode != 0
        assert json.loads((w / 'state.json').read_text())['revision'] == 1, 'status changes do not touch the plan revision'

        # Harness discovery finds known stores by convention and unknown session folders by shape; metadata only.
        home = d / 'home'; (home / '.claude/projects/-p').mkdir(parents=True); (home / '.codex/sessions/2026/09/01').mkdir(parents=True); (home / '.mystery/sessions').mkdir(parents=True); (home / '.mutagen/sessions').mkdir(parents=True)
        shutil.copy(ROOT / 'fixtures/sessions/claude-projects/-Users-owner-proj/11111111-aaaa-bbbb-cccc-000000000001.jsonl', home / '.claude/projects/-p/a.jsonl')
        shutil.copy(ROOT / 'fixtures/sessions/codex-sessions/2026/09/01/rollout-2026-09-01T10-00-00-0000.jsonl', home / '.codex/sessions/2026/09/01/r.jsonl')
        for i in range(3): (home / f'.mystery/sessions/s{i}.jsonl').write_text('{"role":"user","content":"hi"}\n'); (home / f'.mutagen/sessions/m{i}.json').write_text('{}')
        inv = subprocess.run([sys.executable, str(ROOT / 'scripts/harnesses.py'), 'inventory', '--home', str(home), '--json'], text=True, capture_output=True)
        assert inv.returncode == 0, inv.stderr
        rows = {r['harness']: r for r in json.loads(inv.stdout)}
        assert rows['claude-code']['files'] == 1 and rows['codex']['files'] == 1 and rows['unknown']['root'].endswith('.mystery/sessions'), rows
        assert not any('mutagen' in r['root'] for r in rows.values()), 'sync tooling is not an agent'
        assert all(k in rows['codex'] for k in ('bytes', 'oldest', 'newest')), rows['codex']
        assert 'hi' not in inv.stdout, 'inventory reads no content'
        # A store rooted at the home directory (aider) must not silence unknown-harness discovery; brackets in home are fine.
        (home / '.aider.chat.history.md').write_text('#### hi\n')
        inv2 = json.loads(subprocess.run([sys.executable, str(ROOT / 'scripts/harnesses.py'), 'inventory', '--home', str(home), '--json'], text=True, capture_output=True).stdout)
        assert {r['harness'] for r in inv2} >= {'aider', 'unknown', 'claude-code'}, inv2
        bhome = d / 'H[x]'; shutil.copytree(home, bhome)
        inv3 = json.loads(subprocess.run([sys.executable, str(ROOT / 'scripts/harnesses.py'), 'inventory', '--home', str(bhome), '--json'], text=True, capture_output=True).stdout)
        assert any(r['harness'] == 'claude-code' for r in inv3), 'bracketed home must still be scanned'
        # A remote login banner before the JSON must not break the remote inventory.
        fake = d / 'bin'; fake.mkdir(); (fake / 'ssh').write_text('#!/bin/sh\necho "[2026-09-02 09:00] Welcome to acme-build-01"\ncat >/dev/null\necho \'[{"harness":"codex","root":"/r","format":"jsonl","files":1,"bytes":10,"oldest":"2026-01-01","newest":"2026-01-02"}]\'\n'); (fake / 'ssh').chmod(0o755)
        env = dict(os.environ, PATH=f"{fake}:{os.environ['PATH']}")
        rem = subprocess.run([sys.executable, str(ROOT / 'scripts/harnesses.py'), 'inventory', '--host', 'acme-build-01'], text=True, capture_output=True, env=env)
        assert rem.returncode == 0 and 'codex' in rem.stdout, rem.stderr + rem.stdout

        # The connections inventory names connector CLIs, MCP servers per harness, and secret stores, by name and sign-in state only.
        chome = d / 'chome'; (chome / '.codex').mkdir(parents=True); (chome / '.config/opencode').mkdir(parents=True)
        (chome / '.claude.json').write_text(json.dumps({'mcpServers': {'gmail': {'command': 'x', 'env': {'TOKEN': 'sekrit-value-123'}}}}))
        (chome / '.codex/config.toml').write_text('[mcp_servers.linear]\ncommand = "x"\n[mcp_servers.notion]\ncommand = "y"\n')
        (chome / '.config/opencode/opencode.json').write_text(json.dumps({'mcp': {'exa': {'type': 'remote', 'url': 'https://example.com/mcp?key=sekrit-value-123'}}}))
        cbin = d / 'cbin'; cbin.mkdir()
        (cbin / 'composio').write_text('#!/bin/sh\necho "{\"email\":\"owner@example.com\"}"\n'); (cbin / 'composio').chmod(0o755)
        (cbin / 'gog').write_text('#!/bin/sh\necho "no token" >&2; exit 1\n'); (cbin / 'gog').chmod(0o755)
        cenv = dict(os.environ, PATH=f"{cbin}:/usr/bin:/bin", HOME=str(chome))
        con = subprocess.run([sys.executable, str(ROOT / 'scripts/connections.py'), 'inventory', '--home', str(chome), '--json'], text=True, capture_output=True, env=cenv)
        assert con.returncode == 0, con.stderr
        rows = json.loads(con.stdout); by = {(r['kind'], r['name']): r for r in rows}
        assert by[('cli', 'composio')]['status'] == 'signed in' and by[('cli', 'gog')]['status'] == 'present, not signed in', rows
        assert by[('mcp', 'gmail')]['harness'] == 'claude-code' and by[('mcp', 'linear')]['harness'] == 'codex' and by[('mcp', 'exa')]['harness'] == 'opencode', rows
        assert 'sekrit-value-123' not in con.stdout and 'owner@example.com' not in con.stdout, 'inventory prints names and states, never values'
        assert not any(r['name'] == 'xurl' for r in rows), 'absent CLIs are not listed'

        # Digests are bounded and redacted; the self-test covers every parser.
        assert subprocess.run([sys.executable, str(ROOT / 'scripts/digest.py'), '--self-test'], text=True, capture_output=True).returncode == 0

        # The example plan avoids audit vocabulary; agents copy the example.
        banned = ('register', 'migration', 'consented', 'read-back', 'read back', 'waypoint', 'canonical', 'causal', 'verdict', 'intervention', 'idempotency', 'truncated', 'leverage move', 'keep human')
        plan_text = ' '.join(' '.join([s['title'], *s['do'], s['you_decide'], s['done_when'], s['never'] or '']) for s in FIXTURE['plan']['steps']).lower()
        for word in banned: assert word not in plan_text, word
    print('ops-audit tests passed')


if __name__ == '__main__':
    main()
