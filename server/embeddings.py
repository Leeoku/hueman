import numpy as np
import json
from typing import List, Tuple
from skimage.color import rgb2lab
from color_utils import hex_to_rgb

N_COLORS = 5  # Always use 5 colors per palette

def load_palettes(json_path: str):
    with open(json_path, 'r') as f:
        data = json.load(f)
    palettes = [item['palette'] for item in data if 'palette' in item]
    return palettes

def load_palettes_with_filenames(json_path: str):
    """
    Load palettes and their corresponding filenames from the JSON file.
    Returns (palettes, filenames) as lists.
    """
    with open(json_path, 'r') as f:
        data = json.load(f)
    palettes = []
    filenames = []
    for item in data:
        if 'palette' in item and 'filename' in item:
            palettes.append(item['palette'])
            filenames.append(item['filename'])
    return palettes, filenames

def rgb_palette_to_lab(palette: List[List[int]], n_colors: int = N_COLORS) -> np.ndarray:
    """
    Convert a palette (list of RGB colors) to Lab color space and flatten.
    Always use n_colors (pad with [0,0,0] or truncate as needed).
    """
    palette = (palette + [[0,0,0]] * n_colors)[:n_colors]
    arr = np.array(palette, dtype=np.float32).reshape(-1, 1, 3) / 255.0
    lab = rgb2lab(arr)
    return lab.flatten()

def build_palette_embeddings(palettes: List[List[List[int]]], output_json: str = None, n_colors: int = N_COLORS) -> np.ndarray:
    embeddings = np.array([rgb_palette_to_lab(p, n_colors) for p in palettes])
    if output_json:
        embeddings_list = embeddings.tolist()
        with open(output_json, 'w') as f:
            json.dump(embeddings_list, f)
    return embeddings

def load_embeddings(json_path: str) -> np.ndarray:
    with open(json_path, 'r') as f:
        embeddings_list = json.load(f)
    return np.array(embeddings_list)

def find_closest_palette(default_palette: List[List[int]], embeddings: np.ndarray, palettes: List[List[List[int]]], color_input: List[str], n_colors: int = N_COLORS) -> list:
    """
    For each color in default_palette, find the closest color in the reference palettes using Lab Euclidean distance.
    Returns a list of (index, distance) for each color.
    """
    results = []
    for color in default_palette:
        color_lab = rgb2lab(np.array(color, dtype=np.float32).reshape(1, 1, 3) / 255.0).flatten()
        min_dist = float('inf')
        min_idx = -1
        for j, palette in enumerate(palettes):
            for c in palette:
                c_lab = rgb2lab(np.array(c, dtype=np.float32).reshape(1, 1, 3) / 255.0).flatten()
                dist = np.linalg.norm(color_lab - c_lab)
                if dist < min_dist:
                    min_dist = dist
                    min_idx = j
        results.append((min_idx, min_dist))
    return results

# Example usage:
# palettes, filenames = load_palettes_with_filenames('image_colors_pallette_trim.json')
# embeddings = build_palette_embeddings(palettes, output_json='embeddings.json')
# embeddings = load_embeddings('embeddings.json')
# default_palette = ...
# color_input = ...
# results = find_closest_palette(default_palette, embeddings, palettes, color_input)
# for idx, dist in results:
#     print('Closest palette:', palettes[idx], 'Filename:', filenames[idx], 'Distance:', dist)
