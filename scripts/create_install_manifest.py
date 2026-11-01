"""Pin the full staged installer payload after compiling the native launcher."""
import json
from pathlib import Path
import subprocess
if __package__:
    from .build_embedded_runtime import ROOT, digest, verify_bundle
    from .audit_nsis_payload import launcher_match
else:
    from build_embedded_runtime import ROOT, digest, verify_bundle
    from audit_nsis_payload import launcher_match


def create(root=ROOT):
    binaries=root/'apps/desktop/src-tauri/binaries'
    runtime=binaries/'runtime'
    record=verify_bundle(runtime)
    source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    if record['source']!=source:raise ValueError('Runtime source differs from the current commit')
    config=json.loads((root/'apps/desktop/src-tauri/tauri.conf.json').read_bytes())
    raw=(root/'apps/desktop/src-tauri/target/release/color-studio-beta.exe').read_bytes()
    marker=b'__TAURI_BUNDLE_TYPE_VAR_'
    if raw.count(marker+b'UNK')!=1:raise ValueError('Expected the unique unbundled Tauri marker')
    installed=raw.replace(marker+b'UNK',marker+b'NSS')
    launcher_match(raw,installed)
    files={'color-studio-beta.exe':digest(installed)}
    for base,prefix in ((runtime,'runtime'),(root/'packaging/notices','notices')):
        for path in base.rglob('*'):
            if path.is_symlink():raise ValueError('Linked payload input')
            if path.is_file():files[prefix+'/'+path.relative_to(base).as_posix()]=digest(path.read_bytes())
    ledger={'schema':1,'product':config['identifier'],'version':config['version'],'source':source,
            'files':dict(sorted(files.items())),'generated':['uninstall.exe']}
    raw=(json.dumps(ledger,sort_keys=True,indent=2)+'\n').encode()
    (binaries/'installer-manifest.json').write_bytes(raw)
    (binaries/'installer-vars.nsh').write_bytes(('!define LF_INSTALL_MANIFEST_SHA256 "'+digest(raw)+'"\n').encode())
    return {'files':len(files),'manifest_sha256':digest(raw),'source':source,'version':config['version']}


if __name__=='__main__':print(json.dumps(create()))
