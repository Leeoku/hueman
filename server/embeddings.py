import numpy as np
import json
from typing import List, Tuple
from skimage.color import rgb2lab

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

def find_closest_palette(query_palette: List[List[int]], embeddings: np.ndarray, palettes: List[List[List[int]]], n_colors: int = N_COLORS) -> Tuple[int, float]:
    """
    Find the index and distance of the closest palette to the query_palette using Euclidean distance in Lab color space.
    Lower distance means higher similarity (0 means identical palettes).
    This is a perceptual color difference: lower is better, higher is worse.
    """
    query_emb = rgb_palette_to_lab(query_palette, n_colors)
    # Compute Euclidean distance between the query and each reference palette
    dists = np.linalg.norm(embeddings - query_emb, axis=1)
    idx = np.argmin(dists)  # Index of the most similar (smallest distance)
    return idx, dists[idx]

# Example usage:
# palettes, filenames = load_palettes_with_filenames('image_colors_pallette_trim.json')
# embeddings = build_palette_embeddings(palettes, output_json='embeddings.json')
# embeddings = load_embeddings('embeddings.json')
# idx, dist = find_closest_palette([[100, 120, 130], [200, 210, 220], [50, 60, 70], [0,0,0], [0,0,0]], embeddings, palettes)
# print('Closest palette:', palettes[idx], 'Filename:', filenames[idx], 'Distance:', dist)
