import json
import os

class ProfileAgent:
    """Handles loading user data from local JSON files."""
    
    def __init__(self, profile_dir="profiles"):
        self.profile_dir = profile_dir
        
    def load_profile(self, user_id: str) -> dict | None:
        """Loads a user's health profile based on their ID."""
        file_path = os.path.join(self.profile_dir, f"{user_id}.json")
        
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r') as f:
                profile_data = json.load(f)
            return profile_data
        except json.JSONDecodeError:
            print(f"Error decoding JSON for profile: {user_id}")
            return None
        except Exception as e:
            print(f"An error occurred while loading profile {user_id}: {e}")
            return None