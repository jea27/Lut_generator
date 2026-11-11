"""Run real regression tests with bundled Python/core; QA extras never ship."""
import argparse
import json
from pathlib import Path
import subprocess
import uuid
from build_embedded_runtime import ROOT,locked_download,extract,verify_sources

RUNNER=r'''
import sys,os,unittest,json
from pathlib import Path
root=Path(sys.argv[1]);runtime=Path(sys.executable).parent
sys.path.insert(0,sys.argv[2]);sys.path.append(str(root))
os.environ['LUMAFORGE_DATA_DIR']=sys.argv[3]
import packages.colour_core.engine as engine
assert Path(engine.__file__).resolve().is_relative_to((runtime/'app').resolve())
suite=unittest.defaultTestLoader.discover(str(root/'tests_mvp'))
class DiagnosticResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs);self.installer_errors=[]
    def addError(self,test,error):
        from apps.desktop.installer_helper import InstallError
        if isinstance(error[1],InstallError):
            detail={'test':test.id(),**error[1].report()}
            self.installer_errors.append(detail)
            print(json.dumps({'unexpected_installer_error':detail}),file=self.stream)
        super().addError(test,error)
result=unittest.TextTestRunner(verbosity=2,resultclass=DiagnosticResult).run(suite)
print(json.dumps({'python':sys.version.split()[0],'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'unexpected_installer_errors':result.installer_errors,'successful':result.wasSuccessful(),'core_loaded_from_packaged_runtime':True,'isolated':sys.flags.isolated,'no_site':sys.flags.no_site,'qa_dependencies_shipped':False,'clean_windows':False}))
raise SystemExit(not result.wasSuccessful())
'''


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('runtime',type=Path);parser.add_argument('report',type=Path);parser.add_argument('--offline',action='store_true');args=parser.parse_args()
    runtime=args.runtime.resolve();verify_sources(runtime,ROOT/'.lumaforge-local/downloads')
    private=ROOT/'.lumaforge-local'/('runtime-tests-'+str(uuid.uuid4()));private.mkdir()
    lock=json.loads((ROOT/'packaging/runtime-qa.lock.json').read_text(encoding='utf-8'))
    files={}
    for item in lock['packages']:
        archive=locked_download(item,ROOT/'.lumaforge-local/downloads',args.offline)
        extract(archive,item,private,files,[])
    result=subprocess.run([str(runtime/'python.exe'),'-I','-S','-B','-c',RUNNER,str(ROOT),str(private/'vendor'),str(private/'data')],
                          cwd=private,capture_output=True,text=True,timeout=180)
    (private/'unittest.log').write_text(result.stdout+result.stderr,encoding='utf-8')
    report=json.loads(result.stdout.strip().splitlines()[-1]);args.report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report));raise SystemExit(result.returncode)


if __name__=='__main__':main()
