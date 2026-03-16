import os
import subprocess
import shutil
import sys
import time

def run_command(command, cwd=None):
    print(f"Running: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=cwd)
    for line in process.stdout:
        print(line, end="")
    process.wait()
    return process.returncode

def safe_rmtree(path):
    if not os.path.exists(path):
        return
    for i in range(5):
        try:
            shutil.rmtree(path)
            return
        except Exception as e:
            print(f"Attempt {i+1} to delete {path} failed: {e}")
            time.sleep(2)
    print(f"Failed to delete {path} after 5 attempts.")

def main():
    project_dir = os.getcwd()
    dist_dir = os.path.join(project_dir, "dist")
    build_dir = os.path.join(project_dir, "build")

    # 1. Clean previous builds
    print("Cleaning old build and dist directories...")
    safe_rmtree(dist_dir)
    safe_rmtree(build_dir)

    # 2. Get dependency paths
    try:
        import streamlit
        import chromadb
        st_path = os.path.dirname(streamlit.__file__)
        ch_path = os.path.dirname(chromadb.__file__)
    except ImportError as e:
        print(f"Required module missing: {e}")
        return
    
    print(f"Streamlit path: {st_path}")
    print(f"ChromaDB path: {ch_path}")

    # 3. Run PyInstaller
    spec_file = "Metis Intelligence.spec"
    
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-
import os
import streamlit
import chromadb

st_path = os.path.dirname(streamlit.__file__)
ch_path = os.path.dirname(chromadb.__file__)

block_cipher = None

a = Analysis(
    ['run_metis.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('metis_app.py', '.'),
        ('memory_manager.py', '.'),
        ('ingest_project.py', '.'),
        (os.path.join(st_path, 'static'), 'streamlit/static'),
        (os.path.join(st_path, 'runtime'), 'streamlit/runtime'),
        (ch_path, 'chromadb'),
    ],
    hiddenimports=[
        'streamlit',
        'chromadb',
        'sentence_transformers',
        'tqdm',
        'numpy',
        'pandas',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Metis Intelligence',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='orion_logo.ico'
)
"""
    with open(spec_file, "w", encoding='utf-8') as f:
        f.write(spec_content)

    print(f"Updated {spec_file}")
    
    # 4. Execute PyInstaller
    # FIXED: Just use the variable directly in the string without double braces
    cmd = "pyinstaller --noconfirm \"" + spec_file + "\""
    ret = run_command(cmd)

    if ret == 0:
        # 5. Verification
        exe_path = os.path.join(dist_dir, "Metis Intelligence.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"Build successful! EXE size: {size_MB:.2f} MB")
        else:
            print("Build FAILED! EXE not found in dist/.")
    else:
        print(f"PyInstaller failed with return code {ret}")

if __name__ == "__main__":
    main()
