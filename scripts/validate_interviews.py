"""Check anonymized interview records; do not collect, infer or invent responses."""
import argparse
import datetime
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT = ROOT/'data/p0/interviews.json'
FIELDS = {'id', 'segment', 'date', 'status', 'notes_consent', 'anonymized',
          'redaction_record_id', 'frequency_30d', 'current_solution', 'pay_intent',
          'problem_summary', 'evidence_type'}
INTENTS = {'buy_if_conditions', 'consider', 'not_buy', 'unknown', 'declined'}


def validate(data, as_of=None):
    as_of = as_of or datetime.date.today()
    errors, pending = [], []
    result = {'schema_valid': False, 'completed_sessions': 0, 'required_sessions': 12,
              'segments': dict.fromkeys('ABCD', 0), 'missing_answers': 0,
              'gate_ready': False, 'errors': errors, 'pending': pending}
    if not isinstance(data, dict) or type(data.get('version')) is not int or data.get('version') != 1 or not isinstance(data.get('interviews'), list):
        errors.append('registry: expected version 1 and interviews list')
        return result
    codes = set()
    for index, item in enumerate(data['interviews'], 1):
        label = f'record {index}'  # Never echo raw record values or private text.
        before = len(errors)
        if not isinstance(item, dict):
            errors.append(f'{label}: expected object')
            continue
        if set(item) - FIELDS:
            errors.append(f'{label}: unexpected fields; do not include contact data')
        code = item.get('id')
        if not isinstance(code, str) or not re.fullmatch(r'E(?:0[1-9]|[1-9][0-9])', code):
            errors.append(f'{label}: invalid participant code')
            code = None
        elif code in codes:
            errors.append(f'{label}: duplicate participant code')
        else:
            codes.add(code)
        if item.get('status') == 'draft':
            pending.append(f'{label}: draft not counted')
            continue
        if item.get('status') != 'complete':
            errors.append(f'{label}: invalid status')
            continue
        segment = item.get('segment')
        if not isinstance(segment, str) or segment not in 'ABCD' or len(segment) != 1:
            errors.append(f'{label}: invalid primary segment')
        try:
            occurred = datetime.date.fromisoformat(item.get('date', ''))
            if occurred > as_of:
                raise ValueError('future')
        except (ValueError, TypeError):
            errors.append(f'{label}: invalid or future interview date')
        if item.get('notes_consent') is not True or item.get('anonymized') is not True:
            errors.append(f'{label}: consent for notes and anonymization must be recorded')
        if not code or item.get('redaction_record_id') != f'REDACT-{code}':
            errors.append(f'{label}: human redaction review reference missing')
        frequency = item.get('frequency_30d')
        if frequency is not None and (type(frequency) is not int or frequency < 0):
            errors.append(f'{label}: frequency must be nonnegative integer or null, never imputed')
        if frequency is None:
            result['missing_answers'] += 1
        intent = item.get('pay_intent')
        if not isinstance(intent, str) or intent not in INTENTS:
            errors.append(f'{label}: invalid pay response; use unknown or declined explicitly')
        if intent in ('unknown', 'declined'):
            result['missing_answers'] += 1
        for field in ('current_solution', 'problem_summary'):
            value = item.get(field)
            if not isinstance(value, str) or not value.strip() or len(value) > 2000:
                errors.append(f'{label}: anonymized summary required (max 2000 characters)')
        if item.get('evidence_type') != 'interview_notes':
            errors.append(f'{label}: expected interview_notes; fixtures/concepts are not research')
        if len(errors) == before:
            result['completed_sessions'] += 1
            result['segments'][segment] += 1
    segments = result['segments']
    if result['completed_sessions'] < 12:
        pending.append('cohort: fewer than 12 complete eligible records')
    if segments['A'] < 4 or segments['B'] < 4 or segments['C'] + segments['D'] < 4:
        pending.append('cohort: minimum A=4, B=4, C/D=4 not reached')
    result['schema_valid'] = not errors
    result['gate_ready'] = not errors and not pending
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('records', type=pathlib.Path, nargs='?', default=DEFAULT)
    parser.add_argument('--ready', action='store_true')
    parser.add_argument('--as-of', type=datetime.date.fromisoformat)
    args = parser.parse_args(argv)
    try:
        report = validate(json.loads(args.records.read_text('utf-8')), args.as_of)
    except (OSError, ValueError, TypeError):
        print(json.dumps({'schema_valid': False, 'errors': ['cannot read valid record JSON']}))
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if not report['schema_valid'] else 2 if args.ready and not report['gate_ready'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
