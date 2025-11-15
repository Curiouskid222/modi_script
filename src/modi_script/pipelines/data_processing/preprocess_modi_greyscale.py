import os
import platform
from pathlib import Path
import cv2
import numpy as np
import random

def get_google_drive_path():
    """Locate Google Drive folder depending on OS."""
    system = platform.system()

    if system == "Windows":
        possible_paths = [
            Path("G:/My Drive"),
            Path("G:/MyDrive"),
            Path(f"C:/Users/{os.getenv('USERNAME')}/Google Drive"),
        ]
    elif system == "Darwin":
        possible_paths = [
            Path("/Volumes/GoogleDrive/My Drive"),
            Path(f"/Users/{os.getenv('USER')}/Library/CloudStorage/GoogleDrive"),
        ]
    else:
        possible_paths = [
            Path.home() / "GoogleDrive",
            Path("/mnt/GoogleDrive/My Drive"),
        ]

    for p in possible_paths:
        if p.exists():
            return p

    raise FileNotFoundError("Google Drive folder not found on this system.")


# ------------------------- IMAGE PROCESSING UTILS -------------------------

def preprocess_image(img, target_size=(224, 224)):
    """
    Apply grayscale → normalization → denoise → threshold → resize → augment.
    """

    # 1. Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Normalize (0–1)
    gray = gray.astype(np.float32) / 255.0

    # 3. Optional denoising (Gaussian)
    denoised = cv2.GaussianBlur(gray, (3, 3), 0)

    # 4. Adaptive Thresholding (light enhancement)
    thr = cv2.adaptiveThreshold(
        (denoised * 255).astype(np.uint8),
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    # 5. Resize to consistent shape
    resized = cv2.resize(thr, target_size, interpolation=cv2.INTER_AREA)

    # Convert back to float
    resized = resized.astype(np.float32) / 255.0

    # 6. Data Augmentation (random)
    aug = apply_augmentations(resized)

    return aug


def apply_augmentations(img):
    """Small safe augmentations for handwriting-style images."""
    # Random rotation ±10 degrees
    angle = random.uniform(-10, 10)
    h, w = img.shape
    M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
    rotated = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

    # Random shift
    max_shift = 5
    tx = random.randint(-max_shift, max_shift)
    ty = random.randint(-max_shift, max_shift)
    M_shift = np.float32([[1, 0, tx], [0, 1, ty]])
    shifted = cv2.warpAffine(rotated, M_shift, (w, h), borderMode=cv2.BORDER_REPLICATE)

    # Random blur
    if random.random() < 0.3:
        shifted = cv2.GaussianBlur(shifted, (3, 3), 0)

    return shifted


# ------------------------- MAIN PROCESSING PIPELINE -------------------------

def preprocess_all_modi_images():
    drive_root = get_google_drive_path()

    base = drive_root / "modi-script" / "data" / "01_raw" / "Modi_Alphabets"

    if not base.exists():
        raise FileNotFoundError(f"Folder not found: {base}")

    print(f" Starting preprocessing inside: {base}")

    # Each folder like B, V, R, ...
    letter_folders = sorted([f for f in base.iterdir() if f.is_dir()])

    for lf in letter_folders:
        print(f"\n Processing letter folder: {lf.name}")

        # 12 subfolders (Ba, Bai, Bau...) under B / V / R...
        subfolders = sorted([s for s in lf.iterdir() if s.is_dir()])

        for sub in subfolders:
            print(f"    Subfolder: {sub.name}")

            # Two PNGs per subfolder
            images = sorted([p for p in sub.glob("*.png")])

            for img_path in images:
                print(f"       Processing: {img_path.name}")

                img = cv2.imread(str(img_path))
                if img is None:
                    print("       Couldn't read image, skipping.")
                    continue

                processed = preprocess_image(img)

                # Save back (overwrite original)
                processed_uint8 = (processed * 255).astype(np.uint8)
                cv2.imwrite(str(img_path), processed_uint8)

    print("\n All images preprocessed successfully!")


if __name__ == "__main__":
    preprocess_all_modi_images()
