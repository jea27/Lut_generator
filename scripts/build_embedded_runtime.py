"""Build a private CPython bundle from hash-locked PSF/PyPI archives only.

Never searches for or copies DLLs from the host. No pip/site/bootstrap in the
embedded interpreter. Outputs are fresh, workspace-local directories. Native
origin/architecture/import closure is checked before an installer may consume it.
"""
import argparse
import base64
import csv
import hashlib
import importlib.metadata
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import urllib.parse
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[1]
LOCK=ROOT/'packaging/runtime.lock.json'
MANIFEST='runtime-manifest.json'
OS_DLLS=set('advapi32 bcrypt bcryptprimitives crypt32 gdi32 iphlpapi kernel32 ntdll ole32 oleaut32 pdh powrprof propsys psapi rpcrt4 shell32 user32 version winmm ws2_32 ucrtbase comctl32 combase dwmapi imm32 shlwapi msvcrt'.split())
API_SETS={'api-ms-win-core-path-l1-1-0.dll','api-ms-win-core-synch-l1-2-0.dll','api-ms-win-core-winrt-error-l1-1-0.dll'}
CRT_SETS={'api-ms-win-crt-'+name+'-l1-1-0.dll' for name in
          'conio convert environment filesystem heap locale math private process runtime stdio string time utility'.split()}


def digest(raw):return hashlib.sha256(raw).hexdigest()


def repository_bytes(source):
    raw=source.read_bytes()
    # Git autocrlf must not make a different runtime from the same source commit.
    return raw.replace(b'\r\n',b'\n') if source.suffix in ('.py','._pth','.json','.md','.txt') else raw


def authorized_demo(directory):
    credits=json.loads((directory/'credits.json').read_text(encoding='utf-8'))
    assets=credits['assets']
    if len(assets)!=2 or {a['role'] for a in assets}!={'source','reference'}:raise ValueError('Unexpected demo catalogue')
    allowed={'credits.json'}
    for asset in assets:
        name=asset['role']+'.jpg'
        if asset['file']!=name or asset['license']!='CC0-1.0' or not asset.get('author') or not asset.get('original_url','').startswith('https://dl.polyhaven.org/'):
            raise ValueError('Demo rights/provenance not allowlisted')
        if digest((directory/name).read_bytes())!=asset['sha256']:raise ValueError('Demo image hash mismatch')
        allowed.add(name)
    if {p.name for p in directory.iterdir()}!=allowed or any(p.is_symlink() for p in directory.iterdir()):raise ValueError('Unexpected/private demo asset')
    return allowed


def safe_member(name):
    path=PurePosixPath(name)
    if not name or '\\' in name or ':' in name or path.is_absolute() or '..' in path.parts or '\x00' in name:
        raise ValueError('Unsafe archive member')
    if any(p.endswith((' ','.')) or p.split('.')[0].upper() in {'CON','PRN','AUX','NUL',*(f'COM{i}' for i in range(1,10)),*(f'LPT{i}' for i in range(1,10))} for p in path.parts):
        raise ValueError('Unsafe Windows archive member')
    return path.as_posix()


def locked_download(item,cache,offline=False):
    filename=safe_member(item['filename'])
    if '/' in filename:raise ValueError('Download filename must be a basename')
    url=urllib.parse.urlparse(item['url'])
    if url.scheme!='https' or url.hostname not in ('www.python.org','files.pythonhosted.org') or url.username or url.password:
        raise ValueError('Untrusted runtime download origin')
    if not re.fullmatch('[a-f0-9]{64}',item['sha256']):raise ValueError('Invalid pinned SHA256')
    path=cache/filename
    if not path.exists():
        if offline:raise ValueError('Missing verified offline build input: '+filename)
        with urllib.request.urlopen(item['url'],timeout=90) as response:
            final=urllib.parse.urlparse(response.url)
            if final.scheme!='https' or final.hostname!=url.hostname:raise ValueError('Unexpected download redirect')
            raw=response.read(256*1024*1024+1)
        if len(raw)>256*1024*1024 or digest(raw)!=item['sha256']:raise ValueError('Runtime archive hash mismatch')
        path.write_bytes(raw)
    if path.is_symlink() or digest(path.read_bytes())!=item['sha256']:raise ValueError('Cached runtime archive hash mismatch')
    return path


