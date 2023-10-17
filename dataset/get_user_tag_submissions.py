import requests
import json
import os

total_submissions = 0

# Load data
with open("users.txt", "r") as users_file:
    users = [line.strip() for line in users_file]

with open("tags.txt", "r") as tags_file:
    tags = [line.strip() for line in tags_file]

for user_index, user in enumerate(users):
    api_url = f"https://codeforces.com/api/user.status?handle={user}&from=1"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            submissions = data["result"]

            for tag in tags:
                tag_submissions = []

                for submission in submissions:
                    if tag in submission["problem"]["tags"]:
                        tag_submissions.append(submission)

                if not os.path.exists(f"submissions/{tag}"):   
                    os.makedirs(f"submissions/{tag}")

            output_file = f"submissions/{tag}/{tag}_{user}_submissions.json"
            with open(output_file, "w") as json_file:
                json.dump(tag_submissions, json_file, indent=4)

            len_user_tag_submissions = len(tag_submissions)
            total_submissions += len_user_tag_submissions

            print(f"{'-'*50}")
            print(f"User #{user_index + 1}")
            print(f"{tag} - {user} submissions: {len_user_tag_submissions}")
            print(f"Total {tag} submissions: {total_submissions}")
        else:
            print("~~~~~ Unsuccessful API call ~~~~~")
    else:
        print("~~~~~ Error connecting to Codeforces API ~~~~~")
