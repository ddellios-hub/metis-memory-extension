import os
from memory_manager import MetisMemoryManager
from datetime import datetime

# Global instance for the session
_memory_manager = None

def on_session_start():
    """Hook triggered when a new Antigravity session starts."""
    global _memory_manager
    print(f"[{datetime.now().isoformat()}] Metis Persistent Memory: Initializing session...")
    _memory_manager = MetisMemoryManager()
    return True

def provide_context(query, n_results=3):
    """
    Antigravity Context Provider hook.
    Searches memory for relevant snippets and returns them for system prompt injection.
    """
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = MetisMemoryManager()
        
    print(f"[{datetime.now().isoformat()}] Metis: Retrieving context for query: '{query[:50]}...'")
    
    results = _memory_manager.search(query, n_results=n_results)
    
    context_output = ""
    if results and 'documents' in results and results['documents'][0]:
        context_output = "\n### RELEVANT MEMORIES (Metis Intelligence):\n"
        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            source = meta.get('path', meta.get('category', 'Stored Information'))
            
            context_output += f"--- Source: {os.path.basename(source)} ---\n"
            context_output += f"{doc}\n\n"
        context_output += "### END MEMORIES\n"
    
    return context_output

if __name__ == "__main__":
    # Internal test/init if run directly
    on_session_start()
    print("Entry point initialized.")
