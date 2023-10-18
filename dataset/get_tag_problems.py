import requests
import json
import os

# Load data
with open("tags.txt", "r") as tags_file:
    tags = [line.strip() for line in tags_file]

problems_per_tag = dict([(tag, 0) for tag in tags])

for tag in tags:
    api_url = f"https://codeforces.com/api/problemset.problems?tags={tag}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            tag_problem_set = data["result"]

            if not os.path.exists(f"submissions/{tag}"):   
                os.makedirs(f"submissions/{tag}")

            output_file = f"submissions/{tag}/{tag}.json"
            with open(output_file, "w") as json_file:
                json.dump(tag_problem_set, json_file, indent=4)

            problems_per_tag[tag] += len(tag_problem_set["problems"])

            print(f"Data saved in file {output_file}")
        else:
            print("~~~~~ Unsuccessful API call ~~~~~")
    else:
        print("~~~~~ Error connecting to Codeforces API ~~~~~")

with open("submissions/total_tags_problems.txt", "w") as file:
    file.write("----- TOTAL PROBLEMS COLLECTED PER TAG -----\n")
    for tag in tags:
        file.write(f"{tag}: {problems_per_tag[tag]}\n")
