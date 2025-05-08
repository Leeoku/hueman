import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

def hex_to_rgb(hexcode):
    """Convert hex code to RGB tuple."""
    hexcode = hexcode.lstrip('#')
    return [int(hexcode[i:i+2], 16) for i in (0, 2, 4)]

def get_colormind_themes():
    """Query Colormind for the current list of available themes."""
    url = "http://colormind.io/list/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("result", [])
    except Exception as e:
        print(f"Error fetching Colormind themes: {e}")
        return []

def query_colormind_with_color(hex_input, model="default", show_samples=False, themes=None):
    # Accept a list of hex codes for hex_input
    if not isinstance(hex_input, list):
        hex_input = [hex_input]
    if len(hex_input) > 5:
        raise ValueError("hex_input cannot be longer than 5.")
    rgb_inputs = [hex_to_rgb(h) for h in hex_input]
    # Fill up to 5 with 'N'
    payload_input = rgb_inputs + ["N"] * (5 - len(rgb_inputs))
    print('rgb_inputs', rgb_inputs)

    console = Console()
    table = Table(title="🎨 Recommended Palette (RGB)")
    table.add_column("#", justify="center")
    table.add_column("RGB (default)", justify="center")
    table.add_column("HEX (default)", justify="center")
    theme_names = themes if themes else []
    theme_palettes = {}
    for theme in theme_names:
        # Fetch palette for each theme, using the rgb_inputs as the first N colors
        url = "http://colormind.io/api/"
        payload_theme = {"model": theme, "input": payload_input}
        try:
            response_theme = requests.post(url, json=payload_theme)
            response_theme.raise_for_status()
            data_theme = response_theme.json()
            theme_palette = data_theme.get("result", [])
        except Exception as e:
            print(f"Error fetching palette for theme '{theme}': {e}")
            theme_palette = []
        theme_palettes[theme] = theme_palette
        table.add_column(theme, justify="center")
    if show_samples:
        table.add_column("ChatGPT", justify="center")
        table.add_column("ChatGPT_2", justify="center")
        table.add_column("ColorKit", justify="center")
        table.add_column("CloudVision", justify="center")

    chatgpt_colors = [
        (32, 58, 94),
        (178, 34, 52),
        (43, 43, 43),
        (47, 111, 117),
        (198, 84, 30),
        (125, 151, 121)
    ]

    chatgpt_colors_second_query = [
        [51, 51, 51],
        [0, 51, 102],
        [0, 79, 79],
        [178, 34, 34],
        [240, 195, 0]
    ]

    colorkit_hexes = [
        "#858961",
        "#282f17",
        "#dfdfdc",
        "#474133",
        "#d0c7a7"
    ]
    colorkit_colors = [tuple(hex_to_rgb(h)) for h in colorkit_hexes]

    cloudvision_colors = [
        {"hex": "9B9A97", "percent": 20.560620272617474},
        {"hex": "A09B84", "percent": 16.97611515595522},
        {"hex": "C5C5BE", "percent": 14.618182119423029},
        {"hex": "7A7B79", "percent": 10.362324898132385},
        {"hex": "E6E6E4", "percent": 8.966651047076807},
        {"hex": "7E7B61", "percent": 8.714496119628375},
        {"hex": "575751", "percent": 6.418926628161042},
        {"hex": "59563C", "percent": 6.211469642297271},
        {"hex": "C5C0AA", "percent": 5.719154972997352},
        {"hex": "738041", "percent": 1.4520591437110426}
    ]
    cloudvision_rgbs = [tuple(hex_to_rgb(c["hex"])) for c in cloudvision_colors]

    # Always use the 'default' theme for the RGB/HEX columns
    default_palette = theme_palettes.get("default", [])
    # Determine the maximum number of rows needed
    max_len = max(
        *(len(theme_palettes[t]) for t in theme_names),
        len(chatgpt_colors),
        len(chatgpt_colors_second_query),
        len(colorkit_colors),
        len(cloudvision_rgbs),
        len(default_palette)
    ) if show_samples or theme_names else 0

    for idx in range(max_len):
        # Main palette row (always use the 'default' theme for RGB/HEX columns)
        if idx < len(default_palette):
            color = default_palette[idx]
            rgb_str = str(tuple(color))
            hex_str = f"#{''.join(f'{c:02x}' for c in color)}"
        else:
            color = None
            rgb_str = ""
            hex_str = ""
        row = [str(idx+1), rgb_str, hex_str]
        # Add theme columns
        for theme in theme_names:
            theme_palette = theme_palettes[theme]
            if idx < len(theme_palette):
                theme_color = theme_palette[idx]
                theme_swatch = Text("     ", style=f"on rgb({theme_color[0]},{theme_color[1]},{theme_color[2]})")
            else:
                theme_swatch = Text("")
            row.append(theme_swatch)
        if show_samples:
            # ChatGPT swatch
            if idx < len(chatgpt_colors):
                chatgpt_color = chatgpt_colors[idx]
                chatgpt_swatch = Text("     ", style=f"on rgb({chatgpt_color[0]},{chatgpt_color[1]},{chatgpt_color[2]})")
            else:
                chatgpt_swatch = Text("")
            # ChatGPT_2 swatch
            if idx < len(chatgpt_colors_second_query):
                chatgpt2_color = chatgpt_colors_second_query[idx]
                chatgpt2_swatch = Text("     ", style=f"on rgb({chatgpt2_color[0]},{chatgpt2_color[1]},{chatgpt2_color[2]})")
            else:
                chatgpt2_swatch = Text("")
            # ColorKit swatch
            if idx < len(colorkit_colors):
                colorkit_color = colorkit_colors[idx]
                colorkit_swatch = Text("     ", style=f"on rgb({colorkit_color[0]},{colorkit_color[1]},{colorkit_color[2]})")
            else:
                colorkit_swatch = Text("")
            # CloudVision swatch
            if idx < len(cloudvision_rgbs):
                cloudvision_color = cloudvision_rgbs[idx]
                cloudvision_swatch = Text("     ", style=f"on rgb({cloudvision_color[0]},{cloudvision_color[1]},{cloudvision_color[2]})")
            else:
                cloudvision_swatch = Text("")
            row.extend([chatgpt_swatch, chatgpt2_swatch, colorkit_swatch, cloudvision_swatch])
        table.add_row(*row)
    console.print(table)
    return default_palette