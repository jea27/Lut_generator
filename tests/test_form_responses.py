import copy
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from scripts.register_form_response import VERSION, register, validate


def fixture():
    # Synthetic infrastructure fixture; never written to the project registry.
    return {"version": VERSION, "response_id": "12345678-1234-4123-8123-123456789abc",
            "participant_code": "R001", "evidence_type": "self_report_form",
            "status": "submitted_unverified", "notes_consent": True, "price_eur_shown": 49,
            "completed_utc": "2026-10-30T10:03:00Z",
            "stage_completed_utc": ["2026-10-30T10:00:00Z", "2026-10-30T10:01:00Z", "2026-10-30T10:02:00Z"],
            "answers": [{"question": f"Q{i}", "answer": "", "disposition": "omitted"} for i in range(1, 16)]}


class FormTests(unittest.TestCase):
    def test_omissions_are_not_purchase_intent(self):
        data = validate(fixture())
        self.assertTrue(all(a["disposition"] == "omitted" for a in data["answers"]))
        self.assertEqual(data["status"], "submitted_unverified")

    def test_rejects_forged_evidence_class_and_extra_identity(self):
        for key, value in [("email", "private"), ("evidence_type", "interview_notes"),
                           ("status", "verified"), ("notes_consent", False), ("price_eur_shown", True)]:
            data = fixture(); data[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate(data)

    def test_invalid_sequence_and_answers(self):
        for mutate in [lambda d: d["stage_completed_utc"].reverse(),
                       lambda d: d["answers"].pop(),
                       lambda d: d["answers"][0].update(answer="x" * 2001),
                       lambda d: d.update(participant_code="R000"),
                       lambda d: d.update(participant_code="../../evil")]:
            data = fixture(); mutate(data)
            with self.assertRaises(ValueError):
                validate(data)

    def test_private_integrity_receipt_and_dedupe(self):
        import hashlib
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "synthetic.json"
            source.write_text(json.dumps(fixture()), encoding="utf-8")
            receipt = register(source, root)
            self.assertEqual(receipt["sha256"], hashlib.sha256(source.read_bytes()).hexdigest())
            self.assertFalse(receipt["counts_as_interview"])
            self.assertEqual(receipt["verification"], "pending_human")
            with self.assertRaises(ValueError):
                register(source, root)
            data = fixture(); data["response_id"] = "abcdefab-1234-4123-8123-123456789abc"
            source.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(ValueError):
                register(source, root)
            self.assertFalse((root / "data/p0/interviews.json").exists())

    def test_synthetic_gui_code_cannot_enter_participant_receipts(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'synthetic.json'
            data = fixture(); data['participant_code'] = 'R999'
            source.write_text(json.dumps(data), encoding='utf-8')
            with self.assertRaises(ValueError):
                register(source, directory)
            self.assertFalse((Path(directory) / '.research-private/responses').exists())

    @unittest.skipUnless(shutil.which("node"), "Node unavailable")
    def test_browser_export_matches_python_schema(self):
        root = Path(__file__).resolve().parents[1]
        script = """
const assert = require('node:assert/strict');
const {makeResponse, QUESTIONS} = require('./research/form.js');
assert.equal(QUESTIONS.length, 15);
const times=['2026-10-30T10:00:00Z','2026-10-30T10:01:00Z','2026-10-30T10:02:00Z'];
const args=['R001', true, Array(15).fill(''), times, '12345678-1234-4123-8123-123456789abc', '2026-10-30T10:03:00Z'];
assert.throws(()=>makeResponse('bad', ...args.slice(1)));
assert.throws(()=>makeResponse(args[0], false, ...args.slice(2)));
const response = makeResponse(...args);
assert.equal(response.evidence_type, 'self_report_form');
assert.equal(response.status, 'submitted_unverified');
console.log(JSON.stringify(response));
"""
        result = subprocess.run(["node", "-e", script], cwd=root, capture_output=True, text=True, check=True)
        self.assertEqual(validate(json.loads(result.stdout))["version"], VERSION)

    def test_form_is_outside_public_site_and_no_external_submission(self):
        root = Path(__file__).resolve().parents[1]
        html = (root / "research/form.html").read_text(encoding="utf-8")
        js = (root / "research/form.js").read_text(encoding="utf-8")
        self.assertIn("connect-src 'none'", html)
        self.assertIn("form-action 'none'", html)
        self.assertNotIn("fetch(", js)
        self.assertNotIn("XMLHttpRequest", js)
        self.assertFalse((root / "site/research/form.html").exists())
