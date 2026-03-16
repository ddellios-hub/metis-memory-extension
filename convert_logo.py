from PIL import Image
import os

source_path = r"C:\Code\Website\Orion Intelligence\orion-site\build\assets\orion-logo-800.png"
target_path = r"C:\code\metis\orion_logo.ico"

try:
    if not os.path.exists(source_path):
        print(f"Error: Source file not found at {source_path}")
    else:
        img = Image.open(source_path)
        # Using multiple sizes for better quality across different OS scales
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(target_path, format='ICO', sizes=icon_sizes)
        print(f"Successfully converted {source_path} to {target_path}")
except Exception as e:
    print(f"Error during conversion: {e}")
