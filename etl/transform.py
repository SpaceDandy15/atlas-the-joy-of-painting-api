import pandas as pd
import re

def transform_paintings(paintings_df):
    """
    Clean the painting data:
    - Extract air_date from the title (e.g. "(Jan 1, 1983)").
    - Clean up and title-case the title text.
    - Create new column for air_date (datetime).
    """
    # Step 1: Extract air_date string from title
    def extract_date(title):
        match = re.search(r'\((.*?)\)', title)
        return match.group(1) if match else None

    paintings_df['air_date_str'] = paintings_df['title'].apply(extract_date)

    # Step 2: Convert air_date string to datetime
    paintings_df['air_date'] = pd.to_datetime(paintings_df['air_date_str'], errors='coerce')

    # Step 3: Clean title (remove date part and format)
    def clean_title(title):
        return re.sub(r'\s*\(.*?\)', '', title).strip().title()

    paintings_df['title'] = paintings_df['title'].apply(clean_title)

    # Optional: Extract season and episode from title (e.g., "Season 2 Episode 5")
    def extract_season_episode(title):
        match = re.search(r'Season\s*(\d+)\s*Episode\s*(\d+)', title, re.IGNORECASE)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None, None

    paintings_df[['season', 'episode']] = paintings_df['title'].apply(
        lambda t: pd.Series(extract_season_episode(t))
    )

    paintings_df = paintings_df.drop(columns=['air_date_str'])

    return paintings_df


def transform_colors(colors_df):
    """
    Clean color data:
    - Strip whitespace and lowercase all color names.
    """
    print("Colors columns:", colors_df.columns.tolist())  # Debug print
    colors_df['colors'] = colors_df['colors'].str.strip().str.lower()
    return colors_df


def transform_subjects(subjects_df):
    """
    Transform the subject data:
    - Normalize column names to lowercase
    - Reshape from wide to long format
    - Extract episode and season
    """
    # Normalize column names
    subjects_df.columns = subjects_df.columns.str.lower()

    # Clean title
    subjects_df['title'] = subjects_df['title'].str.replace('"', '').str.strip().str.title()

    # Extract season and episode from episode string (e.g., "S02E05")
    def parse_season_episode(ep_str):
        match = re.match(r'[Ss](\d+)[Ee](\d+)', ep_str)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None, None

    subjects_df[['season', 'episode_number']] = subjects_df['episode'].apply(
        lambda x: pd.Series(parse_season_episode(x))
    )

    # Get only subject columns (everything except title and episode)
    subject_cols = [col for col in subjects_df.columns if col not in ['episode', 'title', 'season', 'episode_number']]

    # Reshape from wide to long format
    melted = subjects_df.melt(
        id_vars=['title', 'season', 'episode_number'],
        value_vars=subject_cols,
        var_name='subject',
        value_name='present'
    )

    # Keep only rows where subject is marked present (1)
    melted = melted[melted['present'] == 1]

    # Clean subject names
    melted['subject'] = melted['subject'].str.strip().str.lower()

    return melted[['title', 'season', 'episode_number', 'subject']]


def transform_data(raw_data):
    """
    Apply all data transformations and return cleaned DataFrames.
    """
    paintings = transform_paintings(raw_data['paintings'])
    colors = transform_colors(raw_data['colors'])
    subjects = transform_subjects(raw_data['subjects'])

    return {
        'paintings': paintings,
        'colors': colors,
        'subjects': subjects
    }
