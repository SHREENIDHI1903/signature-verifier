import os

def rename_images(folder_path, prefix="sign"):
    files = sorted(os.listdir(folder_path))
    for i, filename in enumerate(files, start=1):
        ext = os.path.splitext(filename)[-1]
        new_name = f"{prefix}{i}{ext}"
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed {filename} → {new_name}")

# Example usage:
#rename_images("dataset/genuine")  # Change path as needed
#rename_images("dataset/forged")