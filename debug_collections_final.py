
import chromadb

db_path = "C:/code/metis/chroma_db"
client = chromadb.PersistentClient(path=db_path)

for coll_meta in client.list_collections():
    name = coll_meta.name
    coll = client.get_collection(name=name)
    count = coll.count()
    print(f"COLLECTION: {name} | COUNT: {count}")
    if count > 0:
        peek = coll.peek(limit=5)
        for i, meta in enumerate(peek['metadatas']):
            print(f"  {i+1}. Path: {meta.get('path', 'N/A')} | Category: {meta.get('category', 'N/A')}")
