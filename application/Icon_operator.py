from pathlib import Path

# Locate the icons folder
CURRENT_DIRECTORY = Path(__file__).resolve().parent
PROJECT_DIRECTORY = CURRENT_DIRECTORY.parent
ICON_DIRECTORY = PROJECT_DIRECTORY / "icons"


def get_icon(icon_name):
    icon_path = ICON_DIRECTORY / icon_name

    if icon_path.exists():
        return str(icon_path)

    print(f"Icon not found: {icon_path}")
    return None


def green_plus():
    return get_icon("green_plus.png")