def excluded(name,python=False):
    parts=PurePosixPath(name).parts
    if any(p.endswith('.dist-info') for p in parts):return None # Preserve notices/metadata, including third-party licenses.
    if 'ffmpeg' in name.lower():return 'video_codec_not_a_product_feature'
    if python and name=='python314._pth':return 'replaced_by_versioned_isolation_configuration'
    if {'tests','test','benchmarks','__pycache__'} & set(parts):return 'upstream_test_or_benchmark_not_runtime'
    if name.endswith(('.pyc','.pdb','.h','.hpp','.c','.cpp','.pyi')):return 'upstream_development_input_not_runtime'
    if name.endswith('.pyd') and any(x in PurePosixPath(name).name for x in ('_tests.','_test.')):return 'upstream_test_extension_not_runtime'
    return None


def wheel_records(archive):
    records=[n for n in archive.namelist() if n.endswith('.dist-info/RECORD')]
    if len(records)!=1:raise ValueError('Wheel must contain exactly one RECORD')
    rows={}
    for name,checksum,size in csv.reader(io.StringIO(archive.read(records[0]).decode('utf-8'))):
        name=safe_member(name)
        if name in rows:raise ValueError('Duplicate wheel RECORD entry')
        rows[name]=(checksum,size)
    return rows


def extract(archive_path,item,target,files,exclusions,python=False):
    with zipfile.ZipFile(archive_path) as archive:
        records=None if python else wheel_records(archive)
        for member in archive.infolist():
            name=safe_member(member.filename)
            if member.is_dir():continue
            if stat.S_ISLNK(member.external_attr>>16):raise ValueError('Archive symlink refused')
            if member.file_size>256*1024*1024:raise ValueError('Archive member too large')
            raw=archive.read(member)
            if records is not None:
                if name not in records:raise ValueError('Unrecorded wheel file')
                checksum,size=records[name]
                is_record=name.endswith('.dist-info/RECORD')
                expected='sha256='+base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).rstrip(b'=').decode()
                if not is_record and (checksum!=expected or size!=str(len(raw))):raise ValueError('Wheel RECORD hash/size mismatch')
            reason=excluded(name,python)
            if reason:
                exclusions.append({'archive':item['filename'],'member':name,'reason':reason});continue
            mapped=name if python else 'vendor/'+name
            if '.data/' in name:raise ValueError('Wheel data mapping requires explicit review')
            key=mapped.casefold()
            if any(p.casefold()==key for p in files):raise ValueError('Case-insensitive bundle collision')
            out=target.joinpath(*PurePosixPath(mapped).parts);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
            files[mapped]={'sha256':digest(raw),'bytes':len(raw),'origin':item['filename'],'member':name}


def native_inventory(target,files):
    import pefile # Build/audit tool only; never copied into the product.
    native=[]
    bundled={PurePosixPath(p).name.lower() for p in files if p.lower().endswith(('.dll','.pyd','.exe'))}
    for name in sorted(files):
        if not name.lower().endswith(('.dll','.pyd','.exe')):continue
        pe=pefile.PE(str(target/name),fast_load=True)
        try:
            if pe.FILE_HEADER.Machine!=0x8664:raise ValueError('Non-AMD64 native file: '+name)
            pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT']])
            imports=sorted({e.dll.decode('ascii').lower() for e in [*getattr(pe,'DIRECTORY_ENTRY_IMPORT',[]),*getattr(pe,'DIRECTORY_ENTRY_DELAY_IMPORT',[])]})
            unknown=[d for d in imports if d not in bundled and d not in API_SETS|CRT_SETS and d.removesuffix('.dll') not in OS_DLLS]
            if unknown:raise ValueError('Unresolved non-OS native dependency: '+name+' -> '+','.join(unknown))
            native.append({'file':name,**files[name],'architecture':'AMD64','imports':imports,
                           'windows_imports':[d for d in imports if d not in bundled]})
        finally:pe.close()
    if not native:raise ValueError('No native binaries audited')
    return native


