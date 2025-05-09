import os
import json
from colorthief import ColorThief

# Directory containing images
IMAGE_DIR = 'images'
OUTPUT_JSON = 'image_colors_palette.json'

results = []

for filename in os.listdir(IMAGE_DIR):
    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")):
        image_path = os.path.join(IMAGE_DIR, filename)
        try:
            color_thief = ColorThief(image_path)
            palette = color_thief.get_palette(color_count=6)  # You can adjust color_count as needed
            results.append({
                'filename': filename,
                'palette': palette
            })
        except Exception as e:
            print(f"Error processing {filename}: {e}")

with open(OUTPUT_JSON, 'w') as f:
    json.dump(results, f, indent=2)

print(f"Extracted palettes for {len(results)} images. Results saved to {OUTPUT_JSON}.") 