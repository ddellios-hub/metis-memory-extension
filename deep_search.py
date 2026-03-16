
import chromadb
from chromadb.utils import embedding_functions

db_path = "C:/code/metis/chroma_db"
client = chromadb.PersistentClient(path=db_path)
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_collection(name="metis_memory", embedding_function=embedding_function)

queries = [
    "Firestore Indexes Ippokampos fix trainerId traineeId",
    "Lawyer Anywhere data security isolation",
    "Orion Website technical presentation content",
    "relationship between Ippokampos and Lawyer Anywhere security"
]

for q in queries:
    print(f"\n--- QUERY: {q} ---")
    results = collection.query(query_texts=[q], n_results=3)
    for i in range(len(results['documents'][0])):
        doc = results['documents'][0][i]
        meta = results['metadatas'][0][i]
        print(f"SOURCE: {meta.get('path', meta.get('category', 'N/A'))}")
        print(f"CONTENT: {doc[:1000]}...")
        print("-" * 20)
