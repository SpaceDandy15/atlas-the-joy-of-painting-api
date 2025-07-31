import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="joy_of_painting",
        user="bob_ross",
        password="colors",
        host="localhost",
        port="5432"
    )
