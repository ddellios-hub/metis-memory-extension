
import chromadb
from chromadb.utils import embedding_functions

db_path = "C:/code/metis/chroma_db"
client = chromadb.PersistentClient(path=db_path)
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collections = client.list_collections()
print(f"Collections: {[c.name for c in collections]}")

collection = client.get_collection(name="metis_memory", embedding_function=embedding_function)
count = collection.count()
print(f"Items in 'metis_memory': {count}")

if count > 0:
    peek = collection.peek(limit=5)
    print("Peek at data:")
    for i in range(len(peek['documents'])):
        print(f" - {peek['metadatas'][i].get('path', 'No Path')}")
