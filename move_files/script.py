import os
import shutil

# Get directories from environment variables
downloads_folder = os.getenv('DOWNLOADS_FOLDER')
destination_base = os.getenv('DESTINATION_BASE')

# Define folder structure
folders = {
    "PDF": [".pdf"],
    "Torrents": [".torrent"],
    "Installers": [".exe"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "ZIP": [".rar", ".zip"],
    "Powerpoint" : [".pptx", ".ppt"]
}

# Make sure destination folders exist
for folder in folders.keys():
    os.makedirs(os.path.join(destination_base, folder), exist_ok=True)

# Function to move files to appropriate folders
def move_files():
    for filename in os.listdir(downloads_folder):
        file_path = os.path.join(downloads_folder, filename)
        if os.path.isfile(file_path):
            moved = False
            for folder, extensions in folders.items():
                if filename.lower().endswith(tuple(extensions)):
                    destination_folder = os.path.join(destination_base, folder)
                    shutil.move(file_path, destination_folder)
                    print(f"Moved: {filename} to {folder}")
                    moved = True
                    break
            if not moved:
                print(f"Skipped: {filename} (No matching extension)")

# Run the function to move files
move_files()
