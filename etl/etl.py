from .extract import extract_data
from .transform import transform_data
from .load import load_data

# Master script to run full ETL pipeline
def run_etl():
    print("Extracting data...")
    raw_data = extract_data()

    print("Transforming data...")
    cleaned_data = transform_data(raw_data)

    print("Loading data...")
    load_data(cleaned_data)

    print("ETL process completed successfully.")

if __name__ == "__main__":
    run_etl()
