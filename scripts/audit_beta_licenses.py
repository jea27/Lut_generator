"""Inventory installed, locked beta inputs; no legal clearance is inferred.

Run using .venv-mvp Python after npm ci and cargo fetch. Captures notices from
local official packages only. Paths in the public report are package-relative.
Cargo includes build dependencies, conservatively; a binary SBOM is still due.
"""
import argparse
import hashlib
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'packaging/notices'


def main(runtime=None):
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
        return rows[-1]
    names=[]
    for req in ('requirements-mvp.txt','requirements-build.txt'):
        names.extend(line.split('==')[0] for line in (ROOT/req).read_text().splitlines() if '==' in line)
    for name in ([] if runtime else sorted(set(names))):
        dist=metadata.distribution(name);files=[]
        for file in dist.files or []:
            if re.search(r'(^|[/\\])(LICENSE[^/\\]*|COPYING[^/\\]*|NOTICE[^/\\]*)$',str(file),re.I):
                files.append((str(file).replace('\\','/'),Path(dist.locate_file(file))))
        declared=dist.metadata.get('License-Expression') or dist.metadata.get('License') or '; '.join(
            x for x in dist.metadata.get_all('Classifier',[]) if x.startswith('License ::'))
        add('python',name,dist.version,declared,files)
    if runtime:
        from build_embedded_runtime import verify_sources
        manifest=verify_sources(runtime,ROOT/'.lumaforge-local/downloads')
        for package in manifest['packages']:
            row=add('python-embedded-runtime',package['name'],package['version'],package['declared_license'],
                [(r['file'],runtime/r['file']) for r in package['notices']])
            source=next(i for i in manifest['inputs'] if i.get('name')==package['name'])
            row.update(source_url=source['url'],archive_sha256=source['sha256'])
    # Compiler/runtime libraries used in the frontend; no dev bundler is shipped.
    lock=json.loads((ROOT/'apps/web/package-lock.json').read_bytes())
    for location,value in sorted(lock['packages'].items()):
        if not location or value.get('dev'):continue
        path=ROOT/'apps/web'/location
        files=[(p.name,p) for p in path.iterdir() if p.is_file() and re.match(r'^(LICENSE|COPYING|NOTICE)',p.name,re.I)]
        if location.endswith('@quasar/extras'):
            files.append(('exports/material-icons/LICENSE',path/'exports/material-icons/LICENSE'))
        row=add('npm',location.removeprefix('node_modules/'),value['version'],value.get('license',''),files)
        row.update(source_url=value.get('resolved'),archive_integrity=value.get('integrity'))
    cargo=Path(os.environ['USERPROFILE'])/'.cargo/bin/cargo.exe'
    cargo_lock=tomllib.loads((ROOT/'apps/desktop/src-tauri/Cargo.lock').read_text(encoding='utf-8'))
    cargo_inputs={(p['name'],p['version']):p for p in cargo_lock['package']}
    result=subprocess.run([str(cargo),'metadata','--locked','--offline','--format-version','1','--filter-platform','x86_64-pc-windows-msvc'],
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
        row=add('cargo-resolved-including-build',pkg['name'],pkg['version'],pkg.get('license',''),files)
        row.update(source_registry=pkg['source'],crate_archive_sha256=cargo_inputs[(pkg['name'],pkg['version'])].get('checksum'))
    python_license=runtime/'LICENSE.txt' if runtime else Path(sys.base_prefix)/'LICENSE.txt'
    row=add('runtime','CPython',manifest['python_version'] if runtime else sys.version.split()[0],'PSF-2.0 and bundled third-party notices',[('LICENSE.txt',python_license)])
    if runtime:row.update(source_url=manifest['inputs'][0]['url'],archive_sha256=manifest['inputs'][0]['sha256'])
    report={'scope':'Conservative locked input inventory, not a complete binary SBOM or legal approval',
            'excluded_binary':'opencv_videoio_ffmpeg: excluded from embedded runtime' if runtime else 'opencv_videoio_ffmpeg: filtered from PyInstaller binaries; verify output tree',
            'manual_gates':['Microsoft WebView2/VC runtime redistribution terms','Binary-to-source reconciliation and third-party code inside wheels',
                            *([] if runtime else ['PyInstaller bootloader exception']),'License selection for own public source','Trademark and commercial terms'],
            'runtime_distribution':'PSF official embeddable; host/build packages not shipped' if runtime else 'legacy PyInstaller',
            'packages':rows}
    (OUT/'inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/'THIRD_PARTY_NOTICES.txt').write_text('Third-party notices · Color Studio technical beta\nNot a license grant for project code.\n'+''.join(notices),encoding='utf-8')
    print(json.dumps({'packages':len(rows),'without_notices':sum(not r['notices'] for r in rows),'notice_bytes':(OUT/'THIRD_PARTY_NOTICES.txt').stat().st_size}))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--runtime',type=Path);args=parser.parse_args()
    main(args.runtime.resolve() if args.runtime else None)
