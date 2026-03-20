from PIL import Image, ImageOps, ImageEnhance
import os
from tqdm import tqdm

# 1. Setup folders
input_folder = r"C:\Users\nansh\Documents\Python\fantasy_herd\img"
output_folder = r"C:\Users\nansh\Documents\Python\fantasy_herd\grey"

# 2. Get list of files to process
files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

print(f"Converting {len(files)} images to grayscale...")

# 3. Process with Progress Bar
# desc sets the label, unit sets the counter type
for filename in tqdm(files, desc="Processing Cards", unit="card"):
    try:
        img_path = os.path.join(input_folder, filename)
        with Image.open(img_path) as img:
            # Convert to Grayscale
            grayscale_img = ImageOps.grayscale(img)
            
            # Boost contrast (optional, but highly recommended for OCR)
            enhancer = ImageEnhance.Contrast(grayscale_img)
            grayscale_img = enhancer.enhance(1.5)
            
            # Save to the new folder
            grayscale_img.save(os.path.join(output_folder, filename))
    except Exception as e:
        print(f"\nError processing {filename}: {e}")

print(f"\nSuccess! All images saved to '{output_folder}'.")