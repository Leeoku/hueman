import os
import json
from colorthief import ColorThief

# Directory containing images
IMAGE_DIR = 'images'
OUTPUT_JSON = 'image_colours.json'

results = []

for filename in os.listdir(IMAGE_DIR):
    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")):
        image_path = os.path.join(IMAGE_DIR, filename)
        try:
            color_thief = ColorThief(image_path)
            dominant_color = color_thief.get_color(quality=1)
            results.append({
                'filename': filename,
                'color': dominant_color
            })
        except Exception as e:
            print(f"Error processing {filename}: {e}")

with open(OUTPUT_JSON, 'w') as f:
    json.dump(results, f, indent=2)

print(f"Extracted colors for {len(results)} images. Results saved to {OUTPUT_JSON}.") 