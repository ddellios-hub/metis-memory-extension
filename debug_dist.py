import sys
import os

def main():
    with open("dist_debug.txt", "w") as f:
        f.write(f"Python version: {sys.version}\n")
        f.write(f"Executable: {sys.executable}\n")
        f.write(f"Prefix: {sys.prefix}\n")
        f.write(f"Base Prefix: {getattr(sys, 'base_prefix', 'N/A')}\n")
        f.write(f"Path: {sys.path}\n")
        f.write(f"MEIPASS: {getattr(sys, '_MEIPASS', 'N/A')}\n")
        try:
            import streamlit
            f.write(f"Streamlit version: {streamlit.__version__}\n")
        except Exception as e:
            f.write(f"Streamlit import failed: {e}\n")
            
        try:
            import chromadb
            f.write("ChromaDB imported successfully\n")
        except Exception as e:
            f.write(f"ChromaDB import failed: {e}\n")

if __name__ == "__main__":
    main()
