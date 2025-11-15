import os
import json

def get_pdf_list(folder_path):
    """
    Reads all PDF files in the given folder and returns a list of lowercase filenames
    without extensions.

    Parameters
    ----------
    folder_path : str
        Path to the folder containing PDF files.

    Returns
    -------
    list
        Sorted list of lowercase PDF file names (without extensions).
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"The provided path does not exist or is not a directory: {folder_path}")

    pdf_list = []

    for file in os.listdir(folder_path):
        if file.lower().endswith('.pdf'):
            name_without_ext = os.path.splitext(file)[0].lower()
            pdf_list.append(name_without_ext)

    return sorted(pdf_list)


if __name__ == "__main__":
    # Hardcode or modify this path as needed
    folder_path = r"C:\Users\ACER\Downloads\barakhadi"

    pdf_files = get_pdf_list(folder_path)

    # Display in console
    print("PDF names list:\n", pdf_files)

    # Automatically save as JSON (no user input)s
    output_path = os.path.join(folder_path, "pdf_files_list.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(pdf_files, f, indent=4)

    print(f"\nList saved successfully to: {output_path}")
