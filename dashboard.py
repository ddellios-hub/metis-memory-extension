import streamlit as st
from memory_manager import MetisMemoryManager
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Metis - Memory Dashboard",
    page_icon="🏛️",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00d4ff;
        margin-bottom: 0.5rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #1a1c24;
        border: 1px solid #333;
        margin-bottom: 2rem;
    }
    .memory-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #1a1c24;
        border: 1px solid #333;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    .memory-card:hover {
        border-color: #00d4ff;
        transform: translateY(-2px);
    }
    .metadata-tag {
        font-size: 0.8rem;
        color: #888;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Memory Manager
@st.cache_resource
def get_manager():
    return MetisMemoryManager()

manager = get_manager()

# Sidebar - Status & Manual Entry
with st.sidebar:
    st.markdown("<div class='main-header'>Metis AI</div>", unsafe_allow_html=True)
    st.write("Long-Term Memory Interface")
    
    st.divider()
    
    # Status Panel
    st.subheader("📊 Status")
    try:
        count = manager.collection.count()
        st.success(f"Connection: Active")
        st.info(f"Memory Chunks: {count}")
    except Exception as e:
        st.error(f"Status: Error - {e}")

    st.divider()
    
    # Manual Entry
    st.subheader("📝 Add Manual Entry")
    with st.form("manual_entry", clear_on_submit=True):
        new_text = st.text_area("Content", placeholder="Enter new information to store...")
        category = st.selectbox("Category", ["Strategy", "Code Snippet", "Bug Fix", "Instructions", "General"])
        submitted = st.form_submit_button("Store in Memory")
        
        if submitted and new_text:
            metadata = {
                "source": "manual_entry",
                "category": category,
                "timestamp": datetime.now().isoformat()
            }
            manager.ingest_text(new_text, metadata)
            st.toast("Stored successfully! ✨")
            st.rerun()

# Main Content
st.markdown("<h1 class='main-header'>🏛️ Metis Memory Dashboard</h1>", unsafe_allow_html=True)

# Tabs
tab_search, tab_browser = st.tabs(["🔍 Search", "📂 Browser"])

with tab_search:
    query = st.text_input("", placeholder="Search anything... (e.g., 'indexes', 'ippokampos', 'sessions')")
    
    if query:
        results = manager.search(query, n_results=10)
        
        if results and 'documents' in results and results['documents'][0]:
            st.write(f"Found {len(results['documents'][0])} relevant entries:")
            for i in range(len(results['documents'][0])):
                doc = results['documents'][0][i]
                meta = results['metadatas'][0][i]
                
                with st.container():
                    st.markdown(f"""
                    <div class='memory-card'>
                        <div class='metadata-tag'>{meta.get('timestamp', 'Unknown Time')} | {meta.get('path', meta.get('category', 'Generic'))}</div>
                        <div style='font-family: monospace; white-space: pre-wrap;'>{doc[:500]}{'...' if len(doc) > 500 else ''}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No matches found.")

with tab_browser:
    st.subheader("All Memory Chunks")
    
    # ChromaDB common pattern to get all items: query with no condition if supported, 
    # but PersistentClient.peek is often easier for local browsing.
    try:
        data = manager.collection.get() # Get all
        if data and 'documents' in data:
            df_data = []
            for i in range(len(data['documents'])):
                doc = data['documents'][i]
                meta = data['metadatas'][i]
                df_data.append({
                    "ID": data['ids'][i],
                    "Metadata": meta.get('path', meta.get('category', 'Generic')),
                    "Snippet": doc[:100] + "..." if len(doc) > 100 else doc
                })
            
            st.dataframe(pd.DataFrame(df_data), use_container_width=True)
        else:
            st.write("Memory is currently empty.")
    except Exception as e:
        st.error(f"Error loading browser: {e}")

st.divider()
st.caption("Powered by ChromaDB & Sentence Transformers | Metis 2026")
