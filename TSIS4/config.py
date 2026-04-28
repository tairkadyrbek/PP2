import json
import os

# Default settings
DEFAULT_SETTINGS = {
    'snake_color': [0, 255, 0],  # Green RGB
    'grid_overlay': True,
    'sound': True
}

SETTINGS_FILE = 'settings.json'


def load_settings():
    # Load settings from JSON file or create default if doesn't exist
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    
    try:
        with open(SETTINGS_FILE, "r") as f:
            user_settings = json.load(f)
        
        # Check if any default settings are missing in user settings
        updated = False
        for key, value in DEFAULT_SETTINGS.items():
            if key not in user_settings:
                user_settings[key] = value
                updated = True
        
        if updated:
            save_settings(user_settings)
            
        return user_settings
    except (json.JSONDecodeError, Exception):
        # If the file is messed up, just overwrite it with defaults
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS


def save_settings(settings):
    # Save settings to JSON file
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False


def get_setting(key):
    # Get specific setting value
    settings = load_settings()
    return settings.get(key, DEFAULT_SETTINGS.get(key))