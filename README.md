# COVID-19 Data Analysis

## Project Overview
This project focuses on analyzing COVID-19 data from multiple regions: USA, Europe, and Asia. The data is collected, processed, and visualized using a combination of REST APIs, relational data sources, and data processing tools.

## Team Members
- SOURAV SARKAR
- PRANSHU Gautam
- 
## Data Sources
- **USA**: REST API (JSON)
- **Europe**: ECDC API (JSON)
- **Asia**: MySQL (CSV sourced from Kaggle)

## Project Structure
- `dags/`: Directory to store all DAGs (Directed Acyclic Graphs).
  - `Collect_Data/`: Subdirectory for data extraction, processing, and indexing.
    - `covid_19_usa.py`: Extracts data from the USA REST API and saves it as usa.json.
    - `covid_19_europe.py`: Extracts data from the Europe REST API and saves it as europe.json.
    - `data_processing.py`: Extracts data from the MySQL database and saves it as asia.json. Combines usa.json, europe.json, and asia.json into a single world.parquet file using Apache Spark.
    - `elastic_index.py`: Indexes the world.parquet file in Elasticsearch.
  - `my_first_dag.py`: Airflow DAG to automate the entire data collection, processing, and indexing workflow.

## Data Collection and Processing
- **USA Data Extraction**: Uses `covid_19_usa.py` to fetch data from the REST API.
- **Europe Data Extraction**: Uses `covid_19_europe.py` to fetch data from the ECDC API.
- **Asia Data Extraction**: Uses `data_processing.py` to fetch data from a MySQL database.
- **Data Aggregation**: Combines data from all regions into `world.parquet`.
- **Indexing in Elasticsearch**: Uses `elastic_index.py` to index data in Elasticsearch.

## Data Visualization
Visualizations and KPIs are created using Kibana.

## Automation with Airflow
The workflow is automated using `my_first_dag.py`.

## Conclusion
This project demonstrates a comprehensive approach to collecting, processing, and visualizing COVID-19 data from multiple regions using modern data engineering tools and techniques.
