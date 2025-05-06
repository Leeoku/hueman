import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

def hex_to_rgb(hexcode):
    """Convert hex code to RGB tuple."""
    hexcode = hexcode.lstrip('#')
    return [int(hexcode[i:i+2], 16) for i in (0, 2, 4)]

def query_colormind_with_color(hex_input, model="default", show_samples=False):
    # Convert hex to RGB for the API
    rgb_input = hex_to_rgb(hex_input)
    print('rgbinput',rgb_input)

    # Format: [color or "N", ..., 5 total]
    payload = {
        "model": model,
        "input": [rgb_input, "N", "N", "N", "N"]
    }
    response = requests.post('http://colormind.io/api/', json=payload)

    if response.status_code == 200:
        palette = response.json()['result']
        console = Console()
        table = Table(title="🎨 Recommended Palette (RGB)")
        table.add_column("#", justify="center")
        table.add_column("RGB", justify="center")
        table.add_column("HEX", justify="center")
        table.add_column("ColorMind", justify="center")
        if show_samples:
            table.add_column("ChatGPT", justify="center")
            table.add_column("ColorKit", justify="center")

        chatgpt_colors = [
            (32, 58, 94),
            (178, 34, 52),
            (43, 43, 43),
            (47, 111, 117),
            (198, 84, 30),
            (125, 151, 121)
        ]

        colorkit_hexes = [
            "#858961",
            "#282f17",
            "#dfdfdc",
            "#474133",
            "#d0c7a7"
        ]
        colorkit_colors = [tuple(hex_to_rgb(h)) for h in colorkit_hexes]

        for idx, color in enumerate(palette, 1):
            print("color", color)
            rgb_str = str(tuple(color))
            hex_str = f"#{''.join(f'{c:02x}' for c in color)}"
            colormind_swatch = Text("     ", style=f"on rgb({color[0]},{color[1]},{color[2]})")
            hex_and_block = Text(hex_str + " ")
            hex_and_block.append(colormind_swatch)
            row = [str(idx), rgb_str, hex_and_block, colormind_swatch]
            if show_samples:
                # ChatGPT swatch for this row (if available)
                if idx-1 < len(chatgpt_colors):
                    chatgpt_color = chatgpt_colors[idx-1]
                    chatgpt_swatch = Text("     ", style=f"on rgb({chatgpt_color[0]},{chatgpt_color[1]},{chatgpt_color[2]})")
                else:
                    chatgpt_swatch = Text("")
                # ColorKit swatch for this row (if available)
                if idx-1 < len(colorkit_colors):
                    colorkit_color = colorkit_colors[idx-1]
                    colorkit_swatch = Text("     ", style=f"on rgb({colorkit_color[0]},{colorkit_color[1]},{colorkit_color[2]})")
                else:
                    colorkit_swatch = Text("")
                row.extend([chatgpt_swatch, colorkit_swatch])
            table.add_row(*row)
        console.print(table)
    else:
        print("❌ Error querying Colormind:", response.text)