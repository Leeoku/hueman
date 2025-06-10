# Hueman

Hueman is a color analysis and palette recommendation tool that leverages AI and perceptual color science to help you find, generate, and compare color palettes for images and design projects.

## Features

- **Palette Extraction:** Extracts dominant color palettes from images and stores them in JSON format.
- **Colormind Integration:** Uses the Colormind API to generate harmonious color palettes based on user-provided colors.
- **Palette Embedding:** Converts color palettes to perceptual Lab color space embeddings for accurate color similarity search.
- **Similarity Search:** Finds the closest matching palette from a reference set using Euclidean distance in Lab space.

## How It Works

1. **Extract Palettes:**
   - Use image analysis (e.g., ColorThief or Pillow) to extract palettes from images and save them in a JSON file (e.g., `image_colors_palette_trim5.json`).

2. **Generate Palettes with Colormind:**
   - Provide up to 5 hex colors as input.
   - The system queries the Colormind API to generate a harmonious palette, filling in missing colors if fewer than 5 are provided.

3. **Embed Palettes:**
   - All palettes are converted to Lab color space and flattened to vectors of length 15 (5 colors × 3 Lab channels).
   - Embeddings are saved to a file (e.g., `embeddings.json`) for fast similarity search.

4. **Find Closest Palette:**
   - For each color in the generated palette, the system finds the closest color in the reference palettes using Euclidean distance in Lab space.
   - The filename and distance of the closest match are displayed.

## Example Usage

```python
#TODO hookup to google cloud vision, for now pass in an array of colour codes up to 5

# In main.py, ensure 
color_input = ["#d4bfa9", "#A09B84", "C5C5BE"]
```
Run `uv run main.py`

## Requirements
- Python 3.8+
- `requests`
- `rich`
- `scikit-image`
- `numpy`

## Project Structure
- `colours.py` — Colormind API integration and palette visualization
- `embeddings.py` — Palette embedding and similarity search
- `color_utils.py` — Shared color utility functions
- `image_colors_palette_trim5.json` — Reference palettes extracted from images
- `embeddings.json` — Saved palette embeddings for fast search

## Tools
- `Connection` - Connect using `localhost:8000`
   - for WSL2, use `hostname -I` and replace localhost with the ip address
- `Tool Inspector` — Run using `npx @modelcontextprotocol/inspector`
   - connect using the provided address, use WSL2 IP address if needed

## License
MIT
