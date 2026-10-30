"""Audit comparable-run bookkeeping; never generate grades or quality metrics."""
import argparse
import collections
import datetime
import json
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT = ROOT/'data/p0/benchmark.json'
SHA = re.compile(r'[a-f0-9]{64}')
ID = re.compile(r'[a-z][a-z0-9-]{1,29}')


def digest(value):
    return isinstance(value, str) and bool(SHA.fullmatch(value))


def validate(data, as_of=None):
    as_of = as_of or datetime.date.today()
    errors, pending = [], []
    result = {'schema_valid': False, 'completed_automatic': 0, 'required_automatic': 100,
              'complete_products': 0, 'blocked_runs': 0, 'failed_runs': 0,
              'refined_runs': 0, 'bookkeeping_ready': False, 'research_validated': False,
              'errors': errors, 'pending': pending}
    if not isinstance(data, dict) or type(data.get('version')) is not int or data.get('version') != 1:
        errors.append('benchmark: expected version 1 object')
        return result
    products, pair_ids, runs = data.get('products'), data.get('pair_ids'), data.get('runs')
    if not isinstance(products, list) or len(products) != 5 or any(
            not isinstance(p, dict) or not isinstance(p.get('id'), str) or not ID.fullmatch(p['id']) for p in products):
        errors.append('benchmark: expected five product objects with safe distinct IDs')
        return result
    product_ids = {p['id'] for p in products}
    if len(product_ids) != 5:
        errors.append('benchmark: duplicate products')
    if not isinstance(pair_ids, list) or not all(isinstance(x, str) for x in pair_ids) or len(pair_ids) != 20 or set(pair_ids) != {f'P0-{i:03}' for i in range(1,21)}:
        errors.append('benchmark: expected twenty unique P0 pair IDs')
        return result
    if not isinstance(runs, list):
        errors.append('benchmark: expected runs list')
        return result
    if not digest(data.get('dataset_sha256')):
        pending.append('dataset: revision not frozen by SHA256')
    seen, inputs, complete = set(), {}, collections.Counter()
    for index, run in enumerate(runs,1):
        label = f'run {index}'
        before = len(errors)
        if not isinstance(run, dict):
            errors.append(f'{label}: expected object')
            continue
        product, pair, mode = run.get('product_id'), run.get('pair_id'), run.get('mode')
        if not isinstance(product, str) or product not in product_ids or not isinstance(pair, str) or pair not in pair_ids or mode not in ('automatic','refined'):
            errors.append(f'{label}: unknown product, pair or mode')
            continue
        key = (product, pair, mode)
        if key in seen:
            errors.append(f'{label}: duplicate product/pair/mode')
            continue
        seen.add(key)
        state = run.get('state')
        if state in ('blocked','failed'):
            reason = run.get('reason_code')
            if reason not in ('dataset','access','platform','privacy','license','execution-error'):
                errors.append(f'{label}: blocker/failure requires reason code')
            if any(field in run for field in ('elapsed_seconds','output_sha256','review_record_id')):
                errors.append(f'{label}: do not invent measurements for blocked/failed runs')
            if len(errors) == before:
                result['blocked_runs' if state == 'blocked' else 'failed_runs'] += 1
            continue
        if state != 'complete':
            errors.append(f'{label}: invalid run state')
            continue
        source, reference = run.get('source_sha256'), run.get('reference_sha256')
        if not digest(source) or not digest(reference) or source == reference:
            errors.append(f'{label}: valid, distinct input hashes required')
        elif pair in inputs and inputs[pair] != (source,reference):
            errors.append(f'{label}: inputs differ between products or modes')
        else:
            inputs[pair] = (source,reference)
        if not isinstance(run.get('tool_version'), str) or not run['tool_version'].strip():
            errors.append(f'{label}: actual tool version/build required')
        elapsed = run.get('elapsed_seconds')
        try:
            valid_elapsed = type(elapsed) in (int,float) and math.isfinite(elapsed) and elapsed >= 0
        except OverflowError:
            valid_elapsed = False
        if not valid_elapsed:
            errors.append(f'{label}: finite measured elapsed_seconds required')
        if run.get('timing_method') not in ('stopwatch','application-log'):
            errors.append(f'{label}: timing method required')
        try:
            if datetime.date.fromisoformat(run.get('recorded_on','')) > as_of:
                raise ValueError('future')
        except (ValueError,TypeError):
            errors.append(f'{label}: invalid/future observation date')
        if not digest(run.get('output_sha256')) or not digest(run.get('capture_sha256')):
            errors.append(f'{label}: output and capture integrity references required')
        for field, prefix in [('settings_record_id','SETTINGS-'),('color_record_id','COLOR-'),('review_record_id','REVIEW-')]:
            if not re.fullmatch(prefix+r'[A-Z0-9-]+', str(run.get(field,''))):
                errors.append(f'{label}: settings/color/visual-review record required')
        if len(errors) == before:
            if mode == 'automatic':
                result['completed_automatic'] += 1
                complete[product] += 1
            else:
                result['refined_runs'] += 1
    result['complete_products'] = sum(value == 20 for value in complete.values())
    if result['completed_automatic'] < 100:
        pending.append('benchmark: fewer than 5 x 20 complete automatic comparisons')
    result['schema_valid'] = not errors
    result['bookkeeping_ready'] = not errors and not pending and result['complete_products'] == 5
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records', type=pathlib.Path, nargs='?', default=DEFAULT)
    parser.add_argument('--ready', action='store_true')
    args = parser.parse_args(argv)
    try:
        result = validate(json.loads(args.records.read_text('utf-8')))
    except (OSError,ValueError,TypeError):
        print(json.dumps({'schema_valid':False,'errors':['cannot read valid benchmark JSON']}))
        return 1
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if not result['schema_valid'] else 2 if args.ready and not result['bookkeeping_ready'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
