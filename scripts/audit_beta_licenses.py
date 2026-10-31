"""Inventory installed, locked beta inputs; no legal clearance is inferred.

Run using .venv-mvp Python after npm ci and cargo fetch. Captures notices from
local official packages only. Paths in the public report are package-relative.
Cargo includes build dependencies, conservatively; a binary SBOM is still due.
"""
import hashlib
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'packaging/notices'


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    rows=[];notices=[]
    def add(ecosystem,name,version,license,files):
        texts=[]
        for label,path in files:
            if path.is_file():
                raw=path.read_bytes();text=raw.decode('utf-8',errors='replace')
                texts.append({'file':label,'sha256':hashlib.sha256(raw).hexdigest()})
                notices.append(f'\n\n===== {ecosystem}: {name} {version} / {label} =====\n{text}')
        rows.append({'ecosystem':ecosystem,'name':name,'version':version,'declared_license':license,
                     'notices':texts,'review':'manual_review_required' if not texts or not license else 'notice_captured_not_legal_approval'})
    names=[]
    for req in ('requirements-mvp.txt','requirements-build.txt'):
        names.extend(line.split('==')[0] for line in (ROOT/req).read_text().splitlines() if '==' in line)
    for name in sorted(set(names)):
        dist=metadata.distribution(name);files=[]
        for file in dist.files or []:
            if re.search(r'(^|[/\\])(LICENSE[^/\\]*|COPYING[^/\\]*|NOTICE[^/\\]*)$',str(file),re.I):
                files.append((str(file).replace('\\','/'),Path(dist.locate_file(file))))
        declared=dist.metadata.get('License-Expression') or dist.metadata.get('License') or '; '.join(
            x for x in dist.metadata.get_all('Classifier',[]) if x.startswith('License ::'))
        add('python',name,dist.version,declared,files)
    # Compiler/runtime libraries used in the frontend; no dev bundler is shipped.
    lock=json.loads((ROOT/'apps/web/package-lock.json').read_bytes())
    for location,value in sorted(lock['packages'].items()):
        if not location or value.get('dev'):continue
        path=ROOT/'apps/web'/location
        files=[(p.name,p) for p in path.iterdir() if p.is_file() and re.match(r'^(LICENSE|COPYING|NOTICE)',p.name,re.I)]
        if location.endswith('@quasar/extras'):
            files.append(('exports/material-icons/LICENSE',path/'exports/material-icons/LICENSE'))
        add('npm',location.removeprefix('node_modules/'),value['version'],value.get('license',''),files)
    cargo=Path(os.environ['USERPROFILE'])/'.cargo/bin/cargo.exe'
    result=subprocess.run([str(cargo),'metadata','--locked','--format-version','1','--filter-platform','x86_64-pc-windows-msvc'],
                          cwd=ROOT/'apps/desktop/src-tauri',check=True,capture_output=True)
    for pkg in sorted(json.loads(result.stdout)['packages'],key=lambda p:(p['name'],p['version'])):
        if not pkg['source']:continue # Own code is not assigned a license by this audit.
        directory=Path(pkg['manifest_path']).parent
        files=[(p.name,p) for p in directory.iterdir() if p.is_file() and re.match(r'^(LICENSE|COPYING|NOTICE)',p.name,re.I)]
        if pkg.get('license_file'):
            p=directory/pkg['license_file']
            if p not in [x[1] for x in files]:files.append((pkg['license_file'],p))
        upstream=OUT/'upstream'/(pkg['name']+'.txt')
        if not files and upstream.is_file():
            sources=json.loads((OUT/'upstream/sources.json').read_bytes())
            source=next(x for x in sources if x['package']==pkg['name'])
            if hashlib.sha256(upstream.read_bytes()).hexdigest()!=source['sha256']:raise ValueError('Upstream notice hash mismatch')
            files.append(('pinned-upstream-license',upstream))
        add('cargo-resolved-including-build',pkg['name'],pkg['version'],pkg.get('license',''),files)
    python_license=Path(sys.base_prefix)/'LICENSE.txt'
    add('runtime','CPython',sys.version.split()[0],'PSF-2.0 and bundled third-party notices',[('LICENSE.txt',python_license)])
    report={'scope':'Conservative locked input inventory, not a complete binary SBOM or legal approval',
            'excluded_binary':'opencv_videoio_ffmpeg: filtered from PyInstaller binaries; verify output tree',
            'manual_gates':['Microsoft WebView2/VC runtime redistribution terms','Binary-to-source reconciliation and third-party code inside wheels',
                            'PyInstaller bootloader exception','License selection for own public source','Trademark and commercial terms'],
            'packages':rows}
    (OUT/'inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'THIRD_PARTY_NOTICES.txt').write_text('Third-party notices · Color Studio technical beta\nNot a license grant for project code.\n'+''.join(notices),encoding='utf-8')
    print(json.dumps({'packages':len(rows),'without_notices':sum(not r['notices'] for r in rows),'notice_bytes':(OUT/'THIRD_PARTY_NOTICES.txt').stat().st_size}))


if __name__=='__main__':main()
