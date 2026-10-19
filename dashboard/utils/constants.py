"""File-path and dashboard constants."""

from pathlib import Path

# Folders that hold the images and the markdown text used by the pages.
ASSETS_PATH = Path(__file__).parents[1] / "assets"
IMAGE_PATH = ASSETS_PATH / "image"
MARKDOWN_PATH = ASSETS_PATH / "markdown"

# Drag and drop your logo into assets/image/ with this name.
LOGO_PATH = IMAGE_PATH / "gallery.png"

# A flight counts as delayed when it is more than this many minutes late
# (same value as delay_threshold_minutes in dbt_project.yml).
DELAY_THRESHOLD_MINUTES = 15

# Session-state keys of the sidebar filters (app.py keeps them alive between pages).
FILTER_KEYS = ["filter_direction", "filter_airports", "filter_airlines", "filter_dates"]
