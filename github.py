import requests as request
import json
import time
import csv

URLS = { "Github": "https://github.com/search"}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
username_input = input("Enter username: ").replace(" ", "+") # FIXME: Input


r = request.get(URLS["Github"], f"q={username_input}&type=users", headers=headers)
print(r.url)
text = r.text
text_json = json.loads(text) # convert to json object
page_count = text_json["payload"]["page_count"] # Get page count
result_count = text_json["payload"]["result_count"] # Get result count
profile = text_json["payload"]["results"]

print(f"Page count: {page_count}")
print(f"Result count: {result_count}")
output_file = open("out.csv", "w") # FIXME Input
csv_writer = csv.writer(output_file)

for page in range(1,page_count+1):
    r = request.get(URLS["Github"], f"q={username_input}&type=users&p={page}", headers=headers)
    if r.status_code == 429:
        print("Github API rate limited Reached !! ... retrying in 60 seconds")
        page = page-2
        time.sleep(40)
        print("resuming :)")
    else:
        text_json = json.loads(r.text)
        text_json = text_json["payload"]["results"]
        count = 0

        # Write data in csv file
        for profile in text_json:
            if count == 0: # write headers
                header = profile.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(profile.values())
        time.sleep(2)
