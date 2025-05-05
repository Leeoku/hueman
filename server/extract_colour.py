import os
import json
from collections import Counter
from PIL import Image

IMAGE_DIR = 'images'
OUTPUT_JSON = 'image_colours.json'

results = []

def get_main_color(image_path):
    with Image.open(image_path) as img:
        img = img.convert('RGBA')
        # Resize to speed up processing
        img = img.resize((100, 100))
        pixels = list(img.getdata())
        # Remove fully transparent pixels
        pixels = [p for p in pixels if p[3] > 0]
        if not pixels:
            return (0, 0, 0, 0)
        most_common = Counter(pixels).most_common(1)[0][0]
        return most_common

for filename in os.listdir(IMAGE_DIR):
    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")):
        image_path = os.path.join(IMAGE_DIR, filename)
        try:
            main_color = get_main_color(image_path)
            results.append({
                'filename': filename,
                'color': main_color
            })
        except Exception as e:
            print(f"Error processing {filename}: {e}")

with open(OUTPUT_JSON, 'w') as f:
    json.dump(results, f, indent=2)

print(f"Extracted colors for {len(results)} images. Results saved to {OUTPUT_JSON}.") 