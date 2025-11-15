import os
import platform
from pathlib import Path

# -------------------------------------------------------------
# 1. Detect OS and choose Google Drive path
# -------------------------------------------------------------
def get_google_drive_path():
    system = platform.system()

    if system == "Windows":
        # usually "My Drive" or "MyDrive" depending on locale
        possible_paths = [
            Path("G:/My Drive"),
            Path("G:/MyDrive"),
            Path("C:/Users") / os.getenv("USERNAME") / "Google Drive",
        ]
    elif system == "Darwin":  # macOS
        possible_paths = [
            Path("/Volumes/GoogleDrive/My Drive"),
            Path("/Users") / os.getenv("USER") / "Library/CloudStorage/GoogleDrive"
        ]
    else:  # Linux or others
        possible_paths = [Path.home() / "GoogleDrive", Path("/mnt/GoogleDrive/My Drive")]

    for p in possible_paths:
        if p.exists():
            return p

    raise FileNotFoundError(
        "⚠️  Could not find your Google Drive folder. "
        "Make sure Google Drive for Desktop is installed and synced locally."
    )


# -------------------------------------------------------------
# 2. Define dataset base path inside Google Drive
# -------------------------------------------------------------
drive_path = get_google_drive_path()
base_dir = drive_path / "ModiOCR" / "data" / "chars"

# -------------------------------------------------------------
# 3. Marathi alphabets
# -------------------------------------------------------------
VOWELS = ["a", "aa", "i", "ii", "u", "uu", "ru", "ruu", "e", "ai", "o", "au"]

CONSONANTS = [
    "ka","kha","ga","gha","nga",
    "cha","chha","ja","jha","nya",
    "ṭa","ṭha","ḍa","ḍha","ṇa",
    "ta","tha","da","dha","na",
    "pa","pha","ba","bha","ma",
    "ya","ra","la","va",
    "śa","ṣa","sa","ha","ḷa"
]

NUMERALS = ["0","1","2","3","4","5","6","7","8","9"]
PUNCTUATION = ["danda","double_danda"]

# -------------------------------------------------------------
# 4. Create dataset structure
# -------------------------------------------------------------
def create_dataset_structure(base_dir):
    os.makedirs(base_dir, exist_ok=True)

    # Vowels
    vowels_dir = base_dir / "vowels"
    for v in VOWELS:
        (vowels_dir / v).mkdir(parents=True, exist_ok=True)

    # Consonants with 12 barakhadi forms
    for c in CONSONANTS:
        c_dir = base_dir / c
        for i in range(1, 13):
            (c_dir / f"{c}{i}").mkdir(parents=True, exist_ok=True)

    # Numerals
    numerals_dir = base_dir / "numerals"
    for n in NUMERALS:
        (numerals_dir / n).mkdir(parents=True, exist_ok=True)

    # Punctuation
    punct_dir = base_dir / "punctuation"
    for p in PUNCTUATION:
        (punct_dir / p).mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Dataset structure created under: {base_dir}")

# -------------------------------------------------------------
# 5. Run
# -------------------------------------------------------------
if __name__ == "__main__":
    create_dataset_structure(base_dir)
