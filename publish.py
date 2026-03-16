import zipfile
import os
import json

def package_extension():
    print("--- 📦 Metis Extension Publisher ---")
    
    # Files to include in the package
    files_to_include = [
        "manifest.json",
        "extension_entry.py",
        "memory_manager.py"
    ]
    
    # Check if all files exist
    for f in files_to_include:
        if not os.path.exists(f):
            print(f"❌ Error: Required file {f} missing.")
            return

    # Load version from manifest
    with open("manifest.json", "r") as f:
        manifest = json.load(f)
        version = manifest.get("version", "1.0.0")
    
    package_name = f"metis_memory_v{version}.zip"
    
    print(f"Packaging version {version} into {package_name}...")
    
    with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_include:
            zipf.write(file)
            print(f"  + Added {file}")
            
    print(f"✅ Packaging complete: {package_name}")
    print("\nNext Steps:")
    print(f"1. Open Terminal")
    print(f"2. Run: ag-registry submit ./{package_name}")

if __name__ == "__main__":
    package_extension()
