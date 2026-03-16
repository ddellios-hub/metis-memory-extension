import os
from memory_manager import MetisMemoryManager
import os
from tqdm import tqdm

def ingest_directory(directory_path, manager):
    # Skip directories that are typically not source code or massive
    skip_dirs = {'.git', '.venv', 'node_modules', 'build', 'ios', 'android', 'chroma_db'}
    
    for root, dirs, files in os.walk(directory_path):
        # In-place modification of dirs to skip certain folders
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            # Basic skip for binary/massive files if needed
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.pdf', '.exe', '.pyc')):
                continue
            
            try:
                manager.ingest_file(file_path)
            except Exception as e:
                print(f"Error ingesting {file_path}: {e}")

if __name__ == "__main__":
    manager = MetisMemoryManager()
    project_path = r"C:\code\Website\Orion Intelligence\orion-site"
    print(f"Starting ingestion for {project_path}...")
    ingest_directory(project_path, manager)
    print("Ingestion complete.")
