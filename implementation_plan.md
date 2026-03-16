# Persistent Long-Term Memory Module Plan

The goal is to provide a local, persistent memory system for the Orion Intelligence agent using a Vector Database.

## User Review Required

> [!IMPORTANT]
> I recommend using **ChromaDB** for the vector database and **sentence-transformers** for embeddings. This combination allows for a **fully local, 100% free** setup without requiring cloud API keys.

## Proposed Changes

### Memory Module (`C:/code/orion_memory`)

#### [NEW] [README.md](file:///C:/code/orion_memory/README.md)
Documentation and setup instructions.

#### [NEW] [memory_manager.py](file:///C:/code/orion_memory/memory_manager.py)
The core logic for embedding, storing, and retrieving information.

#### [NEW] [memory_log.json](file:///C:/code/orion_memory/memory_log.json)
Metadata storage for tracking sessions and file ingestion.

#### [NEW] [requirements.txt](file:///C:/code/orion_memory/requirements.txt)
Dependency list (`chromadb`, `sentence-transformers`, `tqdm`).

## Verification Plan

### Automated Tests
- Run a test script to ingest a sample code file and a text instruction.
- Perform a retrieval query to see if the most relevant chunk is returned correctly.

### Manual Verification
- Check if `memory_log.json` is updated after ingestion.
- Verify the `chroma_db` folder is created and populated.