def verify_bundle(target):
    report=json.loads((target/MANIFEST).read_text(encoding='utf-8'))
    expected=report['files']
    actual={p.relative_to(target).as_posix() for p in target.rglob('*') if p.is_file() and p!=target/MANIFEST}
    if actual!=set(expected):raise ValueError('Bundle contains missing or unexpected files')
    for name,record in expected.items():
        name=safe_member(name);path=target/name
        if path.is_symlink() or not path.resolve().is_relative_to(target.resolve()) or digest(path.read_bytes())!=record['sha256']:
            raise ValueError('Bundle file hash/containment mismatch')
    return report


def verify_sources(target,cache):
    """Reconcile manifest AND files against trusted lock/archives/checkout.

    Hashing a file against a manifest that could be edited together is not
    sufficient to establish origin. This is the builder's stronger gate.
    """
    report=verify_bundle(target)
    lock=json.loads(LOCK.read_text(encoding='utf-8'))
    inputs=[lock['python'],*lock['packages']]
    demos=authorized_demo(ROOT/'apps/demo')
    if report['lock_sha256']!=digest(repository_bytes(LOCK)) or report['inputs']!=inputs:
        raise ValueError('Runtime lock/manifest mismatch')
    archives={item['filename']:zipfile.ZipFile(locked_download(item,cache,True)) for item in inputs}
    try:
        for name,row in report['files'].items():
            member=safe_member(row['member'])
            if row['origin']=='repository':
                if member.startswith('apps/demo/') and member.removeprefix('apps/demo/') not in demos:raise ValueError('Untrusted demo asset')
                allowed=(member=='packaging/python314._pth' and name=='python314._pth') or (
                    name=='app/'+member and (member.startswith(('apps/api/','apps/desktop/','packages/colour_core/','packages/shot_planner/')) and member.endswith('.py') or member.startswith('apps/web/dist/') or member.startswith('apps/demo/') or member in ('apps/__init__.py','packages/__init__.py')))
                if not allowed or name.lower().endswith(('.dll','.pyd','.exe')):raise ValueError('Untrusted repository runtime file')
                source=ROOT/member
                if source.is_symlink() or not source.resolve().is_relative_to(ROOT.resolve()):raise ValueError('Repository source escapes checkout')
                raw=repository_bytes(source)
            else:
                if row['origin'] not in archives:raise ValueError('Untrusted runtime file origin')
                python=row['origin']==lock['python']['filename']
                if name!=(member if python else 'vendor/'+member) or excluded(member,python):raise ValueError('Incorrect archive mapping')
                raw=archives[row['origin']].read(member)
            if digest(raw)!=row['sha256']:raise ValueError('Runtime source reconciliation failed')
        if native_inventory(target,report['files'])!=report['native_files']:raise ValueError('Native audit differs from manifest')
    finally:
        for archive in archives.values():archive.close()
    return report


def dependency_inventory(target,lock,files):
    from packaging.requirements import Requirement
    from packaging.markers import default_environment
    from packaging.specifiers import SpecifierSet
    from packaging.utils import canonicalize_name
    expected={canonicalize_name(i['name']):i for i in lock['packages']}
    dists={canonicalize_name(d.metadata['Name']):d for d in importlib.metadata.distributions(path=[str(target/'vendor')])}
    if set(dists)!=set(expected):raise ValueError('Installed metadata differs from pinned dependency closure')
    env=default_environment();env.update(python_version='3.14',python_full_version='3.14.10',sys_platform='win32',platform_system='Windows',platform_machine='AMD64',os_name='nt',extra='')
    rows=[]
    for name,dist in sorted(dists.items()):
        if dist.version!=expected[name]['version']:raise ValueError('Pinned package version mismatch')
        if '3.14.10' not in SpecifierSet(dist.metadata.get('Requires-Python','')):raise ValueError('Unsupported Python version')
        for raw in dist.requires or []:
            req=Requirement(raw)
            if req.marker and not req.marker.evaluate(env):continue
            dep=canonicalize_name(req.name)
            if dep not in dists or dists[dep].version not in req.specifier:raise ValueError('Unresolved pinned package dependency')
        notices=[{'file':p,'sha256':r['sha256']} for p,r in files.items() if r['origin']==expected[name]['filename'] and re.search(r'(^|/)(license[^/]*|copying[^/]*|notice[^/]*)$',p,re.I)]
        if not notices:raise ValueError('Missing license notices: '+name)
        license=dist.metadata.get('License-Expression') or dist.metadata.get('License') or '; '.join(x for x in dist.metadata.get_all('Classifier',[]) if x.startswith('License ::'))
        if not license:raise ValueError('No declared package license: '+name)
        rows.append({'name':name,'version':dist.version,'declared_license':license,'notices':notices,
                     'qualification':'Package license plus all bundled third-party notices; not owner/commercial legal approval'})
    return rows


