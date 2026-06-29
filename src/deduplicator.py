import hashlib

class Deduplicator:
    
    @staticmethod
    def compute_hash(file_path: str, chunk_size: int = 8192) -> str:
        hasher = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(chunk_size):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            print(f"Error reading {file_path} for hashing: {e}")
            return None
