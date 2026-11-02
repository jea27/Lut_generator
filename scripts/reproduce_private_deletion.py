"""Contained incident probe. Only synthetic files in a fresh workspace fixture.

Never accepts a user data directory. Legacy mode executes the exact pre-incident
API Git blob solely to demonstrate its deletion policy, not to attribute the
historical NTFS events. All deletion attempts outside the fixture are denied by
a Python audit hook. Fixtures and private traces are retained, not cleaned up.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import types
import uuid

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
LEGACY='eb3866dfdf9cfc605ae56859d6127dfadd43e2f7'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=('legacy','contained'),required=True)
    parser.add_argument('--probe',choices=('images','batch-part'),default='images')
    args=parser.parse_args()
    private=ROOT/'.lumaforge-local'
    if private.is_symlink() or private.resolve()!=private.absolute():raise RuntimeError('Refuse linked workspace fixture root')
    folder=private/('data-incident-repro-'+uuid.uuid4().hex);folder.mkdir()
    data=folder/'ColorStudioBetaData';(data/'images').mkdir(parents=True);(data/'presets').mkdir()
    for index in range(1,7):(data/'images'/f'{uuid.UUID(int=index)}.png').write_bytes(b'Inert synthetic PNG sentinel')
    for index in (7,8):(data/'presets'/f'{uuid.UUID(int=index)}.json').write_bytes(b'{"fixture":"inert preset"}')
    (data/'preferences.json').write_bytes(b'{"workspace":"pro"}')
    os.environ['LUMAFORGE_DATA_DIR']=str(data)
    os.environ['TEMP']=os.environ['TMP']=str(folder)
    trace=[]
    def audit(event,values):
        if event not in ('os.remove','os.rmdir'):return
        path=Path(os.fsdecode(values[0])).absolute()
        if len(values)>1 and values[1] not in (-1,None):raise RuntimeError('Unresolved dir_fd deletion refused')
        if not path.resolve().is_relative_to(folder.resolve()):raise RuntimeError('Deletion outside owned fixture refused')
        trace.append({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),
                      'event':event,'relative_fixture_path':str(path.relative_to(folder))})
    sys.addaudithook(audit)
    source_path='apps/api/main.py' if args.probe=='images' else 'apps/api/jobs.py'
    if args.mode=='legacy':
        source=subprocess.check_output(['git','show',LEGACY+':'+source_path],cwd=ROOT)
        module=types.ModuleType('apps.api.incident_legacy');module.__package__='apps.api'
        module.__file__=str(ROOT/source_path);sys.modules[module.__name__]=module
        exec(compile(source,module.__file__,'exec'),module.__dict__)
    else:
        source=(ROOT/source_path).read_bytes()
        if args.probe=='images':from apps.api import main as module
        else:from apps.api import jobs as module
    def snapshot():return {p.relative_to(data).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in data.rglob('*') if p.is_file()}
    before=snapshot()
    response_status=None;part_preserved=None
    if args.probe=='images':
        from fastapi.testclient import TestClient
        with TestClient(module.create_app(data),base_url='http://127.0.0.1') as client:
            token=client.get('/api/session').json()['csrf']
            client.headers.update({'X-LumaForge-Local':'1','X-Color-Studio-Token':token})
            # No UI consent, confirmation token, checklist or human acceptance.
            response_status=client.delete('/api/images').status_code
    else:
        import threading,time
        import numpy as np
        from unittest.mock import patch
        from packages.colour_core import engine
        jobs=module.Jobs(data/'jobs',threading.Lock());identifier=uuid.UUID(int=100)
        part=data/'jobs'/str(identifier)/'batch-001.png.part'
        sentinel=b'Preexisting private fixture; not created by the export writer'
        def encode(*args,**kwargs):part.write_bytes(sentinel);return b'Synthetic newly encoded bytes'
        with patch.object(module.uuid,'uuid4',return_value=identifier),patch.object(module.image_io,'decode',return_value=(np.zeros((24,32,3),dtype='float32'),None,[])),patch.object(module.image_io,'encode',side_effect=encode):
            jobs.start([str(uuid.UUID(int=1))],engine.Recipe(),'png',lambda value:data/'images'/f'{value}.png')
            workers=[t for t in threading.enumerate() if t.name=='color-studio-batch']
            for thread in workers:thread.join(5)
            if any(t.is_alive() for t in workers):raise RuntimeError('Owned batch did not finish')
        part_preserved=part.is_file() and part.read_bytes()==sentinel
        assert jobs.get(str(identifier))['status']=='completed_with_errors'
    after=snapshot()
    deleted=set(before)-set(after)
    if args.probe=='images':
        if args.mode=='legacy':assert response_status==200 and len(deleted)==6 and len(after)==3
        else:assert response_status==423 and before==after and not trace
    else:
        assert all(after.get(name)==digest for name,digest in before.items())
        assert part_preserved==(args.mode=='contained')
        assert len(trace)==(1 if args.mode=='legacy' else 0)
    result={'schema':'color-studio-contained-deletion-reproduction-v1','mode':args.mode,'probe':args.probe,
            'source_commit':LEGACY if args.mode=='legacy' else None,'code_path':source_path,'source_file_sha256':hashlib.sha256(source).hexdigest(),
            'synthetic_only':True,'initial_files':len(before),'remaining_original_files':sum(name in after for name in before),'deleted_images':len(deleted),
            'preexisting_part_preserved':part_preserved,'http_status':response_status,'explicit_deletion_consent_provided':False,'audit_remove_events':len(trace),
            'actor':'owned_reproduction_python_process','all_events_from_reproduction_pid':all(t['pid']==os.getpid() for t in trace),
            'private_trace_retained':True,'real_store_accessed':False,'historical_actor_identified':False,
            'process_monitor_executed':False,'external_beta':'NO-GO','commercial':'NO-GO'}
    (folder/'private-audit-trace.json').write_text(json.dumps({'events':trace,'before':before,'after':after},indent=2)+'\n',encoding='utf-8')
    (folder/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'result':result,'private_fixture':str(folder)}))


if __name__=='__main__':main()
