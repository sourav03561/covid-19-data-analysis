import pandas as pd
from elasticsearch import Elasticsearch, helpers, ConnectionError, NotFoundError

# Step 1: Read the Parquet file into a DataFrame
df = pd.read_parquet('/home/wsl/airflow/dags/Collect Data/world.parquet')

# Print the column names to inspect them
print("Columns in DataFrame:", df.columns)

# Adjust the column names as per the actual DataFrame columns
df = df[['date', 'continent', 'country', 'cases', 'deaths']]
# Ensure date is in the correct format
df['date'] = df['cases'].fillna(0).astype(int)
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Replace NaN values with appropriate defaults or remove rows with NaNs
df['cases'] = df['cases'].fillna(0).astype(int)
df['deaths'] = df['deaths'].fillna(0).astype(int)

# Remove rows with missing required fields
df = df.dropna(subset=['date', 'continent', 'country'])

# Step 2: Transform the DataFrame into a list of dictionaries
records = df.to_dict(orient='records')

# Step 3: Create an Elasticsearch client
try:
    es = Elasticsearch(['http://localhost:9200'])
    # Test connection
    if not es.ping():
        raise ValueError("Connection to Elasticsearch failed")

    # Define the index name
    index_name = 'world_data'

    # Step 4: Define the index mapping
    mapping = {
        "mappings": {
            "properties": {
                "date": {"type": "date"},
                "continent": {"type": "keyword"},
                "country": {"type": "keyword"},
                "cases": {"type": "long"},
                "deaths": {"type": "long"}
            }
        }
    }

    # Create the index with the defined mapping
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mapping)

    # Prepare the records for bulk indexing
    def generate_records(records, index_name):
        for record in records:
            yield {
                "_index": index_name,
                "_source": record
            }
            print(record)


    # Bulk index the records
    try:
        helpers.bulk(es, generate_records(records, index_name))
        print("Data indexed successfully!")
    except helpers.BulkIndexError as bulk_error:
        print(f"Bulk indexing error: {bulk_error}")
        for error in bulk_error.errors:
            print(error)

except ConnectionError as e:
    print(f"Connection error: {e}")
except NotFoundError as e:
    print(f"Index not found: {e}")
except Exception as e:
    print(f"Error: {e}")
