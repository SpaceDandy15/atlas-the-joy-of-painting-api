# Apply transformations and cleanup to raw data
def transform_data(raw_data):
    """
    Cleans and standardizes raw data fields for consistency.

    Args:
        raw_data (dict): Dictionary containing raw DataFrames
                         with keys 'paintings', 'colors', and 'subjects'.

    Returns:
        dict: Dictionary containing cleaned DataFrames.
    """
    # Extract individual DataFrames
    paintings = raw_data['paintings']
    colors = raw_data['colors']
    subjects = raw_data['subjects']

    # Normalize 'title' in paintings:
    # - Remove leading/trailing spaces
    # - Convert to title case (e.g., "starry night")
    paintings['title'] = paintings['title'].str.strip().str.title()

    # Clean 'colors':
    # - Remove spaces
    # - Convert all to lowercase for uniformity
    colors['colors'] = colors['colors'].str.strip().str.lower()

    # Clean 'subject':
    # - Remove spaces
    # - Convert all to lowercase for uniformity
    subjects['subject'] = subjects['subject'].str.strip().str.lower()

    # Return the cleaned DataFrames in a dictionary
    return {
        'paintings': paintings,
        'colors': colors,
        'subjects': subjects
    }
