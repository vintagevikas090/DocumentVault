import csv
import zipfile
import os
from src.database import DatabaseManager
from datetime import datetime

class Exporter:
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def export_inventory_csv(self, output_file: str = "document_inventory.csv") -> str:
        documents = self.db.get_all_documents()
        
        if not documents:
            return "No documents in database to export."

        headers = documents[0].keys()

        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(documents)
            return f"Inventory successfully exported to {output_file}"
        except Exception as e:
            return f"Failed to export inventory: {e}"

    def create_database_backup(self, backup_dir: str = "data/backups") -> str:
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        db_path = self.db.db_path
        
        if not os.path.exists(db_path):
            return "Database file not found. Nothing to backup."

        zip_filename = os.path.join(backup_dir, f"doc_inventory_backup_{timestamp}.zip")
        
        try:
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(db_path, os.path.basename(db_path))
            return f"Database backed up to {zip_filename}"
        except Exception as e:
            return f"Failed to create backup: {e}"

    def get_database_backup_bytes(self) -> bytes:
        import io
        db_path = self.db.db_path
        if not os.path.exists(db_path):
            return b""
            
        buffer = io.BytesIO()
        try:
            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(db_path, os.path.basename(db_path))
            return buffer.getvalue()
        except Exception as e:
            print(f"Failed to create in-memory backup bytes: {e}")
            return b""

