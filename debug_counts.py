
import chromadb

db_path = "C:/code/metis/chroma_db"
client = chromadb.PersistentClient(path=db_path)

collections = client.list_collections()
for coll in collections:
    c = client.get_collection(name=coll.name)
    print(f"COLLECTION: {coll.name} | COUNT: {c.count()}")
