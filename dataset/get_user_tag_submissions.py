import requests
import json
import os

# Load data
with open("users.txt", "r") as users_file:
    users = [line.strip() for line in users_file]

with open("tags.txt", "r") as tags_file:
    tags = [line.strip() for line in tags_file]

submissions_per_tags = dict([(tag, 0) for tag in tags])

for user_index, user in enumerate(users):
    api_url = f"https://codeforces.com/api/user.status?handle={user}&from=1"
    response = requests.get(api_url)

    print(f"{'='*50}")
    print(f"User #{user_index + 1}")

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            submissions = data["result"]

            for tag in tags:
                tag_submissions = []

                for submission in submissions:
                    tag_with_spaces = tag.replace("+", " ")

                    if tag_with_spaces in submission["problem"]["tags"]:
                        tag_submissions.append(submission)

                if len(tag_submissions) == 0:
                    continue

                if not os.path.exists(f"submissions/{tag}"):   
                    os.makedirs(f"submissions/{tag}")

                output_file = f"submissions/{tag}/{tag}_{user}_submissions.json"
                with open(output_file, "w") as json_file:
                    json.dump(tag_submissions, json_file, indent=4)

                user_tag_submissions = len(tag_submissions)
                submissions_per_tags[tag] += user_tag_submissions

                print(f"{'-'*50}")
                print(f"{tag} - {user} submissions: {user_tag_submissions}")
                print(f"Total {tag} submissions so far: {submissions_per_tags[tag]}")

        else:
            print("\n~~~~~ Unsuccessful API call ~~~~~\n")
            print(data["comment"])
    else:
        print("\n~~~~~ Error connecting to Codeforces API ~~~~~\n")

with open("submissions/total_tags_submissions.txt", "w") as file:
    file.write("----- TOTAL SUBMISSIONS COLLECTED PER TAG -----\n")
    for tag in tags:
        file.write(f"{tag}: {submissions_per_tags[tag]}\n")
