from colours import query_colormind_with_color, get_colormind_themes

def main():
    print("Hello from server!")


if __name__ == "__main__":
    themes = get_colormind_themes()
    query_colormind_with_color(["#d4bfa9"], show_samples=True, themes=themes)
    # query_colormind_with_color(["#d4bfa9", "#A09B84"], show_samples=True, themes=themes)