def build(target,cache,offline=False):
    private=(ROOT/'.lumaforge-local').resolve()
    if not target.resolve().is_relative_to(private) or target.resolve()==private:raise ValueError('Build target must be a private workspace subdirectory')
    if target.exists():raise ValueError('Refusing to overwrite an existing runtime')
    if not cache.resolve().is_relative_to(private):raise ValueError('Download cache must be inside the private workspace')
    lock=json.loads(LOCK.read_text(encoding='utf-8'))
    if lock.get('schema')!='color-studio-embedded-runtime-lock-v1' or lock['target']!='cp314-win_amd64':raise ValueError('Unknown runtime lock')
    cache.mkdir(parents=True,exist_ok=True)
    authorized_demo(ROOT/'apps/demo')
    inputs=[lock['python'],*lock['packages']]
    archives=[locked_download(item,cache,offline) for item in inputs]
    target.mkdir(parents=True);files={};exclusions=[]
    for item,archive in zip(inputs,archives):extract(archive,item,target,files,exclusions,item is lock['python'])
    def own(source,destination):
        raw=repository_bytes(source);out=target/destination;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
        files[destination]={'sha256':digest(raw),'bytes':len(raw),'origin':'repository','member':source.relative_to(ROOT).as_posix()}
    own(ROOT/'packaging/python314._pth','python314._pth')
    folders=['apps/api','apps/desktop','packages/colour_core','packages/shot_planner']
    for folder in folders:
        for p in sorted((ROOT/folder).glob('*.py')):own(p,'app/'+p.relative_to(ROOT).as_posix())
    for name in ('apps/__init__.py','packages/__init__.py'):
        if (ROOT/name).is_file():own(ROOT/name,'app/'+name)
    if not (ROOT/'apps/web/dist/index.html').is_file():raise ValueError('Compile the frontend before bundling')
    for folder in ('apps/web/dist','apps/demo'):
        for p in sorted((ROOT/folder).rglob('*')):
            if p.is_file():
                if p.is_symlink() or p.suffix in ('.map','.log','.tmp','.exe','.dll','.pyd') or '.git' in p.parts:raise ValueError('Unreviewed app asset')
                own(p,'app/'+p.relative_to(ROOT).as_posix())
    native=native_inventory(target,files)
    packages=dependency_inventory(target,lock,files)
    source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    dirty=bool(subprocess.check_output(['git','status','--porcelain','--untracked-files=normal'],cwd=ROOT,text=True).strip())
    report={'schema':'color-studio-runtime-manifest-v1','python_version':lock['python']['version'],
            'python_distribution':'official-PSF-embeddable','target':lock['target'],'source':source,'dirty':dirty,
            'lock_sha256':digest(repository_bytes(LOCK)),'inputs':inputs,'files':dict(sorted(files.items())),
            'native_files':native,'excluded':exclusions,'build_origin_gate_passed':True,
            'packages':packages,'python_notices':{'file':'LICENSE.txt','sha256':files['LICENSE.txt']['sha256']},
            'copy_host_dlls':False,'windows_baseline':'Windows10/11 x64; system UCRT/API sets are OS prerequisites, not redistributed',
            'redistribution_approved':False,'external_distribution':'NO-GO until owner/legal/clean-Windows gates',
            'isolation':{'site':False,'user_site':False,'pythonpath':False,'registry_install':False}}
    (target/MANIFEST).write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
    verify_sources(target,cache)
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('target',type=Path);p.add_argument('--offline',action='store_true');p.add_argument('--verify',action='store_true')
    args=p.parse_args();target=args.target.resolve()
    r=verify_sources(target,ROOT/'.lumaforge-local/downloads') if args.verify else build(target,ROOT/'.lumaforge-local/downloads',args.offline)
    print(json.dumps({'files':len(r['files']),'native':len(r['native_files']),'build_origin_gate_passed':r['build_origin_gate_passed'],'redistribution_approved':False}))


if __name__=='__main__':main()
