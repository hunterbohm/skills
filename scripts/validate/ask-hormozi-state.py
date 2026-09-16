#!/usr/bin/env python3
"""Exercise package replacement and unsafe state paths using disposable data."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

SOURCE = Path(__file__).resolve().parents[2] / 'skills/business/ask-hormozi/scripts/ledger.py'

with tempfile.TemporaryDirectory(prefix='ask-hormozi-state-') as tmp:
    base = Path(tmp)
    package = base / 'installation/skills/ask-hormozi'
    def install():
        (package / 'scripts').mkdir(parents=True)
        (package / 'SKILL.md').write_text('# Disposable skill fixture\n')
        shutil.copy2(SOURCE, package / 'scripts/ledger.py')
    install()
    env = {**os.environ, 'XDG_CONFIG_HOME': str(base / 'config')}
    env.pop('ASK_HORMOZI_ADVISORY_ROOT', None)
    def run(*args, overrides=None, ok=True):
        result = subprocess.run(['python3', str(package / 'scripts/ledger.py'), *args],
                                env={**env, **(overrides or {})}, capture_output=True, text=True)
        assert (result.returncode == 0) == ok, (args, result.stdout, result.stderr)
        return result
    data = base / 'business-memory'
    run('root', '--set', str(data))
    run('init', 'fictional-roofing', '--business', 'Fictional Roofing')
    run('append', 'fictional-roofing', '--branch', 'advise', '--summary', 'First advice',
        '--model', 'offer=Roof replacements', '--action', 'Check margin')
    state = data / 'fictional-roofing/advisory.json'
    config = base / 'config/ask-hormozi/config.json'
    state_before, config_before = state.read_bytes(), config.read_bytes()
    # Model an installer replacing the package, not touching external user data.
    shutil.rmtree(package)
    install()
    opened = json.loads(run('open', 'fictional-roofing').stdout)
    assert opened['model']['offer'] == 'Roof replacements'
    assert opened['_open_prescriptions'][0]['action'] == 'Check margin'
    assert state.read_bytes() == state_before and config.read_bytes() == config_before
    run('validate', 'fictional-roofing')
    run('append', 'fictional-roofing', '--branch', 'advise', '--summary', 'New question', '--allow-unresolved')
    assert json.loads(state.read_text())['prescriptions'] == json.loads(state_before)['prescriptions']
    for unsafe in [package / 'data', package.parent / 'shared-data']:
        run('root', '--set', str(unsafe), '--force', ok=False)
        assert not unsafe.exists()
    # An old unsafe environment override must fail without replacing history.
    run('init', 'unsafe', overrides={'ASK_HORMOZI_ADVISORY_ROOT': str(package)}, ok=False)
    link = base / 'linked-install'
    link.symlink_to(package, target_is_directory=True)
    run('root', '--set', str(link / 'data'), '--force', ok=False)
    run('root', '--set', str(base / 'other-data'), '--force',
        overrides={'XDG_CONFIG_HOME': str(package / 'config')}, ok=False)
    assert not (package / 'config').exists()
    # A per-business symlink cannot redirect a safe root back into the package.
    (data / 'unsafe').symlink_to(package, target_is_directory=True)
    run('init', 'unsafe', ok=False)
    assert not (package / 'advisory.json').exists()
    # Protect the atomic-write temporary path too.
    victim = package / 'protected.txt'
    victim.write_text('unchanged')
    state.with_suffix('.json.tmp').symlink_to(victim)
    prior = state.read_bytes()
    run('append', 'fictional-roofing', '--branch', 'advise', '--summary', 'Rejected', '--allow-unresolved', ok=False)
    assert state.read_bytes() == prior and victim.read_text() == 'unchanged'
    assert config.read_bytes() == config_before
print('Ask Hormozi external-state tests passed: replacement, context/history preservation, unsafe roots, config and symlinks')
