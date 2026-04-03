"""
Lab 06: Smart Image Enhancement & Analysis System
Digital Image Processing - Mr. Ghulam Ali
Entry point: runs the full pipeline on a sample image
"""

import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, sys

sys.path.insert(0, os.path.dirname(__file__))

from functions.phase1_acquisition     import image_acquisition
from functions.phase2_sampling        import sampling_quantization
from functions.phase3_geometric       import geometric_transformations
from functions.phase4_intensity       import intensity_transformations
from functions.phase5_histogram       import histogram_processing
from functions.phase6_pipeline        import process_image

# ── paths ──────────────────────────────────────────────────────────────────
BASE   = os.path.dirname(os.path.dirname(__file__))
INPUT  = os.path.join(BASE, "images", "input",  "sample.jpg")
OUTPUT = os.path.join(BASE, "images", "output")
RESULTS= os.path.join(BASE, "results")

os.makedirs(OUTPUT,  exist_ok=True)
os.makedirs(RESULTS, exist_ok=True)

# ── generate a synthetic low-quality input if none exists ──────────────────
def create_sample_image(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = np.zeros((256, 256, 3), dtype=np.uint8)
    # gradient background
    for i in range(256):
        img[i, :, 0] = i          # R channel
        img[:, i, 1] = i          # G channel
    img[:, :, 2] = 80             # low blue (simulates low-quality image)
    # add some circles / shapes
    cv2.circle(img, (128,128), 60, (200,150,50), -1)
    cv2.rectangle(img, (20,20), (90,90), (50,100,200), -1)
    cv2.putText(img, "DIP", (90,155), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)
    # simulate low contrast by compressing range
    img = (img * 0.5 + 30).astype(np.uint8)
    cv2.imwrite(path, img)
    print(f"[main] Created synthetic sample image: {path}")

if not os.path.exists(INPUT):
    create_sample_image(INPUT)

img_bgr  = cv2.imread(INPUT)
img_rgb  = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

print("=" * 60)
print("  Smart Image Enhancement & Analysis System")
print("=" * 60)

# Phase 1
print("\n[Phase 1] Image Acquisition & Understanding")
image_acquisition(img_rgb, img_gray, RESULTS)

# Phase 2
print("\n[Phase 2] Sampling & Quantization")
sampling_quantization(img_gray, RESULTS)

# Phase 3
print("\n[Phase 3] Geometric Transformations")
geometric_transformations(img_gray, RESULTS)

# Phase 4
print("\n[Phase 4] Intensity Transformations")
intensity_transformations(img_gray, RESULTS)

# Phase 5
print("\n[Phase 5] Histogram Processing")
histogram_processing(img_gray, RESULTS)

# Phase 6 — Final Pipeline
print("\n[Phase 6] Final Integrated Pipeline")
enhanced = process_image(img_bgr)
cv2.imwrite(os.path.join(OUTPUT, "enhanced_output.png"), enhanced)

# side-by-side comparison
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(img_rgb);      axes[0].set_title("Original Input");  axes[0].axis("off")
axes[1].imshow(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))
axes[1].set_title("Enhanced Output"); axes[1].axis("off")
plt.suptitle("Final Pipeline: Input vs Enhanced", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS, "final_comparison.png"), dpi=150, bbox_inches="tight")
plt.close()

print("\n[main] All phases complete.")
print(f"[main] Results saved to: {RESULTS}/")
print(f"[main] Enhanced image : {OUTPUT}/enhanced_output.png")
print("=" * 60)
