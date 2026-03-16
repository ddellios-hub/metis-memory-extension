import os
import sys

# PyInstaller windowed mode fix: sys.stdout/stderr are None
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

import streamlit.web.cli as stcli
import threading
import webbrowser
import time
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def open_browser(port):
    """Wait for the server to be ready, then open the browser."""
    max_retries = 20
    for _ in range(max_retries):
        if is_port_in_use(port):
            time.sleep(1) # Small extra buffer
            webbrowser.open(f"http://localhost:{port}")
            return
        time.sleep(1)

def main():
    port = 8501
    
    # In PyInstaller, the temporary folder path is stored in _MEIPASS
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    app_script = os.path.join(base_dir, "metis_app.py")
    
    # Start the browser-opener thread
    threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    
    # Run Streamlit internally
    # This prevents the recursion/fork-bomb because it doesn't call sys.executable
    sys.argv = [
        "streamlit",
        "run",
        app_script,
        "--server.port", str(port),
        "--server.headless", "true",
        "--global.developmentMode", "false",
    ]
    
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()
