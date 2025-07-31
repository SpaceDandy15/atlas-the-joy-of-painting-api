import psycopg2
from psycopg2 import sql
from db import get_db_connection

def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS painting (
            id SERIAL PRIMARY KEY,
            title VARCHAR UNIQUE,
            episode_number VARCHAR,
            season_number VARCHAR,
            air_date TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS color (
            id SERIAL PRIMARY KEY,
            name VARCHAR UNIQUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS subject (
            id SERIAL PRIMARY KEY,
            name VARCHAR UNIQUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS painting_color (
            painting_id INTEGER REFERENCES painting(id) ON DELETE CASCADE,
            color_id INTEGER REFERENCES color(id) ON DELETE CASCADE,
            UNIQUE (painting_id, color_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS painting_subject (
            painting_id INTEGER REFERENCES painting(id) ON DELETE CASCADE,
            subject_id INTEGER REFERENCES subject(id) ON DELETE CASCADE,
            UNIQUE (painting_id, subject_id)
        );
        """
    ]

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        conn.commit()
        cur.close()
        print("Tables created successfully (or already exist).")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating tables: {error}")
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    create_tables()
