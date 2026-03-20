import pytesseract
from PIL import Image
import pandas as pd
import os
from tqdm import tqdm
import re

# 1. Exact Coordinates from image (Left, Top, Right, Bottom)
zones = {        
    "Milk_Volume_KL": (91, 732, 230, 788),  # Your MV coordinates
    "Protein_KG": (86, 821, 251, 877),     # Your Protein coordinates
    "Production_Worth": (74, 913, 215, 972),# Your Perf coordinates
    "Price_M": (474, 122, 573, 183),        # Your Money coordinates
    "Rating": (470, 289, 555, 363),         # Your Rating coordinates
    "Tag_No": (466, 424, 578, 533)          # Your No coordinates
}

def clean_text(text, field):
    """Removes units and non-numeric junk for specific fields"""
    if not text: return ""
    # Remove letters/units but keep numbers and symbols like '.' or '-'
    if field in ["Name", "Rating"]:
        return text
    cleaned = re.sub(r'[a-zA-Z]+', '', text).strip()
    return cleaned

# 2. Setup folders
input_folder = r"C:\Users\nansh\Documents\Python\fantasy_herd\grey"
files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
all_results = []

print(f"Extracting data from {len(files)} cards using custom coordinates...")

# 3. Process Loop
for filename in tqdm(files[:4], desc="Processing", unit="card"):
    img_path = os.path.join(input_folder, filename)
    try:
        img = Image.open(img_path)
        card_data = {"File_Name": filename}
        
        for field, coords in zones.items():
            cropped = img.crop(coords)
            config = '--psm 7' if field != "Name" else '--psm 6'
            raw_text = pytesseract.image_to_string(cropped, config=config).strip()
            
            card_data[field] = clean_text(raw_text, field)
            
        all_results.append(card_data)
    except Exception as e:
        print(f"Error on {filename}: {e}")

# 4. Save to CSV
df = pd.DataFrame(all_results)
df.to_csv(r"C:\Users\nansh\Documents\Python\fantasy_herd\data_out.csv", index=True)

print(f"\nSuccess! Data saved to 'cow_data_final_output.csv'.")