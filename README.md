# metis-memory-extension
"Metis: The Long-Term Memory for AI Agents"

Metis is a local, persistent memory module designed to bridge the gap between AI agent sessions. Developed by Orion Intelligence, it enables agents to retain context, recall previous debugging sessions, and maintain project-specific knowledge without cloud dependency.

Key Technical Highlights:

Local-First RAG: Built on ChromaDB for 100% data privacy and zero API costs for storage.

High-Speed Retrieval: Optimized with HNSW indexing and Cosine similarity, achieving an average latency of 14.83ms.

Language-Aware Intelligence: Features adaptive top-k retrieval based on query language detection (English/Greek).

Privacy-Centric: Uses local sentence-transformers for embeddings, ensuring no sensitive code leaves your machine.
