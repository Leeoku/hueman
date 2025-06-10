from fastmcp import FastMCP
from colours import query_colormind_with_color, get_colormind_themes
from embeddings import find_closest_palette, build_palette_embeddings, load_embeddings, load_palettes_with_filenames

mcp = FastMCP("Hueman MCP")

# sample color_input = ["#d4bfa9", "#A09B84", "C5C5BE"]
@mcp.tool
def colormind_tool(color_input: list[str]) -> list[str]:
    themes = get_colormind_themes()
    palettes, filenames = load_palettes_with_filenames('image_colors_palette_trim5.json')
    # Build and save embeddings to file
    embeddings = build_palette_embeddings(palettes, output_json='embeddings.json')
    # Load embeddings from file
    embeddings = load_embeddings('embeddings.json')
    default_palette = query_colormind_with_color(color_input, show_samples=True, themes=themes)
    results = find_closest_palette(default_palette, embeddings, palettes, color_input)
    for idx, dist in results:
        print(f"Closest palette: {palettes[idx]}, Filename: {filenames[idx]}, Euclidean Distance: {dist}")

if __name__ == "__main__":
    mcp.run( transport="streamable-http",
        host="0.0.0.0",
        port=8000)