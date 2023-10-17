import requests
import json

# Load data
with open("tags.txt", "r") as tags_file:
    tags = [line.strip() for line in tags_file]

for tag in tags:
    api_url = f"https://codeforces.com/api/problemset.problems?tags={tag}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            problems = data["result"]

            output_file = f"submissions/{tag}/{tag}.json"
            with open(output_file, "w") as json_file:
                json.dump(problems, json_file)

            print(f"Data saved in file {output_file}")
        else:
            print("~~~~~ Unsuccessful API call ~~~~~")
    else:
        print("~~~~~ Error connecting to Codeforces API ~~~~~")
