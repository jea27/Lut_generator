"""Assemble a private, hash-verifiable QA handoff; never install or start a VM."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(artifact, output, previous=None):
    private=ROOT/'.lumaforge-local'
    output=output.absolute()
    if private.resolve()!=private.absolute() or output.resolve()!=output or not output.is_relative_to(private) or output==private:
        raise ValueError('QA output must be an unlinked private workspace child')
    if output.exists() or output.with_suffix('.zip').exists():raise ValueError('Preserve existing kits; choose a new output')
    if subprocess.check_output(['git','status','--porcelain','--untracked-files=normal'],cwd=ROOT):
        raise ValueError('Commit QA tools and documents before creating a reproducible handoff')
    record=json.loads(artifact.read_bytes())
    if (record.get('dirty') is not False or not record.get('build_origin_gate_passed') or not record.get('payload_audit_passed')
            or record.get('nsis_full_audit')!='passed' or not re.fullmatch('[a-f0-9]{40}',record.get('source',''))):
        raise ValueError('Only a clean, audited internal installer may enter the kit')
    name=record['file']
    if Path(name).name!=name or not name.endswith('_x64-setup.exe'):raise ValueError('Invalid installer filename')
    installer=ROOT/'apps/desktop/src-tauri/target/release/bundle/nsis'/name
    if installer.is_symlink() or sha(installer)!=record['sha256']:raise ValueError('Installer hash mismatch')
    subprocess.run(['git','cat-file','-e',record['source']+'^{commit}'],cwd=ROOT,check=True,capture_output=True)
    output.mkdir(parents=True)
    shutil.copyfile(installer,output/'candidate.exe')
    for source,destination in [
        ('scripts/qa_guest_checks.ps1','qa_guest_checks.ps1'),
        ('scripts/qa_vm_cycle.ps1','qa_vm_cycle.ps1'),
        ('scripts/qa_vm_assistant.ps1','scripts/qa_vm_assistant.ps1'),
        ('scripts/qa_guest_api.py','scripts/qa_guest_api.py'),
        ('scripts/qa_windows_preservation.ps1','qa_windows_preservation.ps1'),
        ('scripts/qa_windows_clean.ps1','qa_windows_clean.ps1'),
        ('scripts/reproduce_private_deletion.py','scripts/reproduce_private_deletion.py'),
        ('tests_mvp/test_installer_transaction.py','tests_mvp/test_installer_transaction.py'),
        ('docs/QA_WINDOWS11_VM.md','QA_WINDOWS11_VM.md'),
        ('docs/QA_RESOLVE_BETA3.md','QA_RESOLVE_BETA3.md'),
        ('docs/QA_EDITORES_03.md','QA_EDITORES_03.md'),
        ('docs/evidence/INCIDENT_036_TOOL_PREP.json','INCIDENT_036_TOOL_PREP.json'),
        ('docs/QA_BETA5_INTERNA.md','QA_BETA5_INTERNA.md'),
        ('docs/PRUEBA_CREATOR_PRO_PLANNER.md','PRUEBA_CREATOR_PRO_PLANNER.md'),
        ('docs/QA_VM_ASISTIDA.md','LEEME.md')]:
        path=ROOT/source
        if path.is_symlink() or not path.resolve().is_relative_to(ROOT):raise ValueError('Linked QA source')
        target=output/destination;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
    import numpy as np
    from packages.colour_core import engine,image_io
    inputs=output/'inputs';inputs.mkdir()
    y=np.linspace(0,1,768,dtype='float32')[:,None,None]
    x=np.linspace(0,1,1024,dtype='float32')[None,:,None]
    source=np.broadcast_to(.65*x+.35*y,(768,1024,3)).copy()
    reference=np.clip(source*np.array([1.1,.9,.75],dtype='float32')+.03,0,1)
    (inputs/'source.png').write_bytes(image_io.encode(source))
    (inputs/'reference.png').write_bytes(image_io.encode(reference))
    (inputs/'identity.recipe.json').write_text(json.dumps(engine.Recipe().model_dump(),indent=2)+'\n',encoding='utf-8')
    from scripts.reproduce_private_deletion import LEGACY,LEGACY_SHA256,legacy_source
    legacy=output/'qa/legacy';legacy.mkdir(parents=True)
    for name in LEGACY_SHA256:(legacy/Path(name).name).write_bytes(legacy_source(name))
    prior=None
    if previous:
        prior=json.loads((ROOT/'docs/evidence/RUNTIME_036_ARTIFACT.json').read_bytes())
        if previous.is_symlink() or sha(previous)!=prior['sha256']:raise ValueError('Previous installer is not the pinned beta3')
        shutil.copyfile(previous,output/'previous.exe')
    files={p.relative_to(output).as_posix():sha(p) for p in output.rglob('*') if p.is_file()}
    audit=json.loads((private/'beta-nsis-audit.json').read_bytes())
    if audit['installer_sha256']!=record['sha256']:raise ValueError('NSIS audit is not bound to this candidate')
    manifest={'schema':'color-studio-private-vm-kit-v2','version':record['version'],'source':record['source'],
        'installer_sha256':record['sha256'],'previous_installer_sha256':prior['sha256'] if prior else None,
        'runtime_manifest_sha256':record['runtime_manifest_sha256'],
        'installer_manifest_sha256':record['installer_manifest_sha256'],
        'previous_version':prior['version'] if prior else None,
        'previous_runtime_manifest_sha256':prior['runtime_manifest_sha256'] if prior else None,
        'previous_installer_manifest_sha256':prior['installer_manifest_sha256'] if prior else None,
        'candidate_uninstaller_sha256':audit['native_components']['uninstaller']['sha256'],
        'tool_source':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'tool_dirty':False,
        'legacy_source_commit':LEGACY,'legacy_source_sha256':LEGACY_SHA256,
        'files':files,'clean_windows_verified':False,'native_capture_verified':False,'human_accepted':False,
        'external_beta':'NO-GO','commercial':'NO-GO','scope':'Private synthetic QA handoff; no historical incident evidence or personal media'}
    (output/'kit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    archive=output.with_suffix('.zip')
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(output.rglob('*')):
            if path.is_file():bundle.write(path,path.relative_to(output).as_posix())
    return {'version':record['version'],'source':record['source'],'installer_sha256':record['sha256'],
        'kit_zip_sha256':sha(archive),'kit_zip_bytes':archive.stat().st_size,'kit_manifest_sha256':sha(output/'kit-manifest.json'),
        'files':len(files),'previous_installer_included':bool(previous),'clean_windows_verified':False,
        'native_capture_verified':False,'external_beta':'NO-GO','commercial':'NO-GO'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifact',type=Path,default=ROOT/'.lumaforge-local/beta-artifact.json')
    parser.add_argument('--output',type=Path,default=ROOT/'.lumaforge-local'/('vm-qa-kit-'+uuid.uuid4().hex))
    parser.add_argument('--previous',type=Path)
    args=parser.parse_args();print(json.dumps(prepare(args.artifact,args.output,args.previous)))
