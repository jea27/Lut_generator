"""Register a private receipt. Self-report is never converted to interview evidence."""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

VERSION = "LF-P0-FORM-2026-10-30-v1"


def validate(data):
    allowed = {"version", "response_id", "participant_code", "evidence_type", "status",
               "notes_consent", "price_eur_shown", "completed_utc", "stage_completed_utc", "answers"}
    if not isinstance(data, dict) or set(data) != allowed:
        raise ValueError("Unexpected response fields")
    if (data["version"] != VERSION or data["evidence_type"] != "self_report_form"
            or data["status"] != "submitted_unverified" or data["notes_consent"] is not True
            or type(data["price_eur_shown"]) is not int or data["price_eur_shown"] != 49):
        raise ValueError("Invalid instrument, consent or evidence class")
    if not isinstance(data["participant_code"], str) or not re.fullmatch(r"R(?!000)\d{3}", data["participant_code"], re.ASCII):
        raise ValueError("Invalid participant code")
    if not isinstance(data["response_id"], str) or not re.fullmatch(r"[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}", data["response_id"]):
        raise ValueError("Invalid response UUID")
    def date(value):
        if not isinstance(value, str):
            raise ValueError("Date must be ISO text")
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if result.utcoffset() != timezone.utc.utcoffset(result):
            raise ValueError("UTC date required")
        return result
    stages = data["stage_completed_utc"]
    if not isinstance(stages, list) or len(stages) != 3:
        raise ValueError("Three stage timestamps required")
    dates = [date(t) for t in stages] + [date(data["completed_utc"])]
    if dates != sorted(dates):
        raise ValueError("Stages out of order")
    answers = data["answers"]
    if not isinstance(answers, list) or len(answers) != 15:
        raise ValueError("15 optional questions required")
    for i, answer in enumerate(answers, 1):
        if (not isinstance(answer, dict) or set(answer) != {"question", "answer", "disposition"}
                or answer["question"] != f"Q{i}" or not isinstance(answer["answer"], str)
                or len(answer["answer"]) > 2000
                or answer["disposition"] != ("answered" if answer["answer"].strip() else "omitted")):
            raise ValueError("Invalid question/answer")
    return data


def register(source, root):
    if Path(source).stat().st_size > 200_000:
        raise ValueError("Response too large")
    payload = Path(source).read_bytes()
    if len(payload) > 200_000:
        raise ValueError("Response too large")
    data = validate(json.loads(payload))
    if data['participant_code'] == 'R999':
        raise ValueError('R999 is synthetic QA and cannot be registered as participant evidence')
    private = Path(root) / ".research-private" / "responses"
    private.mkdir(parents=True, exist_ok=True)
    receipts = []
    for path in private.glob("*.receipt.json"):
        receipts.append(json.loads(path.read_text(encoding="utf-8")))
    digest = hashlib.sha256(payload).hexdigest()
    if any(r["sha256"] == digest or r["response_id"] == data["response_id"]
           or r["participant_code"] == data["participant_code"] for r in receipts):
        raise ValueError("Duplicate participant/response; retain correction separately for human review")
    destination = private / (data["response_id"] + ".json")
    receipt_path = private / (data["response_id"] + ".receipt.json")
    if destination.exists() or receipt_path.exists():
        raise ValueError("Existing evidence will not be overwritten")
    receipt = {"version": 1, "response_id": data["response_id"], "participant_code": data["participant_code"],
               "sha256": digest, "received_utc": datetime.now(timezone.utc).isoformat(),
               "verification": "pending_human", "evidence_type": "self_report_form",
               "counts_as_interview": False}
    with destination.open("xb") as stream:
        stream.write(payload)
    with receipt_path.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("response")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    receipt = register(args.response, root)
    print(json.dumps({"registered_privately": True, "sha256": receipt["sha256"],
                      "counts_as_interview": False, "verification": "pending_human"}))


if __name__ == "__main__":
    main()
