"""Read-only P0 checkpoint: evidence bookkeeping + GitHub acceptance, never P1 authorization."""
import argparse
import importlib.util
import json
import os
import pathlib
import re
import shutil
import subprocess
import datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
TASKS = tuple(f'COL-{i:03}' for i in range(1,7))
VALIDATORS = {'interviews':'validate_interviews.py', 'dataset':'validate_dataset.py',
              'benchmark':'validate_benchmark.py'}


def approvals_from_issues(issues):
    found, duplicates = {}, []
    for issue in issues:
        if not isinstance(issue, dict):
            continue
        labels = {label.get('name') for label in issue.get('labels',[]) if isinstance(label,dict)}
        match = re.match(r'^\[(COL-\d{3})\]', str(issue.get('title','')))
        if not match or match[1] not in TASKS or 'roadmap' not in labels:
            continue
        tid = match[1]
        if tid in found:
            duplicates.append(tid)
        found[tid] = str(issue.get('state','')).lower() == 'closed' and 'approved' in labels
    accepted = [tid for tid in TASKS if found.get(tid) and tid not in duplicates]
    return {'available':True, 'accepted':accepted,
            'pending':[tid for tid in TASKS if tid not in accepted],
            'duplicate_ids':sorted(set(duplicates)),
            'all_accepted':len(accepted)==6 and not duplicates}


def github_approvals(gh_path=None):
    gh = gh_path or shutil.which('gh')
    if not gh:
        candidate = pathlib.Path(os.environ.get('ProgramFiles', ''))/'GitHub CLI/gh.exe'
        if candidate.is_file():
            gh = str(candidate)
    unavailable = {'available':False, 'accepted':[], 'pending':list(TASKS),
                   'duplicate_ids':[], 'all_accepted':False}
    if not gh:
        return unavailable
    try:
        result = subprocess.run([gh,'issue','list','--repo','jea27/Lut_generator',
            '--state','all','--limit','1000','--json','number,title,state,labels'],
            capture_output=True,text=True,encoding='utf-8',timeout=30,check=True)
        issues = json.loads(result.stdout)
        if not isinstance(issues,list) or len(issues)>=1000:
            return unavailable
        return approvals_from_issues(issues)
    except (OSError,ValueError,subprocess.SubprocessError):
        return unavailable  # Do not echo CLI credentials/errors or raw issue text.


def load_reports(paths, media_root=None, as_of=None):
    results = {}
    for name, filename in VALIDATORS.items():
        try:
            spec = importlib.util.spec_from_file_location('p0_'+name,ROOT/'scripts'/filename)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            data = json.loads(paths[name].read_text('utf-8'))
            result = module.validate(data, media_root if name=='dataset' else as_of)
            results[name] = result
        except (OSError,ValueError,TypeError,AttributeError):
            results[name] = {'schema_valid':False,'errors':['validator or evidence record unavailable']}
    return results


def summarize(reports, approvals=None):
    approvals = approvals or {'available':False,'accepted':[], 'pending':list(TASKS),
                             'duplicate_ids':[], 'all_accepted':False}
    ready_keys = {'interviews':'gate_ready','dataset':'gate_ready','benchmark':'bookkeeping_ready'}
    evidence = {name:reports.get(name,{}).get('schema_valid') is True and
                      reports.get(name,{}).get(key) is True for name,key in ready_keys.items()}
    counts = {'interviews':reports.get('interviews',{}).get('completed_sessions',0),
              'dataset_pairs':reports.get('dataset',{}).get('ready_pairs',0),
              'benchmark_automatic':reports.get('benchmark',{}).get('completed_automatic',0)}
    return {'version':1, 'counts':counts, 'evidence_ready':evidence,
            'technical_evidence_ready':all(evidence.values()), 'github_acceptance':approvals,
            'p0_records_and_acceptance_complete':all(evidence.values()) and approvals.get('all_accepted') is True,
            'automatic_p1_authorization':False,
            'p1_instruction':'Read explicit human authorization after P0; this tool never grants it.',
            'errors':{name:report.get('errors',[]) for name,report in reports.items() if not report.get('schema_valid')},
            'raw_private_evidence_logged':False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in VALIDATORS:
        parser.add_argument('--'+name, type=pathlib.Path, default=ROOT/'data/p0'/f'{name}.json')
    parser.add_argument('--media-root', type=pathlib.Path)
    parser.add_argument('--as-of', type=datetime.date.fromisoformat)
    parser.add_argument('--github', action='store_true', help='Read canonical Issues; never write labels or close tasks')
    parser.add_argument('--gh-path')
    parser.add_argument('--ready', action='store_true')
    args = parser.parse_args(argv)
    reports = load_reports({name:getattr(args,name) for name in VALIDATORS},args.media_root,args.as_of)
    result = summarize(reports,github_approvals(args.gh_path) if args.github else None)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if result['errors'] else 2 if args.ready and not result['p0_records_and_acceptance_complete'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
