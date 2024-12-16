import os
import shutil
import hashlib

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
    "Powerpoint": [".pptx", ".ppt"]
}
# Create destination folders if they do not exist
def create_folders():
    for folder in folders.keys():
        os.makedirs(os.path.join(destination_base, folder), exist_ok = True)

# Calculate the SHA-256 hash of a file
def calculate_hash(file_path, chunk_size=8192):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            sha256.update(chunk)
    return sha256.hexdigest()
    
# Check if the file already exists and either rename the old one or delete it
def file_exists(destination_path, file_path):
    if os.path.exists(destination_path):
        source_hash = calculate_hash(file_path)
        destination_hash = calculate_hash(destination_path)
        
        if source_hash == destination_hash:
            os.remove(file_path)
            print(f"Deleted duplicate file: {os.path.basename(file_path)}")
            return True
        else:
            old_destination_path = f"{destination_path}_old"
            os.rename(destination_path, old_destination_path)
            print(f"Renamed existing file to: {old_destination_path}")
    
    return False

# Move a file to a folder
def move_file(file_path, folder):
    destination_folder = os.path.join(destination_base, folder)
    destination_path = os.path.join(destination_folder, os.path.basename(file_path))
    
    if not file_exists(destination_path, file_path):
        shutil.move(file_path, destination_folder)
        print(f"Moved: {os.path.basename(file_path)} to {folder}")

# Process all files in the specified folder
def process_files():
    for filename in os.listdir(downloads_folder):
        file_path = os.path.join(downloads_folder, filename)
        if os.path.isfile(file_path):
            moved = False
            for folder, extensions in folders.items():
                if filename.lower().endswith(tuple(extensions)):
                    move_file(file_path, folder)
                    moved = True
                    break
            if not moved:
                print(f"Skipped: {filename} (No matching extension)")

if __name__ == "__main__":
    create_folders()
    process_files()
