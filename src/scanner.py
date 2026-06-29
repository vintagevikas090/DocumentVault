import os
from src.database import DatabaseManager
from src.deduplicator import Deduplicator
from src.categorizer import Categorizer

class DocumentScanner:
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

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

                    inserted = self.db.insert_document(
                        filename=filename,
                        original_path=file_path,
                        file_hash=file_hash,
                        category=category,
                        file_size=file_size
                    )
                    
                    if inserted:
                        added_to_db += 1
                        
                except Exception as e:
                    print(f"Failed processing {file_path}: {e}")

        print("\n--- Scan Summary ---")
        print(f"Total Files Encountered: {files_found}")
        print(f"Duplicates Skipped:      {duplicates_skipped}")
        print(f"New Documents Added:     {added_to_db}")
        print("--------------------\n")
