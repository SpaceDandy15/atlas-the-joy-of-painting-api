import pandas as pd
import re

def transform_paintings(paintings_df):
    """
    Clean the painting data:
    - Extracts air_date from the title.
    - Cleans up title formatting.
    """

    # --- Step 1: Extract air_date string from original title ---
    def extract_date(title):
        match = re.search(r'\((.*?)\)', title)
        if match:
            return match.group(1)
        else:
            return None

    paintings_df['air_date_str'] = paintings_df['title'].apply(extract_date)

    # --- Step 2: Convert extracted string to datetime (if valid) ---
    paintings_df['air_date'] = pd.to_datetime(paintings_df['air_date_str'], errors='coerce')

    # --- Step 3: Clean the title itself (strip and remove date part) ---
    def clean_title(title):
        return re.sub(r'\s*\(.*?\)', '', title).strip().title()

    paintings_df['title'] = paintings_df['title'].apply(clean_title)

    # Drop the temporary string column
    paintings_df = paintings_df.drop(columns=['air_date_str'])

    return paintings_df


def transform_colors(colors_df):
    """
    Lowercase and clean color names.
    """
    print("Colors columns:", colors_df.columns.tolist())  # debug print

    colors_df['colors'] = colors_df['colors'].str.strip().str.lower()

    return colors_df


def transform_subjects(subjects_df):
    """
    Reshape and clean subject data from wide to long format.
    """
    # Normalize columns to lowercase
    subjects_df.columns = subjects_df.columns.str.lower()

    # Clean title column
    subjects_df['title'] = subjects_df['title'].str.replace('"', '').str.strip().str.title()

    # Get subject columns only
    subject_cols = [col for col in subjects_df.columns if col not in ['episode', 'title']]

    # Melt to long format
    melted = subjects_df.melt(
        id_vars=['episode', 'title'],
        value_vars=subject_cols,
        var_name='subject',
        value_name='present'
    )

    # Keep only rows where subject is marked present
    melted = melted[melted['present'] == 1]

    # Clean subject names
    melted['subject'] = melted['subject'].str.lower()

    return melted[['episode', 'title', 'subject']]


def transform_data(raw_data):
    """
    Apply all transformations to the raw extracted data.
    """
    paintings = transform_paintings(raw_data['paintings'])
    colors = transform_colors(raw_data['colors'])
    subjects = transform_subjects(raw_data['subjects'])

    return {
        'paintings': paintings,
        'colors': colors,
        'subjects': subjects
    }
