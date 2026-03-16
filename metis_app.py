import streamlit as st
from memory_manager import MetisMemoryManager
import os
import subprocess
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Metis Intelligence",
    page_icon="🤖",
    layout="wide"
)

# Initialize Memory Manager
@st.cache_resource
def get_manager():
    return MetisMemoryManager()

manager = get_manager()

# Sidebar
with st.sidebar:
    st.title("🤖 Metis Intelligence")
    st.markdown("---")
    
    st.subheader("Memory Management")
    if st.button("🔄 Update Memory (Ingest)"):
        with st.status("Ingesting project data...", expanded=True) as status:
            try:
                # Run the ingestion script
                proc = subprocess.run(["python", "ingest_project.py"], capture_output=True, text=True)
                st.code(proc.stdout)
                if proc.returncode == 0:
                    status.update(label="Ingestion Complete!", state="complete")
                    st.success("Memory updated successfully.")
                else:
                    status.update(label="Ingestion Failed", state="error")
                    st.error(proc.stderr)
            except Exception as e:
                st.error(f"Error: {e}")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("---")
    st.caption(f"DB Path: {manager.db_path}")
    try:
        count = manager.collection.count()
        st.info(f"Memory Chunks: {count}")
    except:
        st.warning("DB Connection issue.")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask Metis anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Search memory for context
    with st.chat_message("assistant"):
        with st.spinner("Searching memory..."):
            results = manager.search(prompt, n_results=5)
            
            response = "I searched my memory for you. Here is what I found:\n\n"
            if results and 'documents' in results and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    doc = results['documents'][0][i]
                    meta = results['metadatas'][0][i]
                    source = meta.get('path', meta.get('category', 'System'))
                    response += f"**Source:** `{os.path.basename(source)}`  \n"
                    response += f"{doc[:300]}...  \n\n"
            else:
                response = "I couldn't find anything directly related to that in my memory."
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
