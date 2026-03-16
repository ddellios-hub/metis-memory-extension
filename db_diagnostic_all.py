
import chromadb
from chromadb.utils import embedding_functions

db_path = "C:/code/metis/chroma_db"
client = chromadb.PersistentClient(path=db_path)
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collections = client.list_collections()
for coll_meta in collections:
    name = coll_meta.name
    collection = client.get_collection(name=name, embedding_function=embedding_function)
    count = collection.count()
    print(f"Collection '{name}': {count} items")
    if count > 0:
        peek = collection.peek(limit=3)
        print(f"  Peek: {[m.get('path', m.get('category', 'N/A')) for m in peek['metadatas']]}")
