import os
import json
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import uuid
from datetime import datetime
import re

class MetisMemoryManager:
    def __init__(self, db_path="C:/code/metis/chroma_db", log_path="C:/code/metis/memory_log.json"):
        self.db_path = db_path
        self.log_path = log_path
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # Local Embedding Function using sentence-transformers
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="metis_memory",
            embedding_function=self.embedding_function
        )
        # Ensure metadata is applied (in case collection already existed)
        self.collection.modify(
            metadata={
                "hnsw:search_ef": 100
            }
        )
        
        # Initialize memory_log
        if not os.path.exists(self.log_path):
            with open(self.log_path, 'w', encoding='utf-8') as f:
                json.dump({"ingested_files": [], "sessions": []}, f, indent=4)

    def ingest_text(self, text, metadata=None):
        """Adds a piece of text to the vector database."""
        id_str = str(uuid.uuid4())
        self.collection.add(
            documents=[text],
            metadatas=[metadata] if metadata else [{}],
            ids=[id_str]
        )
        self._update_log("text_ingestion", {"id": id_str, "timestamp": datetime.now().isoformat()})
        return id_str

    def ingest_file(self, file_path):
        """Reads a file and stores its content."""
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found.")
            return None
            
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # In a real scenario, we might want to chunk long files
        id_str = str(uuid.uuid4())
        self.collection.add(
            documents=[content],
            metadatas=[{"path": file_path, "timestamp": datetime.now().isoformat()}],
            ids=[id_str]
        )
        
        self._update_log("file_ingestion", {"path": file_path, "id": id_str})
        return id_str

    def _is_english(self, query):
        """Detects if a query is primarily English (non-Greek)."""
        # Simple detection: if it doesn't contain Greek characters, treat as English
        greek_pattern = re.compile(r'[\u0370-\u03ff\u1f00-\u1fff]')
        return not bool(greek_pattern.search(query))

    def search(self, query, n_results=3):
        """Searches for relevant information in the memory with adaptive top-k."""
        # Use smaller top-k for English queries to reduce latency
        if self._is_english(query):
            final_n = max(1, n_results // 2)
        else:
            final_n = n_results

        results = self.collection.query(
            query_texts=[query],
            n_results=final_n
        )
        return results

    def _update_log(self, action, details):
        with open(self.log_path, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            if action == "file_ingestion":
                data["ingested_files"].append(details)
            elif action == "text_ingestion":
                if "texts" not in data: data["texts"] = []
                data["texts"].append(details)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

if __name__ == "__main__":
    # Example usage
    manager = MetisMemoryManager()
    print("Memory Manager initialized.")
