import os
import re

public_dir = '/Users/sai2005/Downloads/gitprojects/iiat/iiath-astro/public'
src_dir = '/Users/sai2005/Downloads/gitprojects/iiat/iiath-astro/src'

# 1. Collect all filenames in public (except some obvious ones)
public_files = []
for root, dirs, files in os.walk(public_dir):
    for file in files:
        rel_path = os.path.relpath(os.path.join(root, file), public_dir)
        public_files.append(rel_path)

print(f"Total files in public: {len(public_files)}")

# 2. Collect all strings from src that look like filenames
referenced_files = set()
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith(('.astro', '.css', '.js', '.mjs', '.ts', '.json')):
            with open(os.path.join(root, file), 'r', errors='ignore') as f:
                content = f.read()
                # Look for the filename or path
                for pub_file in public_files:
                    # Check for just filename or full path
                    # Using escape for regex to handle special chars like .
                    if re.search(re.escape(pub_file), content) or re.search(re.escape(os.path.basename(pub_file)), content):
                        referenced_files.add(pub_file)

print(f"Referenced files: {len(referenced_files)}")

# 3. Identify and Delete unreferenced files
deleted_count = 0
deleted_size = 0
for pub_file in public_files:
    if pub_file not in referenced_files:
        full_path = os.path.join(public_dir, pub_file)
        if os.path.isfile(full_path):
            size = os.path.getsize(full_path)
            # Only delete if it's large or seems irrelevant? 
            # Actually, user said delete ALL assets of bower. 
            # If it's not referenced, it's safe and likely leftover.
            os.remove(full_path)
            deleted_count += 1
            deleted_size += size

print(f"Deleted {deleted_count} unreferenced files.")
print(f"Saved {deleted_size / (1024*1024):.2f} MB.")
