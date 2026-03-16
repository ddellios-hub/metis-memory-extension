
import chromadb

db_path = "C:/code/metis/chroma_db"
client = chromadb.PersistentClient(path=db_path)

try:
    # Check if metis_memory exists and is empty
    try:
        metis_coll = client.get_collection("metis_memory")
        if metis_coll.count() == 0:
            print("Deleting empty 'metis_memory' collection to allow rename.")
            client.delete_collection("metis_memory")
    except:
        pass

    # Rename orion_memory to metis_memory
    print("Renaming 'orion_memory' to 'metis_memory'...")
    coll = client.get_collection("orion_memory")
    coll.modify(name="metis_memory")
    print("Rename successful.")
except Exception as e:
    print(f"Error during rename: {e}")
    print("Attempting manual migration...")
    try:
        old_coll = client.get_collection("orion_memory")
        new_coll = client.get_or_create_collection("metis_memory")
        data = old_coll.get()
        if data['ids']:
            new_coll.add(
                ids=data['ids'],
                documents=data['documents'],
                metadatas=data['metadatas']
            )
            print(f"Migrated {len(data['ids'])} items.")
    except Exception as e2:
        print(f"Migration failed: {e2}")
