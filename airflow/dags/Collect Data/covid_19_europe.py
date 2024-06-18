import requests
import json

# Get the response from the URL
response = requests.get('https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/json/')

# Extract the JSON content from the response
data = response.json()

# Write the JSON content to a file
with open("/home/wsl/airflow/dags/Collect Data/europe.json", "w") as outfile:
    json.dump(data, outfile, indent=4)
