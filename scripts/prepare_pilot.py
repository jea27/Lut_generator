"""Download four CC0 backplates, unchanged; no benchmark or P0 approval."""
import argparse
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

BASE = "https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Backplates/rural_landscape"
FILES = {
    "DSC_0106": {"jpg_plain": (7227955, "5787d4d2d84bf857e15c1b2eaf29ad78"),
                 "jpg_pretty": (11523209, "c026f3eb7ac7c37b9e068b8ef029008e")},
    "DSC_0181": {"jpg_plain": (6276679, "ca034964d2467bc9f45e7979581b1868"),
                 "jpg_pretty": (9745257, "977640e4967f704a18df40a5f9a3faa9")},
}


def inspect_bytes(data, expected_size, expected_md5):
    from PIL import Image
    if len(data) != expected_size or hashlib.md5(data).hexdigest() != expected_md5:
        raise ValueError("Provider size/MD5 mismatch; reject asset")
    with Image.open(io.BytesIO(data)) as image:
        image.verify()
    with Image.open(io.BytesIO(data)) as image:
        if image.format != "JPEG" or image.width * image.height > 50_000_000:
            raise ValueError("Unexpected image format or dimensions")
        image.load()
        return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
                "width": image.width, "height": image.height,
                "mode": image.mode, "icc_present": bool(image.info.get("icc_profile")),
                "color_review": "pending"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="Explicit network opt-in")
    args = parser.parse_args()
    if not args.download:
        parser.error("Use --download after checking docs/P0_PILOTO_FUENTES.md")
    root = Path(__file__).resolve().parents[1]
    media = root / ".research-media" / "polyhaven-rural"
    media.mkdir(parents=True, exist_ok=True)
    manifest = {"version": 1, "evidence_type": "real_photo_infrastructure_pilot",
                "retrieved_utc": datetime.now(timezone.utc).isoformat(),
                "author": "Sergej Majboroda", "provider": "Poly Haven",
                "source_page": "https://polyhaven.com/a/rural_landscape",
                "metadata_url": "https://api.polyhaven.com/files/rural_landscape",
                "license": "CC0-1.0", "license_url": "https://polyhaven.com/license",
                "deed": "https://creativecommons.org/publicdomain/zero/1.0/",
                "coverage_review": "pending", "pairs": []}
    for capture, versions in FILES.items():
        assets = []
        for variant, (size, md5) in versions.items():
            url = f"{BASE}/{variant}/{capture}.jpg"
            destination = media / f"{capture}-{variant}.jpg"
            if destination.exists():
                data = destination.read_bytes()
            else:
                request = Request(url, headers={"User-Agent": "LumaForge-P0-research/1.0"})
                with urlopen(request, timeout=60) as response:
                    if not response.url.startswith(BASE + "/"):
                        raise ValueError("Unexpected redirect")
                    data = response.read(size + 1)
            record = inspect_bytes(data, size, md5)
            if not destination.exists():
                with destination.open("xb") as stream:
                    stream.write(data)
            record.update(url=url, provider_md5=md5,
                          local_path=destination.relative_to(root).as_posix(), variant=variant)
            assets.append(record)
        manifest["pairs"].append({"capture": capture, "assets": assets,
                                  "alignment_verified": False, "ground_truth": False})
    target = root / "data/p0/pilot.json"
    target.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"files_verified": 4, "pairs": 2, "manifest": "data/p0/pilot.json",
                      "p0_approved": False}))


if __name__ == "__main__":
    main()
