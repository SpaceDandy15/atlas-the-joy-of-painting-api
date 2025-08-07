import ast
from etl.db import get_db_connection
from etl.utils import normalize_title  # <-- imported from utils

def load_data(data):
    conn = get_db_connection()
    cur = conn.cursor()

    paintings = data['paintings']
    colors = data['colors']
    subjects = data['subjects']

    # Insert paintings
    painting_id_map = {}  # map normalized title -> id
    for idx, row in paintings.iterrows():
        raw_title = row['title']
        norm_title = normalize_title(raw_title)

        # Prefer the keys that exist; convert to int or None
        episode = row.get('episode') or row.get('episode_number') or None
        season = row.get('season') or row.get('season_number') or None

        try:
            episode = int(episode) if episode is not None else None
        except (ValueError, TypeError):
            episode = None

        try:
            season = int(season) if season is not None else None
        except (ValueError, TypeError):
            season = None

        air_date = row.get('air_date') or None

        cur.execute(
            """
            INSERT INTO painting (title, episode, season, air_date)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (title) DO UPDATE SET title=EXCLUDED.title
            RETURNING id
            """,
            (raw_title, episode, season, air_date)
        )
        painting_id = cur.fetchone()[0]
        painting_id_map[norm_title] = painting_id
    print(f"Loaded {len(painting_id_map)} paintings")

    # Insert unique colors and map name -> id
    unique_colors = set()
    for idx, row in colors.iterrows():
        color_list_str = row['colors']
        try:
            color_list = ast.literal_eval(color_list_str)
        except Exception as e:
            print(f"Error parsing colors for row {idx}: {e}")
            color_list = []
        for c in color_list:
            unique_colors.add(c.strip().lower())
    print(f"Found {len(unique_colors)} unique colors")

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
            cur.execute("SELECT id FROM color WHERE name = %s", (color_name,))
            color_id = cur.fetchone()[0]
        color_id_map[color_name] = color_id
    print(f"Loaded {len(color_id_map)} colors")

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
    print(f"Loaded {len(subject_id_map)} subjects")

    # Link paintings to colors
    missing_paintings_colors = set()
    for idx, row in colors.iterrows():
        raw_title = row['painting_title']
        norm_title = normalize_title(raw_title)
        painting_id = painting_id_map.get(norm_title)
        if not painting_id:
            missing_paintings_colors.add(raw_title)
            continue
        try:
            color_list = ast.literal_eval(row['colors'])
        except Exception as e:
            print(f"Error parsing colors for painting '{raw_title}': {e}")
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
    if missing_paintings_colors:
        print(f"Missing painting titles when linking colors: {missing_paintings_colors}")

    # Link paintings to subjects
    missing_paintings_subjects = set()
    for idx, row in subjects.iterrows():
        raw_title = row['title']
        norm_title = normalize_title(raw_title)
        painting_id = painting_id_map.get(norm_title)
        if not painting_id:
            missing_paintings_subjects.add(raw_title)
            continue
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
    if missing_paintings_subjects:
        print(f"Missing painting titles when linking subjects: {missing_paintings_subjects}")

    conn.commit()
    cur.close()
    conn.close()
