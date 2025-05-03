import requests
import csv
import sys
import requests
import json
import os

TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_API_KEY = os.getenv('OMDB_API_KEY')

if not TMDB_API_KEY:
    raise ValueError("OMDB_API_KEY environment variable is not set")

pages_to_fetch = 100
movie_counter = 1

iterations = 0

def get_movie_id_from_imdb(imdb_id) -> str | None:
    global iterations
    iterations += 1

    url = f"{TMDB_BASE_URL}/find/{imdb_id}?external_source=imdb_id&api_key={TMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        real_id = data['movie_results'][0]['id']
        return real_id
    else:
        print(f"Error fetching id from imdb_id for movie {imdb_id} on TMDb")
        return None

def get_movie_details_tmdb(movie_id):
    global iterations
    iterations += 1

    url = f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching details for movie {movie_id} on TMDb")
        return None


def main():
    writer = csv.writer(sys.stdout)
    writer.writerow(["id", "response"])

    imdb_ids = [line.strip() for line in sys.stdin if line.strip()]
    for imdb_id_value in imdb_ids:
        real_id = get_movie_id_from_imdb(imdb_id_value)
        if not real_id:
            return

        data = get_movie_details_tmdb(real_id)
        if not data:
            return

        writer.writerow([id_value, json.dumps(data)])

if __name__ == "__main__":
    main()


