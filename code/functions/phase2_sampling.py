"""
Phase 2 – Sampling & Quantization Analysis  (Lab 02)
Up/down samples image at multiple scales; reduces bit depth.
Produces a visual comparison grid and prints a comparison table.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def _resize(img: np.ndarray, scale: float) -> np.ndarray:
    h, w = img.shape[:2]
    new_w, new_h = max(1, int(w * scale)), max(1, int(h * scale))
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    # restore to original canvas size for comparison
    return cv2.resize(resized, (w, h), interpolation=cv2.INTER_NEAREST)


def _quantize(img: np.ndarray, bits: int) -> np.ndarray:
    levels = 2 ** bits
    factor = 256 // levels
    quantized = (img // factor) * factor
    return quantized.astype(np.uint8)


def sampling_quantization(img_gray: np.ndarray, results_dir: str) -> None:
    scales = [0.25, 0.5, 1.0, 1.5, 2.0]
    scale_labels = ["0.25×", "0.5×", "1.0× (original)", "1.5×", "2.0×"]
    bits_list = [8, 4, 2]

    # ── Sampling figure ──────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 5, figsize=(20, 4))
    fig.suptitle("Phase 2 – Sampling: Scale Comparison", fontsize=13, fontweight="bold")

    table_rows = []
    for ax, scale, label in zip(axes, scales, scale_labels):
        resampled = _resize(img_gray, scale)
        h_s = max(1, int(img_gray.shape[0] * scale))
        w_s = max(1, int(img_gray.shape[1] * scale))
        psnr_val = cv2.PSNR(img_gray, resampled)
        ax.imshow(resampled, cmap="gray", vmin=0, vmax=255)
        ax.set_title(f"{label}\n{w_s}×{h_s}", fontsize=9)
        ax.axis("off")
        quality = "Excellent" if scale == 1.0 else ("Good" if scale >= 0.5 else "Degraded")
        table_rows.append([label, f"{w_s}×{h_s}", f"{psnr_val:.1f} dB", quality])

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "phase2_sampling.png"), dpi=150, bbox_inches="tight")
    plt.close()

    # ── Quantization figure ──────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    fig.suptitle("Phase 2 – Quantization: Bit Depth Reduction", fontsize=13, fontweight="bold")

    for ax, bits in zip(axes, bits_list):
        q = _quantize(img_gray, bits)
        levels = 2 ** bits
        ax.imshow(q, cmap="gray", vmin=0, vmax=255)
        ax.set_title(f"{bits}-bit  ({levels} levels)", fontsize=10)
        ax.axis("off")

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "phase2_quantization.png"), dpi=150, bbox_inches="tight")
    plt.close()

    # ── console comparison table ─────────────────────────────────────────────
    print("  Sampling comparison table:")
    print(f"  {'Scale':<20} {'Resolution':<12} {'PSNR':<12} {'Quality'}")
    print("  " + "-" * 58)
    for row in table_rows:
        print(f"  {row[0]:<20} {row[1]:<12} {row[2]:<12} {row[3]}")

    print(f"\n  Saved → {results_dir}/phase2_sampling.png")
    print(f"  Saved → {results_dir}/phase2_quantization.png")
