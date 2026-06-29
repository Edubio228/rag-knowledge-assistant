# app/feedback/feedback_store.py
import json
import os

FEEDBACK_FILE = "feedback.json"

def store_feedback(feedback_id: str, rating: str):
    """Store user feedback in a simple JSON file."""
    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "w") as f:
            json.dump({}, f)
    
    with open(FEEDBACK_FILE, "r") as f:
        data = json.load(f)
    
    data[feedback_id] = rating
    
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)