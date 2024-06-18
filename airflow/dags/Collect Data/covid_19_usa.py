import requests
import json
url = "https://covid-193.p.rapidapi.com/history"

querystring = {"country":"usa"}

headers = {
	"X-RapidAPI-Key": "6063e77f40mshf54dddc02df3ccfp15582fjsnaacdd007242b",
	"X-RapidAPI-Host": "covid-193.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

data = response.json()

with open("/home/wsl/airflow/dags/Collect Data/usa.json", "w") as outfile:
    json.dump(data, outfile, indent=4)
