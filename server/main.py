from colours import query_colormind_with_color, get_colormind_themes
from embeddings import find_closest_palette, load_palettes, build_palette_embeddings
def main():
    print("Hello from server!")


if __name__ == "__main__":
    themes = get_colormind_themes()
    reference_palette = load_palettes('image_colors_palette_trim.json')
    embeddings = build_palette_embeddings(reference_palette)
    default_palette = query_colormind_with_color(["#d4bfa9"], show_samples=True, themes=themes)
    # query_colormind_with_color(["#d4bfa9", "#A09B84"], show_samples=True, themes=themes)
    print(default_palette)
