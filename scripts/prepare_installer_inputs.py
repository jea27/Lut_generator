"""Prepare hash-locked NSIS/bootstrapper inputs in the worktree's Tauri cache.

No host DLLs, global Tauri cache mutation, bootstrapper execution or installation.
All redirects must remain HTTPS, before any redirected request is sent.
"""
import argparse
import json
from pathlib import Path
import urllib.parse
import urllib.request
import zipfile
if __package__:
    from .build_embedded_runtime import ROOT,digest,safe_member
    from .audit_nsis_payload import prepare_archive,verify_toolchain
else:
    from build_embedded_runtime import ROOT,digest,safe_member
    from audit_nsis_payload import prepare_archive,verify_toolchain


class HttpsRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if urllib.parse.urlparse(newurl).scheme!='https':raise ValueError('Non-HTTPS redirect refused')
        return super().redirect_request(req,fp,code,msg,headers,newurl)


def fetch(item,path,offline=False):
    if urllib.parse.urlparse(item['url']).scheme!='https':raise ValueError('Non-HTTPS input refused')
    if path.exists():
        if path.is_symlink() or digest(path.read_bytes())!=item['sha256']:raise ValueError('Changed installer input cache')
        return path
    if offline:raise ValueError('Missing pinned offline installer input: '+path.name)
    with urllib.request.build_opener(HttpsRedirects()).open(item['url'],timeout=90) as response:
        raw=response.read(64*1024*1024+1)
    if len(raw)>64*1024*1024 or digest(raw)!=item['sha256']:raise ValueError('Downloaded installer input hash mismatch')
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as stream:stream.write(raw)
    return path


def prepare(offline=False):
    lock=json.loads((ROOT/'packaging/nsis-toolchain.lock.json').read_bytes())
    cache=ROOT/'apps/desktop/src-tauri/target/.tauri'
    nsis=cache/'NSIS'
    archive=prepare_archive(offline)
    # Refuse any redirected staging path, even when it was created by other tooling.
    for ancestor in (nsis,*nsis.parents):
        if ancestor.is_symlink() or (ancestor.exists() and getattr(ancestor.lstat(),'st_file_attributes',0)&0x400):raise ValueError('Linked installer tool cache')
    nsis.mkdir(parents=True,exist_ok=True)
    if any(p.is_symlink() or getattr(p.lstat(),'st_file_attributes',0)&0x400 for p in nsis.rglob('*')):raise ValueError('Linked NSIS cache entry')
    with zipfile.ZipFile(archive) as source:
        for item in source.infolist():
            name=safe_member(item.filename)
            if not name.startswith('nsis-3.13/'):raise ValueError('Unexpected NSIS archive root')
            if item.is_dir():continue
            path=nsis/name.removeprefix('nsis-3.13/')
            raw=source.read(item)
            if path.exists():
                if path.read_bytes()!=raw:raise ValueError('Changed worktree-local NSIS input')
            else:
                path.parent.mkdir(parents=True,exist_ok=True)
                with path.open('xb') as stream:stream.write(raw)
    plugin=fetch(lock['tauri-utils'],ROOT/'.lumaforge-local/downloads'/lock['tauri-utils']['filename'],offline)
    destination=nsis/'Plugins/x86-unicode/additional/nsis_tauri_utils.dll'
    destination.parent.mkdir(parents=True,exist_ok=True)
    if destination.exists() and destination.read_bytes()!=plugin.read_bytes():raise ValueError('Changed Tauri plugin')
    if not destination.exists():destination.write_bytes(plugin.read_bytes())
    verify_toolchain(archive,nsis)
    webview=json.loads((ROOT/'packaging/webview2.lock.json').read_bytes())
    if urllib.parse.urlparse(webview['url']).hostname!='msedge.sf.dl.delivery.mp.microsoft.com':raise ValueError('Unexpected bootstrapper origin')
    fetch(webview,cache/webview['filename'],offline)
    return {'nsis':'3.13','bootstrapper_sha256':webview['sha256'],'https_only':True,'executed':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--offline',action='store_true')
    args=parser.parse_args();print(json.dumps(prepare(args.offline)))
