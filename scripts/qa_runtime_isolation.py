"""Real embedded startup/environment/restart probes on the existing host.

Uses synthetic tripwires and a fresh private data directory, never real user
data. It is not a clean-Windows or external editor compatibility result.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import uuid
import httpx
from build_embedded_runtime import ROOT,verify_sources
from smoke_beta import isolated_environment,read_ready,engine_command,loaded_modules


def probe(runtime):
    verify_sources(runtime,ROOT/'.lumaforge-local/downloads')
    private=ROOT/'.lumaforge-local'/('isolation-'+str(uuid.uuid4()));private.mkdir()
    poisoned=private/'untrusted-cwd';poisoned.mkdir()
    for name in ('numpy.py','sitecustomize.py','usercustomize.py'):
        (poisoned/name).write_text("raise RuntimeError('Synthetic search-path tripwire must never run')\n")
    env=isolated_environment(private/'unused')
    env.update(PYTHONHOME=str(poisoned),PYTHONPATH=str(poisoned),PYTHONUSERBASE=str(poisoned),LOCALAPPDATA=str(private/'localappdata'))
    env.pop('LUMAFORGE_DATA_DIR') # Verify the actual packaged default, not a QA override.
    code="import sys,json,numpy;from pathlib import Path;r=Path(sys.executable).parent;assert Path(numpy.__file__).is_relative_to(r);assert all(Path(p).resolve().is_relative_to(r) for p in sys.path);assert 'sitecustomize' not in sys.modules;print(json.dumps({'isolated':sys.flags.isolated,'ignore_environment':sys.flags.ignore_environment,'no_site':sys.flags.no_site,'no_user_site':sys.flags.no_user_site,'modules_and_search_path_within_bundle':True}))"
    result=subprocess.run([str(runtime/'python.exe'),'-I','-S','-B','-c',code],env=env,cwd=poisoned,capture_output=True,text=True,timeout=45)
    if result.returncode:raise ValueError('Contaminated environment changed embedded startup')
    report=json.loads(result.stdout)
    for phase in ('write','restart'):
        child=subprocess.Popen(engine_command(runtime/'python.exe',os.getpid()),env=env,cwd=poisoned,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
        try:
            ready=read_ready(child)
            with httpx.Client(base_url='http://127.0.0.1:'+str(ready['port']),trust_env=False,timeout=30) as client:
                csrf=client.get('/api/session').json()['csrf'];client.headers.update({'X-LumaForge-Local':'1','X-Color-Studio-Token':csrf})
                if phase=='write':
                    prefs=client.get('/api/preferences').json();prefs.update(workspace='pro',language='en',welcome_seen=True,export_format='jpg')
                    client.put('/api/preferences',json=prefs).raise_for_status()
                    demo=client.post('/api/demo/load',json={});demo.raise_for_status();demo=demo.json()
                    recipe=client.post('/api/fit',json={'source_id':demo['source']['id'],'reference_id':demo['reference']['id']}).json()['recipe']
                    client.post('/api/presets',json={'name':'Isolation QA fixture','recipe':recipe}).raise_for_status()
                else:
                    assert client.get('/api/preferences').json()==prefs,'Preferences lost across embedded restart'
                    presets=client.get('/api/presets').json();assert len(presets)==1 and presets[0]['recipe']==recipe,'Preset lost across embedded restart'
                    report['loaded_modules']=loaded_modules(child,runtime/'python.exe')
        finally:
            if child.poll() is None:child.terminate();child.wait(timeout=10)
    data=private/'localappdata/ColorStudioBetaData'
    assert (data/'preferences.json').is_file(),'Packaged data location changed from beta2'
    verify_sources(runtime,ROOT/'.lumaforge-local/downloads') # No pycache/session files leaked into installation.
    report.update(schema='color-studio-embedded-isolation-v1',default_data_location_preserved=True,preferences_and_preset_survive_restart=True,
                  poisoned_cwd_and_python_environment_ignored=True,installation_tree_unchanged=True,clean_windows=False)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('runtime',type=Path);parser.add_argument('report',type=Path);args=parser.parse_args()
    report=probe(args.runtime.resolve());args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
