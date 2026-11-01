"""Inspect an NSIS candidate without installing it or executing extracted plugins.

7-Zip must already be authorized/available. Extraction is fresh and workspace-local;
the public report contains relative names/hashes only. Clean Windows is a separate gate.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import uuid
import zipfile
if __package__:
    from .build_embedded_runtime import ROOT, MANIFEST, digest, safe_member, verify_sources, OS_DLLS, API_SETS, CRT_SETS
    from .audit_embedded_payload import scan_files
else:
    from build_embedded_runtime import ROOT, MANIFEST, digest, safe_member, verify_sources, OS_DLLS, API_SETS, CRT_SETS
    from audit_embedded_payload import scan_files


def listing(text):
    if 'Type = Nsis' not in text or '\n----------\n' not in text:
        raise ValueError('Expected complete NSIS listing')
    rows={};seen=set();total=0
    for block in text.split('\n----------\n',1)[1].strip().split('\n\n'):
        row=dict(line.split(' = ',1) for line in block.splitlines() if ' = ' in line)
        if not row:continue
        name=safe_member(row['Path'].replace('\\','/'))
        if name.casefold() in seen or any('link' in key.lower() for key in row):
            raise ValueError('Collision or link in installer')
        if any(c not in ' A' for c in row.get('Attributes','')):raise ValueError('Unexpected archive attributes')
        if not row.get('Size') and name!='uninstall.exe':raise ValueError('Missing archive size')
        size=int(row['Size']) if row.get('Size') else 0
        if size<0:raise ValueError('Invalid archive size')
        total+=size;seen.add(name.casefold());rows[name]=size
    if not rows or len(rows)>5000 or total>1024**3:raise ValueError('Installer extraction bounds exceeded')
    return rows


def expected_files(runtime,notices,plugins):
    names={'runtime/'+n for n in runtime['files']}|{'runtime/'+MANIFEST,'color-studio-beta.exe','uninstall.exe'}|set(plugins)
    names|={'notices/'+p.relative_to(notices).as_posix() for p in notices.rglob('*') if p.is_file()}
    return names


def pe_summary(path,machine):
    import pefile
    pe=pefile.PE(str(path),fast_load=False)
    try:
        if pe.FILE_HEADER.Machine!=machine:raise ValueError('Wrong installer component architecture')
        imports={entry.dll.decode('ascii').lower() for key in ('DIRECTORY_ENTRY_IMPORT','DIRECTORY_ENTRY_DELAY_IMPORT') for entry in getattr(pe,key,[])}
        # Common-dialog and legacy Winsock are Windows system dependencies used
        # by the hash-verified NSIS plugins, never copied into the application.
        unknown={name for name in imports if name.removesuffix('.dll') not in OS_DLLS|{'comdlg32','wsock32'} and name not in API_SETS|CRT_SETS}
        if unknown:raise ValueError('Unknown native installer dependencies: '+','.join(sorted(unknown)))
        return {'machine':hex(machine),'imports':sorted(imports),'sha256':digest(path.read_bytes())}
    finally:pe.close()


def launcher_match(built,installed):
    # Tauri2.12.4 restores the build exe's UNK marker after bundling. Only the
    # documented NSS bundle marker may differ; never normalize executable code.
    marker=b'__TAURI_BUNDLE_TYPE_VAR_'
    if built==installed:return 'identical'
    if built.count(marker+b'UNK')==1 and built.replace(marker+b'UNK',marker+b'NSS')==installed:
        return 'only_Tauri_UNK_to_NSS_bundle_marker'
    raise ValueError('Native launcher hash mismatch outside documented bundle marker')


def audit(installer,seven_zip,native,nsis_zip,nsis_cache):
    lock=json.loads((ROOT/'packaging/nsis-toolchain.lock.json').read_text(encoding='utf-8'))
    if digest(nsis_zip.read_bytes())!=lock['nsis']['sha256']:raise ValueError('Official NSIS archive hash mismatch')
    # Reconcile every embedded plugin/graphic against independently fetched official bytes.
    with zipfile.ZipFile(nsis_zip) as archive:
        for name,row in lock['files'].items():
            if row['source']=='nsis' and digest(archive.read(row['member']))!=row['sha256']:
                raise ValueError('Official NSIS member hash mismatch')
        for member in ('Stubs/lzma_solid-x86-unicode','Bin/makensis.exe','COPYING'):
            if (nsis_cache/member).read_bytes()!=archive.read('nsis-3.13/'+member):
                raise ValueError('NSIS compiler/stub/license differs from official archive')
    result=subprocess.run([str(seven_zip),'l','-slt',str(installer)],capture_output=True,text=True,encoding='utf-8',check=True)
    rows=listing(result.stdout.replace('\r\n','\n'))
    private=ROOT/'.lumaforge-local'/('nsis-audit-'+uuid.uuid4().hex);private.mkdir()
    subprocess.run([str(seven_zip),'x','-y','-o'+str(private),str(installer)],stdout=subprocess.DEVNULL,check=True)
    if any(p.is_symlink() or not p.resolve().is_relative_to(private.resolve()) for p in private.rglob('*')):
        raise ValueError('Extraction escaped audited directory')
    actual={p.relative_to(private).as_posix() for p in private.rglob('*') if p.is_file()}
    if actual!=set(rows):raise ValueError('Listing/extraction mismatch')
    runtime=verify_sources(private/'runtime',ROOT/'.lumaforge-local/downloads')
    notices=ROOT/'packaging/notices'
    if actual!=expected_files(runtime,notices,lock['files']):raise ValueError('Unexpected or missing installer files')
    launcher=launcher_match(native.read_bytes(),(private/'color-studio-beta.exe').read_bytes())
    for path in notices.rglob('*'):
        if path.is_file() and (private/'notices'/path.relative_to(notices)).read_bytes()!=path.read_bytes():
            raise ValueError('Notice changed inside setup')
    plugins=[]
    for name,row in lock['files'].items():
        if digest((private/name).read_bytes())!=row['sha256']:raise ValueError('Installer plugin/resource hash mismatch')
        plugins.append({'file':name,**row,**(pe_summary(private/name,0x14c) if name.endswith('.dll') else {})})
    native_components={'installer':pe_summary(installer,0x14c),'uninstaller':pe_summary(private/'uninstall.exe',0x14c),
                       'launcher':pe_summary(private/'color-studio-beta.exe',0x8664)}
    extra={n:{'origin':'repository-compiled' if n in ('color-studio-beta.exe','uninstall.exe') else 'verified-upstream'} for n in actual if not n.startswith('runtime/')}
    privacy=scan_files(private/'runtime/python.exe',private,extra)
    if not privacy['passed']:raise ValueError('Installer non-runtime privacy gate failed')
    return {'schema':'color-studio-nsis-audit-v1','installer_sha256':digest(installer.read_bytes()),'installer_bytes':installer.stat().st_size,
            'source':runtime['source'],'dirty':runtime['dirty'],'files':len(actual),'runtime_files':len(runtime['files']),
            'runtime_manifest_sha256':digest((private/'runtime'/MANIFEST).read_bytes()),'plugins_and_graphics':plugins,
            'nsis_source':lock['nsis'],'native_components':native_components,'all_payload_bytes_match_verified_inputs':True,
            'launcher_comparison':launcher,'build_launcher_sha256':digest(native.read_bytes()),
            'notices_match_repository':True,'privacy':privacy,'webview2_runtime_or_bootstrapper_embedded':False,
            'clean_windows_tested':False,'redistribution_approved':False,'external_beta':'NO-GO',
            'scope':'NSIS full extraction, exact file set/hashes and native import audit; not installation or legal approval'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('installer','report','seven_zip','native','nsis_zip','nsis_cache'):parser.add_argument(name,type=Path)
    args=parser.parse_args()
    result=audit(*(getattr(args,n).resolve() for n in ('installer','seven_zip','native','nsis_zip','nsis_cache')))
    args.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('installer_sha256','files','runtime_files','all_payload_bytes_match_verified_inputs','external_beta')}))
