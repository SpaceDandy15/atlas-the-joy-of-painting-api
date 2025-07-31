import ast
from db import get_db_connection

def load_data(data):
    conn = get_db_connection()
    cur = conn.cursor()

    paintings = data['paintings']
    colors = data['colors']
    subjects = data['subjects']

    # Insert paintings
    painting_id_map = {}  # map title -> id
    for _, row in paintings.iterrows():
        title = row['title']
        episode = row.get('episode_number') or row.get('episode') or row.get('episode_number')
        season = row.get('season_number') or row.get('season')
        air_date = row.get('air_date')  # if you have this column, else None

        cur.execute(
            """
            INSERT INTO painting (title, episode_number, season_number, air_date)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (title) DO UPDATE SET title=EXCLUDED.title
            RETURNING id
            """,
            (title, episode, season, air_date)
        )
        painting_id = cur.fetchone()[0]
        painting_id_map[title] = painting_id

    # Insert unique colors and map name -> id
    unique_colors = set()
    for _, row in colors.iterrows():
        color_list_str = row['colors']
        try:
            color_list = ast.literal_eval(color_list_str)
        except Exception as e:
            print(f"Error parsing colors for row {_}: {e}")
            color_list = []
        for c in color_list:
            unique_colors.add(c.strip().lower())

    color_id_map = {}
    for color_name in unique_colors:
        cur.execute(
            "INSERT INTO color (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id",
            (color_name,)
        )
        result = cur.fetchone()
        if result:
            color_id = result[0]
        else:
            # color already exists, fetch id
            cur.execute("SELECT id FROM color WHERE name = %s", (color_name,))
            color_id = cur.fetchone()[0]
        color_id_map[color_name] = color_id

    # Insert subjects and map name -> id
    unique_subjects = set(subjects['subject'].str.lower().unique())
    subject_id_map = {}
    for subject_name in unique_subjects:
        cur.execute(
            "INSERT INTO subject (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id",
            (subject_name,)
        )
        result = cur.fetchone()
        if result:
            subject_id = result[0]
        else:
            cur.execute("SELECT id FROM subject WHERE name = %s", (subject_name,))
            subject_id = cur.fetchone()[0]
        subject_id_map[subject_name] = subject_id

    # Link paintings to colors (painting_color table)
    for _, row in colors.iterrows():
        title = row['painting_title'].strip()
        painting_id = painting_id_map.get(title)
        if not painting_id:
            continue
        try:
            color_list = ast.literal_eval(row['colors'])
        except Exception:
            color_list = []
        for c in color_list:
            color_name = c.strip().lower()
            color_id = color_id_map.get(color_name)
            if color_id:
                cur.execute(
                    """
                    INSERT INTO painting_color (painting_id, color_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (painting_id, color_id)
                )

    # Link paintings to subjects (painting_subject table)
    for _, row in subjects.iterrows():
        title = row['title'].strip()
        painting_id = painting_id_map.get(title)
        subject_name = row['subject'].lower()
        subject_id = subject_id_map.get(subject_name)
        if painting_id and subject_id:
            cur.execute(
                """
                INSERT INTO painting_subject (painting_id, subject_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
                """,
                (painting_id, subject_id)
            )

    conn.commit()
    cur.close()
    conn.close()
