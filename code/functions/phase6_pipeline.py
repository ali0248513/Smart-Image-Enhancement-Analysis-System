"""
Phase 6 – Final Integrated Pipeline  (Lab 06)
process_image(input_image) — complete enhancement pipeline.

Pipeline order:
  1. Grayscale-aware CLAHE for local contrast enhancement
  2. Gamma correction (γ=0.8) — mild brightening
  3. Log transform blend — shadow detail recovery
  4. Unsharp masking — edge / detail sharpening
  5. Histogram equalization on luminance channel (color images)
"""

import cv2
import numpy as np


# ── individual enhancement utilities ─────────────────────────────────────────

def _apply_clahe(gray: np.ndarray, clip: float = 2.0, tile: int = 8) -> np.ndarray:
    clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=(tile, tile))
    return clahe.apply(gray)


def _gamma_correction(img: np.ndarray, gamma: float) -> np.ndarray:
    table = np.array([(i / 255.0) ** gamma * 255 for i in range(256)], dtype=np.uint8)
    return cv2.LUT(img, table)


def _log_blend(img: np.ndarray, alpha: float = 0.4) -> np.ndarray:
    img_f = img.astype(np.float64) + 1.0
    c = 255.0 / np.log(1 + img_f.max())
    log_img = np.clip(c * np.log(img_f), 0, 255).astype(np.uint8)
    return cv2.addWeighted(img, 1 - alpha, log_img, alpha, 0)


def _unsharp_mask(img: np.ndarray, sigma: float = 1.0, strength: float = 1.5) -> np.ndarray:
    blurred = cv2.GaussianBlur(img, (0, 0), sigma)
    sharpened = cv2.addWeighted(img, strength, blurred, -(strength - 1), 0)
    return np.clip(sharpened, 0, 255).astype(np.uint8)


def _enhance_color(img_bgr: np.ndarray) -> np.ndarray:
    """Enhance color image via YCrCb luminance channel processing."""
    ycrcb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb)

    # CLAHE on Y channel
    y = _apply_clahe(y, clip=2.0)
    # Gamma brightening
    y = _gamma_correction(y, gamma=0.85)
    # Log shadow recovery (mild)
    y = _log_blend(y, alpha=0.25)
    # Sharpening
    y = _unsharp_mask(y, sigma=1.0, strength=1.4)

    merged = cv2.merge([y, cr, cb])
    return cv2.cvtColor(merged, cv2.COLOR_YCrCb2BGR)


def _enhance_gray(img_gray: np.ndarray) -> np.ndarray:
    """Enhance grayscale image."""
    out = _apply_clahe(img_gray, clip=2.0)
    out = _gamma_correction(out, gamma=0.85)
    out = _log_blend(out, alpha=0.25)
    out = _unsharp_mask(out, sigma=1.0, strength=1.4)
    return out


# ── public API ───────────────────────────────────────────────────────────────

def process_image(input_image: np.ndarray) -> np.ndarray:
    """
    Main pipeline function.

    Parameters
    ----------
    input_image : np.ndarray
        BGR (color) or single-channel (grayscale) image loaded by OpenCV.

    Returns
    -------
    enhanced : np.ndarray
        Enhanced image in the same color space as input.
    """
    if input_image is None:
        raise ValueError("process_image: input_image is None. Check the file path.")

    print("  [pipeline] Starting enhancement pipeline...")

    if len(input_image.shape) == 2 or input_image.shape[2] == 1:
        # grayscale path
        gray = input_image if len(input_image.shape) == 2 else input_image[:, :, 0]
        print("  [pipeline] Mode: Grayscale")
        enhanced = _enhance_gray(gray)
    else:
        # color path
        print("  [pipeline] Mode: Color (BGR → YCrCb)")
        enhanced = _enhance_color(input_image)

    print("  [pipeline] Enhancement complete.")
    return enhanced
