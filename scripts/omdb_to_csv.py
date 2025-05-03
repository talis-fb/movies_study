import requests
import json
import os
import sys
import csv

OMDB_BASE_URL = 'http://www.omdbapi.com/'
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

if not OMDB_API_KEY:
    raise ValueError("OMDB_API_KEY environment variable is not set")


iterations = 0

def get_movie_details_omdb(imdb_id):
    global iterations
    iterations += 1

    url = f"{OMDB_BASE_URL}?i={imdb_id}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"{iterations} Ok {imdb_id}", file=sys.stderr)
        return response.json()
    else:
        print(f"Error fetching data for IMDb ID {imdb_id} from OMDb", file=sys.stderr)
        return None


def main():
    writer = csv.writer(sys.stdout)
    writer.writerow(["id", "response"])

    ids = [line.strip() for line in sys.stdin if line.strip()]
    for id_value in ids:
        data = get_movie_details_omdb(id_value)
        if not data:
            return

        writer.writerow([id_value, json.dumps(data)])

if __name__ == "__main__":
    main()


