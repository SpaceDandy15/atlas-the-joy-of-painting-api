import pandas as pd

def transform_paintings(paintings_df):
    paintings_df['title'] = paintings_df['title'].str.strip().str.title()
    return paintings_df

def transform_colors(colors_df):
    print("Colors columns:", colors_df.columns.tolist())  #debug print

    colors_df['colors'] = colors_df['colors'].str.strip().str.lower()

    return colors_df

def transform_subjects(subjects_df):
    # Normalize columns to lowercase
    subjects_df.columns = subjects_df.columns.str.lower()

    # Clean title column: remove extra quotes, strip, title case
    subjects_df['title'] = subjects_df['title'].str.replace('"', '').str.strip().str.title()

    # Identify subject columns (all except episode and title)
    subject_cols = [col for col in subjects_df.columns if col not in ['episode', 'title']]

    # Melt to long format
    melted = subjects_df.melt(
        id_vars=['episode', 'title'],
        value_vars=subject_cols,
        var_name='subject',
        value_name='present'
    )

    # Filter to subjects that are present (1)
    melted = melted[melted['present'] == 1]

    # Lowercase subject names
    melted['subject'] = melted['subject'].str.lower()

    # Reset index
    melted = melted.reset_index(drop=True)

    return melted[['episode', 'title', 'subject']]

def transform_data(raw_data):
    paintings = transform_paintings(raw_data['paintings'])
    colors = transform_colors(raw_data['colors'])
    subjects = transform_subjects(raw_data['subjects'])

    return {
        'paintings': paintings,
        'colors': colors,
        'subjects': subjects
    }
