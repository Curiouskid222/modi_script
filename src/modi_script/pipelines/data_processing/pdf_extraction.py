import os
import shutil
import platform
from pathlib import Path
from pdf2image import convert_from_path


def get_google_drive_path():
    """Locate Google Drive folder based on OS."""
    system = platform.system()

    if system == "Windows":
        possible_paths = [
            Path("G:/My Drive"),
            Path("G:/MyDrive"),
            Path(f"C:/Users/{os.getenv('USERNAME')}/Google Drive"),
        ]
    elif system == "Darwin":  # macOS
        possible_paths = [
            Path("/Volumes/GoogleDrive/My Drive"),
            Path(f"/Users/{os.getenv('USER')}/Library/CloudStorage/GoogleDrive"),
        ]
    else:  # Linux or others
        possible_paths = [
            Path.home() / "GoogleDrive",
            Path("/mnt/GoogleDrive/My Drive"),
        ]

    for p in possible_paths:
        if p.exists():
            return p

    raise FileNotFoundError(
        "⚠️ Could not find your Google Drive folder. Make sure Google Drive for Desktop is installed and synced locally."
    )


def process_pdfs(local_folder):
    """Deletes extra subfolders, extracts images from PDFs, and moves them."""
    drive_root = get_google_drive_path()
    target_root = drive_root / "modi-script" / "data" / "01_raw" / "chars"

    local_folder = Path(local_folder)
    pdf_files = list(local_folder.glob("*.pdf"))

    if not pdf_files:
        print("⚠️ No PDF files found in the given folder.")
        return

    for pdf_path in pdf_files:
        base_name = pdf_path.stem
        char_folder = target_root / base_name

        if not char_folder.exists():
            print(f"⚠️ Skipped {base_name}: main folder not found.")
            continue

        print(f"\n📘 Processing {pdf_path.name} → {char_folder}")

        # Step 1: Delete extra subfolders (keep only 10)
        subfolders = sorted([f for f in char_folder.iterdir() if f.is_dir()])
        if len(subfolders) > 10:
            for extra in subfolders[10:]:
                shutil.rmtree(extra)
                print(f"🗑️ Deleted extra subfolder: {extra.name}")

        # Step 2: Extract images from PDF
        pages = convert_from_path(pdf_path, dpi=300)
        subfolders = sorted([f for f in char_folder.iterdir() if f.is_dir()])

        # Step 3: Move images into the 10 subfolders
        for i, (page, subfolder) in enumerate(zip(pages, subfolders)):
            img_filename = f"{base_name}_{i+1}.png"
            img_path = subfolder / img_filename
            page.save(img_path, "PNG")
            print(f"✅ Saved page {i+1} → {img_path}")

        # Step 4: Move original PDF to its main folder
        dest_pdf = char_folder / pdf_path.name
        shutil.move(str(pdf_path), str(dest_pdf))
        print(f"📦 Moved original PDF to {char_folder}\n")


if __name__ == "__main__":
    local_folder = r"C:\Users\ACER\Downloads\barakhadi"  # 🔹 your local folder path
    process_pdfs(local_folder)
