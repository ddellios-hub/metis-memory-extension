from memory_manager import MetisMemoryManager
import os

def test_memory():
    manager = MetisMemoryManager()
    
    # Ingesting multiple relevant files
    files_to_ingest = [
        r"C:\Code\Orion Finance\implementation_plan.md",
        r"C:\Code\katsilas\ippokampos_app\lib\features\admin\admin_attendance_screen.dart"
    ]
    
    for file_path in files_to_ingest:
        if os.path.exists(file_path):
            print(f"Ingesting {file_path}...")
            manager.ingest_file(file_path)
        else:
            print(f"File {file_path} not found.")

    print("\nIngestion complete.")
    
    queries = [
        "Ποιο ήταν το τελευταίο bug που συζητήσαμε;",
        "Τι αφορούσε η τελευταία διόρθωση στον κώδικα;"
    ]
    
    for query in queries:
        print(f"\nSearching for: {query}")
        results = manager.search(query)
        for i, doc in enumerate(results['documents'][0]):
            print(f"\nResult {i+1}:")
            print(doc[:300] + "...")

if __name__ == "__main__":
    test_memory()
