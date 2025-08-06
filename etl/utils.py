import re

def normalize_title(title):
    # Lowercase, strip punctuation, remove date in parentheses
    title = title.lower().strip()
    title = re.sub(r'\s*\(.*?\)', '', title)  # Remove anything in parentheses
    title = re.sub(r'[^\w\s]', '', title)     # Remove punctuation
    title = re.sub(r'\s+', ' ', title)        # Normalize spaces
    return title
