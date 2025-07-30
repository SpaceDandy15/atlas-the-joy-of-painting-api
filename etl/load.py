import psycopg2
from db import get_db_connection

# Load the transformed data into the database
def load_data(data):
    conn = get_db_connection()
    cur = conn.cursor()

    paintings = data['paintings']
    colors = data['colors']
    subjects = data['subjects']

    # Insert paintings
    for _, row in paintings.iterrows():
        cur.execute(
            "INSERT INTO painting (title, episode, season, ... ) VALUES (%s, %s, %s, ...)",
            (row['title'], row['episode'], row['season'], ...)
        )

    # Insert colors
    for _, row in colors.iterrows():
        cur.execute(
            "INSERT INTO color (color) VALUES (%s) ON CONFLICT DO NOTHING",
            (row['color'],)
        )

    # Insert subjects
    for _, row in subjects.iterrows():
        cur.execute(
            "INSERT INTO subject (subject) VALUES (%s) ON CONFLICT DO NOTHING",
            (row['subject'],)
        )

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()
