"""Offline P0 measurement tools. No image grading, inference or task approval."""
import argparse
import hashlib
import io
import json
import math
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path


def timing_summary(seconds):
    if not seconds or any(type(x) not in (int, float) or not math.isfinite(x) or x < 0
                          for x in seconds):
        raise ValueError("Need observed finite nonnegative durations")
    ordered = sorted(seconds)
    return {"count": len(ordered), "median_seconds": statistics.median(ordered),
            "p95_nearest_rank_seconds": ordered[math.ceil(.95 * len(ordered)) - 1]}


def rgb_array(value):
    import numpy as np
    a = np.asarray(value, dtype=np.float64)
    if a.ndim != 3 or a.shape[2] != 3 or min(a.shape[:2]) < 7:
        raise ValueError("Need RGB arrays of at least 7x7")
    if not np.isfinite(a).all() or a.min() < 0 or a.max() > 1:
        raise ValueError("sRGB samples must be finite in [0,1]; no silent clipping")
    return a


def lab_d65(rgb):
    import numpy as np
    a = rgb_array(rgb)
    linear = np.where(a <= .04045, a / 12.92, ((a + .055) / 1.055) ** 2.4)
    matrix = np.array([[.4124564, .3575761, .1804375],
                       [.2126729, .7151522, .0721750],
                       [.0193339, .1191920, .9503041]])
    xyz = (linear @ matrix.T) / np.array([.95047, 1., 1.08883])
    delta = 6 / 29
    f = np.where(xyz > delta ** 3, np.cbrt(xyz), xyz / (3 * delta ** 2) + 4 / 29)
    return np.stack((116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])), axis=-1)


def box7(a):
    import numpy as np
    integral = np.pad(a, ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    return (integral[7:, 7:] - integral[:-7, 7:] - integral[7:, :-7]
            + integral[:-7, :-7]) / 49


def measure(output, target):
    import numpy as np
    a, b = rgb_array(output), rgb_array(target)
    if a.shape != b.shape:
        raise ValueError("Aligned target dimensions must match; no implicit registration")
    mse = float(np.mean((a - b) ** 2))
    delta_e = np.linalg.norm(lab_d65(a) - lab_d65(b), axis=-1)
    # Encoded-sRGB luma diagnostic, not physical luminance or perceptual quality.
    weights = np.array([.2126, .7152, .0722])
    x, y = a @ weights, b @ weights
    ux, uy = box7(x), box7(y)
    vx = np.maximum(0, (box7(x*x) - ux*ux) * 49/48)
    vy = np.maximum(0, (box7(y*y) - uy*uy) * 49/48)
    cov = (box7(x*y) - ux*uy) * 49/48
    ssim = ((2*ux*uy + .01**2) * (2*cov + .03**2)
            / ((ux*ux + uy*uy + .01**2) * (vx + vy + .03**2)))
    gradients_a = np.concatenate([np.diff(x, axis=0).ravel(), np.diff(x, axis=1).ravel()])
    gradients_b = np.concatenate([np.diff(y, axis=0).ravel(), np.diff(y, axis=1).ravel()])
    correlation = None
    if np.std(gradients_a) > 1e-12 and np.std(gradients_b) > 1e-12:
        correlation = float(np.corrcoef(gradients_a, gradients_b)[0, 1])
    return {"mse_encoded_srgb": mse, "psnr_db": None if mse == 0 else -10*math.log10(mse),
            "psnr_infinite": mse == 0, "delta_e76_d65_mean": float(delta_e.mean()),
            "delta_e76_d65_p95": float(np.percentile(delta_e, 95)),
            "ssim_uniform7_luma_valid_samplecov": float(ssim.mean()),
            "gradient_correlation": correlation,
            "output_endpoint_channel_fraction": float(np.mean((a == 0) | (a == 1)))}


def repeatability(outputs):
    import numpy as np
    if len(outputs) < 2:
        raise ValueError("At least two real repeated outputs required")
    arrays = [rgb_array(a) for a in outputs]
    if any(a.shape != arrays[0].shape for a in arrays):
        raise ValueError("Repeated output dimensions differ")
    return {"count": len(arrays), "max_abs_encoded_srgb_from_first":
            max(float(np.max(np.abs(a - arrays[0]))) for a in arrays[1:])}


def read_image(path, untagged_record):
    from PIL import Image, ImageCms, ImageOps
    payload = Path(path).read_bytes()
    with Image.open(io.BytesIO(payload)) as original:
        if original.width * original.height > 50_000_000 or original.mode != "RGB":
            raise ValueError("Only bounded opaque RGB stills supported")
        image = ImageOps.exif_transpose(original)
        profile = original.info.get("icc_profile")
        if profile:
            profile = ImageCms.ImageCmsProfile(io.BytesIO(profile))
            description = ImageCms.getProfileDescription(profile).strip()
            image = ImageCms.profileToProfile(image, profile, ImageCms.createProfile("sRGB"),
                                              renderingIntent=1, outputMode="RGB")
        elif untagged_record:
            description = "untagged; explicit assumption " + untagged_record
            image = image.copy()
        else:
            raise ValueError("Untagged image requires --untagged-srgb-record")
        return image, {"sha256": hashlib.sha256(payload).hexdigest(),
                       "profile": description, "oriented_size": list(image.size)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-image", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--aligned-target", action="store_true")
    parser.add_argument("--alignment-record", required=True)
    parser.add_argument("--untagged-srgb-record")
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    if not args.aligned_target or not args.alignment_record.strip():
        parser.error("Pixel fidelity requires an aligned same-content target and record")
    import numpy as np
    import PIL
    start = time.perf_counter()
    output, output_record = read_image(args.output_image, args.untagged_srgb_record)
    target, target_record = read_image(args.target, args.untagged_srgb_record)
    if output.size != target.size:
        raise ValueError("Dimensions differ before resize; target not accepted")
    output.thumbnail((512, 512), PIL.Image.Resampling.LANCZOS)
    target.thumbnail((512, 512), PIL.Image.Resampling.LANCZOS)
    metrics = measure(np.asarray(output)/255., np.asarray(target)/255.)
    report = {"version": 1, "evidence_type": "metric_measurement_only",
              "research_validated": False, "measured_utc": datetime.now(timezone.utc).isoformat(),
              "alignment_record": args.alignment_record,
              "output": output_record, "target": target_record,
              "measurement_size": list(output.size), "max_side": 512,
              "preprocess": "EXIF orientation; ICC to sRGB relative-colorimetric; Lanczos thumbnail",
              "numpy": np.__version__, "pillow": PIL.__version__, "metrics": metrics,
              "measurement_wall_seconds": time.perf_counter() - start,
              "model_inference_seconds": None, "lpips": None}
    # Never overwrite evidence or write into the canonical benchmark registry.
    with Path(args.report).open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"report_written": True, "research_validated": False}))


if __name__ == "__main__":
    main()
