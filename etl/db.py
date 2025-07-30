import psycopg2
import os

# Returns a PostgreSQL connection object
def get_db_connection():
    return psycopg2.connect(
        dbname="your_db_name",
        user="your_username",
        password="your_password",
        host="localhost",
        port=5432
    )
