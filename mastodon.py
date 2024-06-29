import requests as request
import json
import time
import csv
import os

MASTODON_API = os.environ.get('MASTODON_API')

if not MASTODON_API:
	print("Error: Mastodon API token not found!\nSee manual for adding token.")
	exit()

print("Mastodon API Token found!")

URLS = { "Mastodon": "https://mastodon.social/api/v2/search"}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
					'Authorization': f'Bearer {MASTODON_API}'}
username_input = input("Enter username: ").replace(" ", "+") # FIXME: Input


r = request.get(URLS["Mastodon"], f"q={username_input}&type=accounts", headers=headers)
print(r.url)
text = r.text
text_json = json.loads(text) # convert to json object
profile = text_json["accounts"]

output_file = open("out.csv", "w") # FIXME Input
csv_writer = csv.writer(output_file)

r = request.get(URLS["Mastodon"], f"q={username_input}&type=accounts", headers=headers)
text_json = json.loads(r.text)
text_json = text_json["accounts"]

count = 0
# Write data in csv file
for profile in text_json:
		if count == 0: # write headers
				header = profile.keys()
				csv_writer.writerow(header)
				count += 1
		csv_writer.writerow(profile.values())
