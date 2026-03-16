# metis-memory-extension
"Metis: The Long-Term Memory for AI Agents"

Metis is a local, persistent memory module designed to bridge the gap between AI agent sessions. Developed by Orion Intelligence, it enables agents to retain context, recall previous debugging sessions, and maintain project-specific knowledge without cloud dependency.

Key Technical Highlights:

Local-First RAG: Built on ChromaDB for 100% data privacy and zero API costs for storage.

High-Speed Retrieval: Optimized with HNSW indexing and Cosine similarity, achieving an average latency of 14.83ms.

Language-Aware Intelligence: Features adaptive top-k retrieval based on query language detection (English/Greek).

Privacy-Centric: Uses local sentence-transformers for embeddings, ensuring no sensitive code leaves your machine.
---

## ⚖️ Disclaimer & Status

**Project Status:** This project is currently in **Active Development** by **Orion Intelligence**. Features and API structures may evolve rapidly.

**Usage:** This software is provided "as is", without warranty of any kind. It is designed to run locally to ensure maximum data privacy. While it significantly improves AI agent recall, users are responsible for managing their own local data security.

**Contributions:** We welcome feedback and contributions! If you encounter any bugs or have suggestions for new features, please open an issue or submit a pull request.

**Contact:** Developed by **Dimitris** (Orion Intelligence). For business inquiries or custom AI implementations, feel free to reach out.
