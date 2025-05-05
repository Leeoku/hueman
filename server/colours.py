import requests

def hex_to_rgb(hexcode):
    """Convert hex code to RGB tuple."""
    hexcode = hexcode.lstrip('#')
    return [int(hexcode[i:i+2], 16) for i in (0, 2, 4)]

def query_colormind_with_color(hex_input):
    # Convert hex to RGB for the API
    rgb_input = hex_to_rgb(hex_input)
    print('rgbinput',rgb_input)

    # Format: [color or "N", ..., 5 total]
    payload = {
        "model": "default",
        "input": [rgb_input, "N", "N", "N", "N"]
    }
    response = requests.post('http://colormind.io/api/', json=payload)

    if response.status_code == 200:
        palette = response.json()['result']
        print("🎨 Recommended Palette (RGB):")
        for color in palette:
            print("color", color)
            print(f"RGB: {color} | HEX: #{''.join(f'{c:02x}' for c in color)}")
    else:
        print("❌ Error querying Colormind:", response.text)