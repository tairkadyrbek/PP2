import json
import os

# File names
SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


def load_settings():
    # Load game settings from file
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    
    # Default settings
    return {
        "sound": True,
        "car_color": "blue",
        "difficulty": "medium"
    }


def save_settings(settings):
    # Save game settings to file
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print(f"Error saving settings: {e}")


def load_leaderboard():
    # Load leaderboard from file
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, 'r') as f:
                data = json.load(f)
                # Sort by score (highest first)
                data.sort(key=lambda x: x['score'], reverse=True)
                return data
        except:
            pass
    
    return []


def save_leaderboard(leaderboard):
    # Save leaderboard to file
    try:
        # Keep only top 10
        leaderboard.sort(key=lambda x: x['score'], reverse=True)
        top_10 = leaderboard[:10]
        
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(top_10, f, indent=4)
    except Exception as e:
        print(f"Error saving leaderboard: {e}")


def add_score(username, score, distance, coins):
    # Add a new score to the leaderboard
    leaderboard = load_leaderboard()
    
    new_entry = {
        "name": username,
        "score": score,
        "distance": distance,
        "coins": coins
    }
    
    leaderboard.append(new_entry)
    save_leaderboard(leaderboard)