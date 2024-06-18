import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, to_date, col
import mysql.connector
import json
from pyspark.sql.functions import row_number
from pyspark.sql.window import Window

# Initialize Spark session
spark = SparkSession.builder \
    .appName('data_processing') \
    .getOrCreate()
print(spark)

# Function to process JSON files
def process_json(file_path, explode_col, select_cols, col_renames):
    df = spark.read.format("json").option('multiline', 'true').option("inferschema", 'true').load(file_path)
    df = df.select(explode(explode_col).alias('new_record')).select(*select_cols)
    for old_name, new_name in col_renames.items():
        df = df.withColumnRenamed(old_name, new_name)
    return df

# Process Europe data
europe = process_json(
    "/home/wsl/airflow/dags/Collect Data/europe.json",
    'records',
    ['new_record.dateRep', 'new_record.continentExp', 'new_record.countriesAndTerritories', 'new_record.cases', 'new_record.deaths'],
    {"dateRep": "date", "continentExp": "continent", "countriesAndTerritories": "country"}
)

# Process USA data
usa = process_json(
    "/home/wsl/airflow/dags/Collect Data/usa.json",
    'response',
    ['new_record.day', 'new_record.continent', 'new_record.country', 'new_record.cases.total', 'new_record.deaths.total'],
    {"day": "date", "cases.total": "cases", "deaths.total": "deaths"}
)

# Function to fetch data from MySQL and save as JSON
def fetch_and_save_as_json(query, output_path):
    mydb = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Naren@03561",
        database="world"
    )
    cursor = mydb.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    data = [{"iso_code": row[0], "continent": row[1], "date": row[2].strftime('%Y-%m-%d'), "location": row[3],
             "total_cases": row[4], "new_cases": row[5], "total_deaths": row[6], "new_deaths": row[7]} for row in rows]
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file)
    cursor.close()
    mydb.close()

# Fetch and save Asia data
fetch_and_save_as_json("SELECT iso_code, continent, date, location, total_cases, new_cases, total_deaths, new_deaths FROM covid_19",
                       '/home/wsl/airflow/dags/Collect Data/asia.json')

# Process Asia data
asia = spark.read.format("json").option('multiline', 'true').option("inferschema", 'true').load("/home/wsl/airflow/dags/Collect Data/asia.json")
asia = asia.select('date', 'continent', 'location', 'total_cases', 'total_deaths') \
    .withColumnRenamed("location", "country") \
    .withColumnRenamed("total_cases", "cases") \
    .withColumnRenamed("total_deaths", "deaths")

# Union all dataframes
world = asia.union(europe).union(usa)
world = world.withColumn("date", to_date(col("date"), "yyyy-MM-dd"))
windowSpec = Window.orderBy("date")
world = world.withColumn("idx", row_number().over(windowSpec))

# Save the world DataFrame as a Parquet file
output_parquet_path = "/home/wsl/airflow/dags/Collect Data/world.parquet"
world.write.mode("overwrite").parquet(output_parquet_path)

print(f"Data saved successfully as Parquet file at {output_parquet_path}")
