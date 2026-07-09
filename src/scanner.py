import os
import shutil
from src.database import DatabaseManager
from src.deduplicator import Deduplicator
from src.categorizer import Categorizer

class DocumentScanner:
    
    def __init__(self, db_manager: DatabaseManager, vault_dir: str = "data/Organized_Data", delete_originals: bool = False):
        self.db = db_manager
        self.vault_dir = vault_dir
        self.delete_originals = delete_originals

    def scan_directory(self, target_dir: str):
        print(f"Starting scan of: {target_dir}")
        files_found = 0
        duplicates_skipped = 0
        added_to_db = 0

        for root, _, files in os.walk(target_dir):
            for filename in files:
                if filename.startswith('.') or "data" in root.split(os.sep):
                    continue
                    
                file_path = os.path.join(root, filename)
                files_found += 1
                
                try:
                    file_size = os.path.getsize(file_path)
                    file_hash = Deduplicator.compute_hash(file_path)
                    
                    if not file_hash:
                        continue

                    if self.db.is_duplicate(file_hash):
                        duplicates_skipped += 1
                        continue

                    category = Categorizer.categorize(filename)
                    
                    # Compute destination path in vault
                    dest_dir = os.path.join(self.vault_dir, category)
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    dest_path = os.path.join(dest_dir, filename)
                    new_filename = filename
                    
                    # Only append hash suffix if a file with this name already exists in target category
                    if os.path.exists(dest_path):
                        name, ext = os.path.splitext(filename)
                        new_filename = f"{name}_{file_hash[:6]}{ext}"
                        dest_path = os.path.join(dest_dir, new_filename)
                    
                    # Clean slashes to be consistent (forward slashes)
                    dest_path = os.path.normpath(dest_path).replace('\\', '/')

                    # Move or copy the file
                    if self.delete_originals:
                        shutil.move(file_path, dest_path)
                    else:
                        shutil.copy2(file_path, dest_path)

                    inserted = self.db.insert_document(
                        filename=new_filename,
                        original_path=dest_path,
                        file_hash=file_hash,
                        category=category,
                        file_size=file_size
                    )
                    
                    if inserted:
                        added_to_db += 1
                    else:
                        # Clean up if DB insertion failed (should be rare)
                        if os.path.exists(dest_path) and not self.delete_originals:
                            os.remove(dest_path)
                        
                except Exception as e:
                    print(f"Failed processing {file_path}: {e}")

        # Post-scan cleanup of empty directories if moving/deleting originals
        if self.delete_originals and os.path.exists(target_dir):
            for root, dirs, files in os.walk(target_dir, topdown=False):
                for dirname in dirs:
                    dir_path = os.path.join(root, dirname)
                    try:
                        if os.path.exists(dir_path) and not os.listdir(dir_path):
                            os.rmdir(dir_path)
                    except Exception as e:
                        print(f"Failed to delete empty directory {dir_path}: {e}")
            
            # Clean up the top-level directory if it's now completely empty
            try:
                if not os.listdir(target_dir):
                    os.rmdir(target_dir)
            except Exception as e:
                print(f"Failed to delete top-level directory {target_dir}: {e}")

        print("\n--- Scan Summary ---")
        print(f"Total Files Encountered: {files_found}")
        print(f"Duplicates Skipped:      {duplicates_skipped}")
        print(f"New Documents Added:     {added_to_db}")
        print("--------------------\n")
