import csv
import pandas as pd

def extract_dates():
    """
    Extracts the 'dates.csv' file using a custom parser to handle
    commas inside unquoted text fields.

    Returns:
        pd.DataFrame: DataFrame with columns 'title' and 'description'.
    """
    dates_list = []
    with open('data/dates.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # Rejoin the row in case commas split the fields incorrectly
            full_line = ','.join(row)
            
            # Split on ' - ' to separate the title/date from the description
            if ' - ' in full_line:
                title_date, description = full_line.split(' - ', 1)
            else:
                # If no separator, treat whole line as title_date and empty description
                title_date = full_line
                description = ''
            
            # Strip whitespace and append as a dictionary
            dates_list.append({'title_date': title_date.strip(), 'description': description.strip()})
    
    # Convert list of dicts to DataFrame
    df = pd.DataFrame(dates_list)
    # Rename title_date to title for compatibility with transform.py
    df.rename(columns={'title_date': 'title'}, inplace=True)
    return df

def extract_colors():
    """
    Reads 'colors.csv' using pandas. Assumes this file is well-formed CSV.

    Returns:
        pd.DataFrame: DataFrame containing color data.
    """
    return pd.read_csv('data/colors.csv')

def extract_subjects():
    """
    Reads 'subjects.csv' using pandas. Assumes this file is well-formed CSV.

    Returns:
        pd.DataFrame: DataFrame containing subject data.
    """
    return pd.read_csv('data/subjects.csv')

def extract_data():
    """
    Runs all extract functions and returns a dictionary
    of DataFrames for colors, paintings, and subjects.

    Returns:
        dict: keys are 'colors', 'paintings', 'subjects' with corresponding DataFrames.
    """
    colors = extract_colors()
    paintings = extract_dates()
    subjects = extract_subjects()

    return {
        'colors': colors,
        'paintings': paintings,
        'subjects': subjects
    }

if __name__ == '__main__':
    # For testing extraction when run standalone
    data = extract_data()
    print("Colors data sample:")
    print(data['colors'].head())
    print("\nPaintings data sample:")
    print(data['paintings'].head())
    print("\nSubjects data sample:")
    print(data['subjects'].head())
