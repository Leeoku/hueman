def hex_to_rgb(hexcode):
    """
    Convert a hex color string (e.g., '#d4bfa9' or 'd4bfa9') to an RGB list [r, g, b].
    """
    hexcode = hexcode.lstrip('#')
    return [int(hexcode[i:i+2], 16) for i in (0, 2, 4)] 