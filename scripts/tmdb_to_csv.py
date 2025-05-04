import requests
import csv
import sys
import requests
import json
import os

TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY environment variable is not set")

pages_to_fetch = 100
movie_counter = 1

iterations = 0

def get_movie_details_tmdb(movie_id):
    global iterations
    iterations += 1

    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    response = requests.get(url, headers={"Authorization": f"Bearer {TMDB_API_KEY}"})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching details for movie {movie_id} on TMDb: {response.status_code}", file=sys.stderr)
        return None


def main():
    writer = csv.writer(sys.stdout)
    writer.writerow(["id", "imdb_id","response"])

    ids = [line.strip() for line in sys.stdin if line.strip()]
    for id_value in ids:
        data = get_movie_details_tmdb(id_value)
        if not data:
            return

        imdb_id = data['imdb_id']
        print(f"{iterations} Ok {imdb_id}: {data['id']}", file=sys.stderr)

        writer.writerow([id_value, imdb_id, json.dumps(data)])

if __name__ == "__main__":
    main()


