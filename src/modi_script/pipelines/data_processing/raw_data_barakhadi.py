import os
import shutil
from pathlib import Path
import platform

def get_google_drive_path():
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
            Path(f"/Users/{os.getenv('USER')}/Library/CloudStorage/GoogleDrive")
        ]
    else:  # Linux or others
        possible_paths = [
            Path.home() / "GoogleDrive",
            Path("/mnt/GoogleDrive/My Drive")
        ]

    for p in possible_paths:
        if p.exists():
            return p

    raise FileNotFoundError(
        "⚠️ Could not find your Google Drive folder. "
        "Make sure Google Drive for Desktop is installed and synced locally."
    )


def move_pdfs_to_drive(local_folder):
    # Get synced Google Drive path
    drive_root = get_google_drive_path()
    target_root = drive_root / "modi-script" / "data" / "01_raw" / "chars"

    if not target_root.exists():
        raise FileNotFoundError(f"❌ Target folder not found: {target_root}")

    local_folder = Path(local_folder)
    pdf_files = list(local_folder.glob("*.pdf"))

    if not pdf_files:
        print("⚠️ No PDF files found in the given folder.")
        return

    for pdf in pdf_files:
        name = pdf.stem  # filename without extension
        subfolder = target_root / name

        if subfolder.exists():
            dest = subfolder / pdf.name
            shutil.move(str(pdf), str(dest))
            print(f"✅ Moved {pdf.name} → {subfolder}")
        else:
            print(f"⚠️ Skipped {pdf.name}: subfolder '{subfolder.name}' not found.")

if __name__ == "__main__":
    # change this to your local source folder
    local_folder = r"C:\Users\ACER\Downloads\barakhadi"
    move_pdfs_to_drive(local_folder)
