"""Audit trusted embedded payload, including 3.14 bytecode with its own Python.

The public result never contains matched strings or private absolute paths.
Vendor build/example paths are classified separately from the user's profile.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
if __package__:
    from .build_embedded_runtime import ROOT,verify_sources,digest,native_inventory
else:
    from build_embedded_runtime import ROOT,verify_sources,digest,native_inventory

SCANNER=r'''
import json,sys,re,zipfile,marshal,types
from pathlib import Path
data=json.load(sys.stdin);root=Path(data['root']);findings=set()
profile=data['profile'].lower()
secret=re.compile(rb'github_pat_[A-Za-z0-9_]{35,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
userpath=re.compile(r'(?i)[a-z]:[\\/]Users[\\/]([^\\/\x00\r\n<>"\s]{1,80})[\\/]')
drive=re.compile(r'(?i)(?<![a-z0-9+._-])[a-z]:[\\/]')
generic={'user','username','runner','runneradmin','vssadministrator','administrator','test','default','public'}
def scan(label,raw,own):
 if secret.search(raw):findings.add((label,'secret_pattern',True))
 for encoding in ('utf-8','utf-16le'):
  value=raw.decode(encoding,errors='ignore')
  if profile and profile in value.lower():
   # GitHub runner usernames can coincide with a published vendor build path.
   # Only hash-verified upstream bytes get this classification; own code does not.
   account=userpath.match(profile.rstrip('\\/')+'\\')
   public_ci=not own and account is not None and account.group(1).lower() in generic
   findings.add((label,'published_upstream_ci_prefix' if public_ci else 'local_private_profile_path',not public_ci))
  for match in userpath.finditer(value):
   known=match.group(1).lower() in generic and not own
   findings.add((label,'generic_upstream_example_account' if known else 'user_path_requires_review',not known))
  # Drive prefixes in compressed image/font bytes are not filesystem evidence.
  # Specific profile/secret checks above still apply to every byte container.
  if Path(label).suffix in ('.py','.pyc','.js','.json','.html','.css','.txt','.md') and drive.search(value):
   findings.add((label,'repository_windows_path' if own else 'upstream_windows_build_or_example_path',own))
def code(label,value,own):
 if isinstance(value,types.CodeType):
  scan(label,value.co_filename.encode(),own)
  for child in value.co_consts:code(label,child,own)
 elif isinstance(value,str):scan(label,value.encode(),own)
 elif isinstance(value,bytes):scan(label,value,own)
for name,row in data['files'].items():
 path=root/name;raw=path.read_bytes();own=row['origin'].startswith('repository')
 scan(name,raw,own)
 if name.endswith('.py'):
  code(name,compile(raw,name,'exec'),own)
 if name=='python314.zip':
  with zipfile.ZipFile(path) as archive:
   for member in archive.namelist():
    if member.endswith('.pyc'):code('stdlib/'+member,marshal.loads(archive.read(member)[16:]),False)
rows=[{'file':label,'reason':reason,'blocking':blocked} for label,reason,blocked in sorted(findings)]
print(json.dumps({'findings':rows,'blocking_findings':sum(r['blocking'] for r in rows),'passed':not any(r['blocking'] for r in rows)}))
'''


def scan_files(interpreter,root,files):
    keep={'SYSTEMROOT','WINDIR','LOCALAPPDATA','APPDATA','USERPROFILE','TEMP','TMP','COMSPEC'}
    env={k:v for k,v in os.environ.items() if k.upper() in keep}
    env['PATH']=str(Path(os.environ['SYSTEMROOT'])/'System32')
    with tempfile.TemporaryDirectory(prefix='payload-audit-',dir=ROOT/'.lumaforge-local') as cwd:
        result=subprocess.run([str(interpreter),'-I','-S','-B','-c',SCANNER],
            input=json.dumps({'root':str(root),'profile':os.environ.get('USERPROFILE',''),'files':files}),
            cwd=cwd,env=env,capture_output=True,text=True,timeout=120)
    if result.returncode:
        (ROOT/'.lumaforge-local/payload-audit-error.log').write_text(result.stderr,encoding='utf-8')
        raise ValueError('Embedded bytecode/source audit failed; inspect private log')
    return json.loads(result.stdout)


def audit(target,native=None):
    manifest=verify_sources(target,ROOT/'.lumaforge-local/downloads')
    report=scan_files(target/'python.exe',target,manifest['files'])
    if native:
        files={native.name:{'sha256':digest(native.read_bytes()),'bytes':native.stat().st_size,'origin':'repository-compiled-locked-cargo'}}
        rows=native_inventory(native.parent,files)
        native_report=scan_files(target/'python.exe',native.parent,files)
        report['native_launcher']={'inventory':rows,'privacy':native_report,'signature':'Not signed; no certificate purchased'}
        report['passed']=report['passed'] and native_report['passed']
        report['blocking_findings']+=native_report['blocking_findings']
    from PIL import Image
    photos=[]
    for p in sorted((target/'app/apps/demo').glob('*.jpg')):
        with Image.open(p) as image:
            if image.getexif():raise ValueError('Demo photo contains EXIF')
        photos.append({'file':p.name,'sha256':digest(p.read_bytes()),'exif_entries':0})
    report.update(schema='color-studio-embedded-payload-audit-v1',files=len(manifest['files']),
                  native=len(manifest['native_files']),manifest_sha256=digest((target/'runtime-manifest.json').read_bytes()),
                  demo=photos,scope='Pinned runtime + source + native bytes + stdlib bytecode. Pattern audit, not proof of absence of all private data.',
                  build_origin_gate_passed=True,redistribution_approved=False)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('runtime',type=Path);parser.add_argument('report',type=Path);parser.add_argument('--native',type=Path);args=parser.parse_args()
    result=audit(args.runtime.resolve(),args.native.resolve() if args.native else None);args.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('files','native','blocking_findings','passed')}))
    raise SystemExit(0 if result['passed'] else 2)
