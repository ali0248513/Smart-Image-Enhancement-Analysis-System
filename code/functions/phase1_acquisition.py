"""
Phase 1 – Image Acquisition & Understanding  (Lab 01)
Loads image, converts to grayscale, displays matrix snippet,
resolution, and data type. Saves initial report figure.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def image_acquisition(img_rgb: np.ndarray, img_gray: np.ndarray, results_dir: str) -> None:
    h, w, c = img_rgb.shape

    # ── console report ──────────────────────────────────────────────────────
    print(f"  Resolution : {w} x {h} pixels")
    print(f"  Channels   : {c}  |  Data type: {img_rgb.dtype}")
    print(f"  Grayscale shape: {img_gray.shape}")
    print("  Image matrix (top-left 5x5 grayscale):")
    print(img_gray[:5, :5])

    # ── figure ──────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(14, 8))
    fig.suptitle("Phase 1 – Image Acquisition & Understanding", fontsize=14, fontweight="bold")

    ax1 = fig.add_subplot(2, 3, 1)
    ax1.imshow(img_rgb)
    ax1.set_title("RGB Input Image")
    ax1.axis("off")

    ax2 = fig.add_subplot(2, 3, 2)
    ax2.imshow(img_gray, cmap="gray")
    ax2.set_title("Grayscale Conversion")
    ax2.axis("off")

    ax3 = fig.add_subplot(2, 3, 3)
    ax3.axis("off")
    info = (
        f"Resolution : {w} × {h} px\n"
        f"Channels   : {c}\n"
        f"Data type  : {img_rgb.dtype}\n"
        f"Min value  : {img_rgb.min()}\n"
        f"Max value  : {img_rgb.max()}\n"
        f"Mean value : {img_rgb.mean():.2f}"
    )
    ax3.text(0.05, 0.5, info, transform=ax3.transAxes,
             fontsize=12, verticalalignment="center",
             fontfamily="monospace",
             bbox=dict(boxstyle="round", facecolor="#f0f0f0", alpha=0.8))
    ax3.set_title("Image Report")

    # show pixel matrix
    ax4 = fig.add_subplot(2, 1, 2)
    ax4.axis("off")
    snippet = img_gray[:8, :8].astype(int)
    rows = [" ".join(f"{v:3d}" for v in row) for row in snippet]
    matrix_str = "Grayscale pixel matrix (top-left 8×8):\n\n" + "\n".join(rows)
    ax4.text(0.05, 0.5, matrix_str, transform=ax4.transAxes,
             fontsize=10, verticalalignment="center",
             fontfamily="monospace",
             bbox=dict(boxstyle="round", facecolor="#e8f4fd", alpha=0.9))

    plt.tight_layout()
    out_path = os.path.join(results_dir, "phase1_acquisition.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved → {out_path}")
