"""Read-only synthetic preflight checks; never invoke a VM, installer or host store."""
import base64
import json
import os
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT=Path(__file__).resolve().parents[1]

class VmPreflightTests(unittest.TestCase):
    def test_both_entrypoints_refuse_prior_data_installations_and_unreadable_registry(self):
        shell=shutil.which('powershell.exe')
        if not shell:self.skipTest('Windows PowerShell unavailable')
        for filename in ('qa_vm_assistant.ps1','qa_vm_cycle.ps1'):
            path=str(ROOT/'scripts'/filename).replace("'","''")
            script=r'''
$ErrorActionPreference='Stop'
$tokens=$null;$errors=$null
$ast=[Management.Automation.Language.Parser]::ParseFile('__PATH__',[ref]$tokens,[ref]$errors)
if($errors.Count){throw 'Invalid PowerShell AST'}
foreach($name in @('Test-LfColorStudioRegistration','Assert-LfNoExistingColorStudio')){
 $definition=@($ast.FindAll({param($node) $node -is [Management.Automation.Language.FunctionDefinitionAst] -and $node.Name -eq $name},$true))
 if($definition.Count -ne 1){throw 'Expected one preflight definition'}
 # Only trusted function definitions are loaded. Top-level VM/install code is never run.
 Invoke-Expression $definition[0].Extent.Text
}
function Test-Path {param([string]$LiteralPath)
 if($script:fixture -eq 'data'){return $LiteralPath.EndsWith('\ColorStudioBetaData')}
 if($script:fixture -eq 'install'){return $LiteralPath.EndsWith('\Color Studio Beta')}
 return $false
}
function Test-LfColorStudioRegistration {
 if($script:fixture -eq 'denied'){throw 'Synthetic registry access denied'}
 return $script:fixture -eq 'registered'
}
$result=@()
foreach($script:fixture in @('clean','data','install','registered','denied')){
 $reached_install=$false
 try{Assert-LfNoExistingColorStudio;$reached_install=$true}catch{}
 $result+=@{fixture=$script:fixture;reached_install=$reached_install}
}
$result|ConvertTo-Json -Compress
'''.replace('__PATH__',path)
            env={k:v for k,v in os.environ.items() if k.upper()!='PSMODULEPATH'}
            command=base64.b64encode(script.encode('utf-16-le')).decode('ascii')
            result=subprocess.run([shell,'-NoProfile','-NonInteractive','-EncodedCommand',command],env=env,capture_output=True,text=True,timeout=25)
            self.assertEqual(result.returncode,0,result.stderr)
            rows=json.loads(result.stdout)
            self.assertEqual({r['fixture']:r['reached_install'] for r in rows},
                {'clean':True,'data':False,'install':False,'registered':False,'denied':False},filename)

if __name__=='__main__':unittest.main()
