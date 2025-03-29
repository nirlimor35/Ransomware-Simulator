import os


def find_files(target_dir, extensions=(".txt", ".docx", ".xlsx")):
    found = []
    for root, _, files in os.walk(target_dir):
        for f in files:
            if any(f.endswith(ext) for ext in extensions):
                found.append(os.path.join(root, f))
    return found
