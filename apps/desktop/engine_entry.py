"""Packaged sidecar: owns its loopback socket and exits with its native parent."""
import argparse
import json
import os
import socket
import threading
import time
import uvicorn
import psutil
from apps.api.main import app


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--parent',type=int,required=True)
    args=parser.parse_args()
    parent=psutil.Process(args.parent);started=parent.create_time()
    listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    listener.bind(('127.0.0.1',0));listener.listen(128)
    port=listener.getsockname()[1]
    server=uvicorn.Server(uvicorn.Config(app,host='127.0.0.1',port=port,access_log=False,log_level='error',proxy_headers=False))
    def supervise():
        while True:
            time.sleep(.4)
            try:alive=parent.is_running() and parent.create_time()==started
            except psutil.Error:alive=False
            if not alive:
                server.should_exit=True
                time.sleep(3)
                os._exit(0)
    threading.Thread(target=supervise,daemon=True).start()
    # Only public connection metadata: session secrets are never written to stdout.
    print(json.dumps({'port':port,'version':'0.2.0-beta.1'}),flush=True)
    try:server.run(sockets=[listener])
    finally:listener.close()


if __name__=='__main__':main()
