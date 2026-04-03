"""
Phase 5 – Histogram Processing  (Lab 05)
Plots histogram, analyzes contrast distribution,
applies histogram equalization, before/after comparison.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def histogram_processing(img_gray: np.ndarray, results_dir: str) -> None:
    # ── equalization ─────────────────────────────────────────────────────────
    equalized = cv2.equalizeHist(img_gray)

    # ── CLAHE (Contrast Limited Adaptive Histogram Equalization) ─────────────
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_img = clahe.apply(img_gray)

    # ── figure ───────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle("Phase 5 – Histogram Processing", fontsize=13, fontweight="bold")

    images   = [img_gray,   equalized,              clahe_img]
    titles   = ["Original", "Histogram Equalized",  "CLAHE"]
    colors   = ["steelblue","darkorange",            "seagreen"]

    for col, (img, title, color) in enumerate(zip(images, titles, colors)):
        # image row
        ax_img = fig.add_subplot(3, 3, col + 1)
        ax_img.imshow(img, cmap="gray", vmin=0, vmax=255)
        ax_img.set_title(title, fontweight="bold")
        ax_img.axis("off")

        # histogram row
        ax_hist = fig.add_subplot(3, 3, col + 4)
        ax_hist.hist(img.ravel(), bins=256, range=(0, 255), color=color, alpha=0.8)
        ax_hist.set_xlim(0, 255)
        ax_hist.set_title(f"Histogram – {title}", fontsize=9)
        ax_hist.set_xlabel("Pixel Intensity")
        ax_hist.set_ylabel("Frequency")

        # CDF row
        ax_cdf = fig.add_subplot(3, 3, col + 7)
        hist_vals, bin_edges = np.histogram(img.ravel(), bins=256, range=(0, 256))
        cdf = hist_vals.cumsum()
        cdf_norm = cdf / cdf[-1]
        ax_cdf.plot(np.arange(256), cdf_norm, color=color, linewidth=1.5)
        ax_cdf.set_xlim(0, 255)
        ax_cdf.set_ylim(0, 1)
        ax_cdf.set_title(f"CDF – {title}", fontsize=9)
        ax_cdf.set_xlabel("Intensity")
        ax_cdf.set_ylabel("Cumulative Probability")
        ax_cdf.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "phase5_histogram.png"), dpi=150, bbox_inches="tight")
    plt.close()

    # ── contrast analysis ─────────────────────────────────────────────────────
    def contrast_score(img):
        return img.std()

    print("  Contrast analysis (std dev of pixel values):")
    for name, img in [("Original", img_gray), ("Equalized", equalized), ("CLAHE", clahe_img)]:
        print(f"    {name:<20} std={contrast_score(img):.2f}  min={img.min()}  max={img.max()}")

    print(f"  Saved → {results_dir}/phase5_histogram.png")
