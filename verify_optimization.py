import time
from memory_manager import MetisMemoryManager

def verify_optimization():
    manager = MetisMemoryManager()
    
    print("--- 🔬 Verifying Memory Retrieval Optimization ---")
    
    # 1. Test Language Detection
    test_queries = {
        "What is the capital of France?": True,
        "Ποια είναι η πρωτεύουσα της Γαλλίας;": False,
        "How to fix ChromaDB packaging?": True,
        "Διόρθωση των σφαλμάτων στο Ippokampos": False,
        "Mixed query: Hello Γεια σας": False # Should detect Greek
    }
    
    print("\n[1] Testing Language Detection (_is_english):")
    for q, expected in test_queries.items():
        is_eng = manager._is_english(q)
        status = "✅" if is_eng == expected else "❌"
        print(f" {status} Query: '{q}' -> English={is_eng}")

    # 2. Test Adaptive top-k (n_results)
    print("\n[2] Testing Adaptive top-k (search method):")
    n_requested = 10
    
    # English Query
    print(f" Running English query (Requested n_results={n_requested})...")
    results_en = manager.search("ChromaDB index optimization", n_results=n_requested)
    n_returned_en = len(results_en['documents'][0]) if results_en['documents'] else 0
    print(f" -> Returned {n_returned_en} results (Expected <= {n_requested // 2})")

    # Greek Query
    print(f" Running Greek query (Requested n_results={n_requested})...")
    results_gr = manager.search("Βελτιστοποίηση ευρετηρίου ChromaDB", n_results=n_requested)
    n_returned_gr = len(results_gr['documents'][0]) if results_gr['documents'] else 0
    print(f" -> Returned {n_returned_gr} results (Expected <= {n_requested})")

    # 3. Latency Measurement
    print("\n[3] Latency Comparison (Average over 5 runs):")
    
    queries_en = [
        "How to use Metis?",
        "Retain memory settings",
        "ChromaDB configuration",
        "Python script optimization",
        "Vector database speed"
    ]
    
    queries_gr = [
        "Πώς χρησιμοποιείται ο Metis;",
        "Ρυθμίσεις διατήρησης μνήμης",
        "Παραμετροποίηση ChromaDB",
        "Βελτιστοποίηση κώδικα Python",
        "Ταχύτητα βάσης διανυσμάτων"
    ]
    
    def measure_avg_latency(queries):
        total_time = 0
        for q in queries:
            start = time.time()
            manager.search(q, n_results=10)
            total_time += (time.time() - start)
        return (total_time / len(queries)) * 1000 # Return in ms

    avg_en = measure_avg_latency(queries_en)
    avg_gr = measure_avg_latency(queries_gr)
    
    print(f" Average English Latency: {avg_en:.2f} ms")
    print(f" Average Greek Latency:   {avg_gr:.2f} ms")
    
    diff = avg_gr - avg_en
    if diff > 0:
        print(f" ✨ English queries are {diff:.2f} ms faster ({ (diff/avg_gr)*100:.1f}% reduction)")
    else:
        print(f" ℹ️ Latency difference is negligible or skewed by small dataset.")

    # 4. Collection Metadata Verification
    print("\n[4] Collection Settings Verification:")
    try:
        # Re-fetch collection to see if metadata is applied
        collection = manager.client.get_collection(name="metis_memory")
        metadata = collection.metadata or {}
        print(f" Metadata: {metadata}")
            
        if 'hnsw:search_ef' in metadata:
            print(f" ✅ HNSW Search EF is set to {metadata['hnsw:search_ef']}")
        else:
            print(" ❌ HNSW Search EF is NOT set.")
            
        if 'hnsw:space' in metadata:
            print(f" ℹ️ HNSW Space is set to '{metadata['hnsw:space']}' (Original setting)")
    except Exception as e:
        print(f" ❌ Could not verify metadata: {e}")

if __name__ == "__main__":
    verify_optimization()
