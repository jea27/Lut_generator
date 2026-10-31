"""Read-only payload audit. No secret values or private source paths in report."""
import argparse,hashlib,json,marshal,os,re,types
from pathlib import Path
from PyInstaller.archive.readers import CArchiveReader


def audit(directory):
    root=Path(directory);files=[];findings=[]
    profile=os.environ.get('USERPROFILE','').encode()
    patterns=[('upstream_or_example_user_path',re.compile(rb'(?i)[A-Z]:[\\/]Users[\\/][^\\/\x00\r\n]{1,80}[\\/]')),
              ('secret_pattern',re.compile(rb'github_pat_[A-Za-z0-9_]{35,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'))]
    def inspect(label,data):
        if profile and (profile.lower() in data.lower() or profile.decode().encode('utf-16le').lower() in data.lower()):
            findings.append({'file':label,'reason':'local_private_profile_path'})
        for reason,pattern in patterns:
            if pattern.search(data):findings.append({'file':label,'reason':reason})
    for path in sorted(root.rglob('*')):
        if not path.is_file():continue
        relative=path.relative_to(root).as_posix();digest=hashlib.sha256()
        if any(part in ('.git','.venv-mvp','node_modules','tests','tests_mvp','.research-private') for part in path.relative_to(root).parts) or path.suffix in ('.pdb','.map','.log'):
            findings.append({'file':relative,'reason':'development_or_private_file'})
        with path.open('rb') as stream:
            tail=b''
            while chunk:=stream.read(4*1024*1024):
                digest.update(chunk);inspect(relative,tail+chunk);tail=chunk[-1024:]
        files.append({'file':relative,'bytes':path.stat().st_size,'sha256':digest.hexdigest()})
    archive=CArchiveReader(str(root/'ColorEngine.exe'))
    def code(label,obj):
        if isinstance(obj,types.CodeType):
            inspect(label,obj.co_filename.encode())
            for value in obj.co_consts:
                if isinstance(value,types.CodeType):code(label,value)
                elif isinstance(value,str):inspect(label,value.encode())
                elif isinstance(value,bytes):inspect(label,value)
    for name,entry in archive.toc.items():
        if entry[-1]=='s':code('archive/'+name,marshal.loads(archive.extract(name)))
    pyz=archive.open_embedded_archive('PYZ.pyz')
    for name in pyz.toc:code('PYZ/'+name,pyz.extract(name))
    unique=[dict(t) for t in {tuple(sorted(f.items())) for f in findings}]
    return {'scope':'Uncompressed staging tree + Python archive code/constants. NSIS runtime/plugin inputs require separate reconciliation; pattern scan is not proof of absence of every secret.',
            'files':files,'findings':unique,'passed':not unique}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory');parser.add_argument('report');args=parser.parse_args()
    report=audit(args.directory);Path(args.report).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'files':len(report['files']),'findings':len(report['findings']),'passed':report['passed']}))
    raise SystemExit(0 if report['passed'] else 2)
