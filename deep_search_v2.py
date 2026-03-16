
import chromadb
from chromadb.utils import embedding_functions

db_path = "C:/code/metis/chroma_db"
client = chromadb.PersistentClient(path=db_path)
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_collection(name="metis_memory", embedding_function=embedding_function)

queries = {
    "ippokampos_indexes": "Firestore composite indexes trainerId traineeId startTime fix",
    "lawyer_anywhere_security": "Lawyer Anywhere security rules database protection trainee privacy",
    "orion_website_tech": "Orion Website technical features presentation platform overview"
}

with open("search_results.txt", "w", encoding="utf-8") as f:
    for key, q in queries.items():
        f.write(f"\n=== KEY: {key} ===\n")
        results = collection.query(query_texts=[q], n_results=5)
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            f.write(f"SOURCE: {meta.get('path', 'N/A')}\n")
            f.write(f"CONTENT: {doc}\n")
            f.write("-" * 40 + "\n")
