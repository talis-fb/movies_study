import requests
import csv
import sys
import requests
import os

TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY environment variable is not set")

iterations = 0

def get_movie_id_from_imdb(imdb_id: str) -> str | None:
    global iterations
    iterations += 1

    url = f"{TMDB_BASE_URL}/find/{imdb_id}?external_source=imdb_id&api_key={TMDB_API_KEY}"
    response = requests.get(url, headers={"Authorization": f"Bearer {TMDB_API_KEY}"})
    if response.status_code == 200:
        data = response.json()

        movie_results = data['movie_results']
        if len(movie_results) < 1:
            print(f"{iterations} Err {imdb_id}: {data['movie_results']}", file=sys.stderr)
            return ''

        real_id = data['movie_results'][0]['id']
        print(f"{iterations} Ok {imdb_id}: {data['movie_results'][0]['id']}", file=sys.stderr)

        return real_id
    else:
        print(f"Error fetching id from imdb_id for movie {imdb_id} on TMDb, status: {response.status_code}", file=sys.stderr)
        return None

def main():
    writer = csv.writer(sys.stdout)
    writer.writerow(["imdb_id", "tmdb_id"])

    imdb_ids = [line.strip() for line in sys.stdin if line.strip()]
    for imdb_id_value in imdb_ids:
        tmdb_id = get_movie_id_from_imdb(imdb_id_value)
        if tmdb_id == None:
            return

        if tmdb_id == '':
            continue

        writer.writerow([imdb_id_value, tmdb_id])

if __name__ == "__main__":
    main()


