#!/usr/bin/env python3
"""Record validated feedback as pending events; this never rewrites card recommendations."""
from __future__ import annotations
import fcntl
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from validator import validate_roadmap, validate_state

HEADER = re.compile(r'^Feedback on roadmap ([A-Za-z0-9_-]+) revision (\d+)\.\nUpdate the ledger, then resume the audit to apply the requested semantic change and re-render\.\n')
LINE = re.compile(r'^- card ([A-Za-z0-9_-]+) version (\d+): (accept|change|reject) \| note: ([^\r\n]*)$')

def conflict(message): raise ValueError(message)
def fsync_directory(directory):
    fd = os.open(directory, os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)
def atomic(path, data):
    fd, temp = tempfile.mkstemp(prefix='.ops-audit-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2); handle.write('\n'); handle.flush(); os.fsync(handle.fileno())
        os.replace(temp, path); fsync_directory(path.parent)
    finally:
        if os.path.exists(temp): os.unlink(temp)
def recover(journal, roadmap_path, state_path):
    if not journal.exists(): return
    record = json.loads(journal.read_text(encoding='utf-8'))
    if record.get('roadmap_path') != roadmap_path.name or record.get('state_path') != state_path.name: conflict('transaction journal does not match inputs')
    atomic(roadmap_path, record['roadmap']); atomic(state_path, record['state']); journal.unlink(); fsync_directory(journal.parent)
def parse(raw, roadmap, state):
    normalized = raw.replace('\r\n', '\n').strip() + '\n'; match = HEADER.match(normalized)
    if not match: conflict('malformed feedback')
    roadmap_id, revision = match.groups()
    if roadmap_id != roadmap['roadmap_id']: conflict('cross-roadmap feedback block')
    if int(revision) != roadmap['revision'] or state['revision'] != roadmap['revision']: conflict('ledger revision conflict')
    identity = hashlib.sha256(normalized.encode()).hexdigest()
    if identity in state['feedback_ledger']: conflict('duplicate feedback block')
    lines = normalized[match.end():].strip().splitlines()
    if not lines or lines == ['']: conflict('no feedback marks')
    cards = {card['id']: card for card in roadmap['cards']}; events = []
    for line in lines:
        found = LINE.match(line)
        if not found: conflict('invalid feedback line')
        card_id, version, choice, note = found.groups()
        if card_id not in cards or int(version) != cards[card_id]['version']: conflict('stale card version')
        if choice == 'change' and not note.strip(): conflict('change needs note')
        events.append({'event_id': hashlib.sha256((identity + card_id).encode()).hexdigest(), 'roadmap_id': roadmap['roadmap_id'], 'roadmap_revision': roadmap['revision'], 'card_id': card_id, 'card_version': int(version), 'choice': choice, 'note': note, 'status': 'pending'})
    if len({event['card_id'] for event in events}) != len(events): conflict('duplicate card block')
    return identity, events

def main():
    if len(sys.argv) != 4: raise SystemExit('usage: apply_feedback.py state.json roadmap.json feedback.txt')
    state_path, roadmap_path, feedback_path = map(Path, sys.argv[1:])
    if state_path.parent != roadmap_path.parent: conflict('state and roadmap must share a workspace')
    lock_path = state_path.parent / '.ops-audit-feedback.lock'; journal = state_path.parent / '.ops-audit-feedback.transaction.json'
    with lock_path.open('a+') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        recover(journal, roadmap_path, state_path)
        roadmap = validate_roadmap(json.loads(roadmap_path.read_text(encoding='utf-8')))
        state = validate_state(json.loads(state_path.read_text(encoding='utf-8')))
        if state['roadmap_id'] != roadmap['roadmap_id']: conflict('cross-roadmap state')
        if state['incomplete'] != roadmap['incomplete'] or state['stopped_at'] != roadmap['stopping_point']: conflict('state and roadmap completion status conflict')
        raw = feedback_path.read_text(encoding='utf-8')
        identity, events = parse(raw, roadmap, state)
        new_revision = roadmap['revision'] + 1
        roadmap['revision'] = new_revision; roadmap['pending_feedback'].extend(events)
        state['revision'] = new_revision; state['feedback_ledger'].append(identity)
        bucket = state['feedback_by_roadmap'].setdefault(roadmap['roadmap_id'], {'revision': new_revision, 'cards': {}})
        bucket['revision'] = new_revision
        for event in events: bucket['cards'].setdefault(event['card_id'], []).append(event)
        validate_roadmap(roadmap); validate_state(state)
        record = {'roadmap_path': roadmap_path.name, 'state_path': state_path.name, 'roadmap': roadmap, 'state': state}
        atomic(journal, record); atomic(roadmap_path, roadmap)
        if os.environ.get('OPS_AUDIT_TEST_FAIL_AFTER_ROADMAP') == '1': raise OSError('injected failure after roadmap write')
        atomic(state_path, state); journal.unlink(); fsync_directory(journal.parent)
    print('recorded', len(events), 'pending feedback marks; resume the audit to apply semantic changes')

if __name__ == '__main__':
    try: main()
    except (ValueError, json.JSONDecodeError, OSError) as error: raise SystemExit('feedback conflict: ' + str(error))
