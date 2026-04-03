"""
Phase 3 – Geometric Transformations  (Lab 03)
Rotation, Translation, Shearing + inverse restoration.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def _rotate(img: np.ndarray, angle: float) -> np.ndarray:
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def _translate(img: np.ndarray, tx: int, ty: int) -> np.ndarray:
    h, w = img.shape[:2]
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    return cv2.warpAffine(img, M, (w, h))


def _shear(img: np.ndarray, shx: float = 0.3, shy: float = 0.0) -> np.ndarray:
    h, w = img.shape[:2]
    M = np.float32([[1, shx, 0], [shy, 1, 0]])
    new_w = int(w + abs(shx) * h)
    new_h = int(h + abs(shy) * w)
    return cv2.warpAffine(img, M, (new_w, new_h))


def geometric_transformations(img_gray: np.ndarray, results_dir: str) -> None:
    angles = [30, 45, 60, 90, 120, 150, 180]

    # ── Rotation grid ────────────────────────────────────────────────────────
    fig, axes = plt.subplots(2, 4, figsize=(18, 9))
    fig.suptitle("Phase 3 – Rotations (30° → 180°)", fontsize=13, fontweight="bold")
    axes[0, 0].imshow(img_gray, cmap="gray"); axes[0, 0].set_title("Original"); axes[0, 0].axis("off")

    for idx, angle in enumerate(angles):
        ax = axes[(idx + 1) // 4, (idx + 1) % 4]
        rotated = _rotate(img_gray, angle)
        ax.imshow(rotated, cmap="gray")
        ax.set_title(f"Rotation {angle}°")
        ax.axis("off")

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "phase3_rotations.png"), dpi=150, bbox_inches="tight")
    plt.close()

    # ── Translation & Shear ──────────────────────────────────────────────────
    translated = _translate(img_gray, tx=40, ty=30)
    sheared    = _shear(img_gray, shx=0.3)

    # Inverse of translation
    translated_inv = _translate(translated, tx=-40, ty=-30)

    # Inverse of rotation (example: 45° → -45°)
    rotated_45     = _rotate(img_gray, 45)
    rotated_45_inv = _rotate(rotated_45, -45)

    fig, axes = plt.subplots(2, 4, figsize=(18, 9))
    fig.suptitle("Phase 3 – Translation, Shear & Inverse Transformations", fontsize=13, fontweight="bold")

    plots = [
        (img_gray,        "Original"),
        (translated,      "Translated (+40, +30)"),
        (translated_inv,  "Inverse Translation"),
        (sheared,         "Sheared (shx=0.3)"),
        (img_gray,        "Original"),
        (rotated_45,      "Rotated 45°"),
        (rotated_45_inv,  "Inverse Rotation (−45°)"),
        (np.abs(img_gray.astype(int) - cv2.resize(rotated_45_inv, img_gray.shape[::-1])).astype(np.uint8),
         "Difference (Original − Restored)"),
    ]

    for ax, (image, title) in zip(axes.flat, plots):
        h, w = image.shape[:2]
        display = cv2.resize(image, (img_gray.shape[1], img_gray.shape[0])) if image.shape != img_gray.shape else image
        ax.imshow(display, cmap="gray")
        ax.set_title(title, fontsize=9)
        ax.axis("off")

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "phase3_transforms.png"), dpi=150, bbox_inches="tight")
    plt.close()

    print(f"  Saved → {results_dir}/phase3_rotations.png")
    print(f"  Saved → {results_dir}/phase3_transforms.png")
