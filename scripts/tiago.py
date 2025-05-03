import requests
import json
import os
import time

TMDB_API_KEY = ''
OMDB_API_KEY = ''
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
OMDB_BASE_URL = 'http://www.omdbapi.com/'
pages_to_fetch = 100
movie_counter = 1

SAVE_FOLDER = 'movies'
os.makedirs(SAVE_FOLDER, exist_ok=True)

def get_movie_details_tmdb(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching details for movie {movie_id} on TMDb")
        return None

def get_movie_details_omdb(imdb_id):
    url = f"{OMDB_BASE_URL}?i={imdb_id}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for IMDb ID {imdb_id} from OMDb")
        return None


for page in range(1, pages_to_fetch + 1):
    url = f"{TMDB_BASE_URL}/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page={page}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        for movie in data['results']:
            movie_id = movie['id']

            tmdb_details = get_movie_details_tmdb(movie_id)
            if not tmdb_details:
                continue

            imdb_id = tmdb_details.get('imdb_id')
            if not imdb_id:
                print(f"Movie {movie['title']} without imdb_id, skipping..")
                continue

            omdb_details = get_movie_details_omdb(imdb_id)
            if not omdb_details or omdb_details.get('Response') == 'False':
                print(f"Error or not found in OMDb for {imdb_id}")
                continue

            combined_data = {
                'tmdb': tmdb_details,
                'omdb': omdb_details
            }

            filename = f"movie_{movie_counter}.json"
            filepath = os.path.join(SAVE_FOLDER, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(combined_data, f, ensure_ascii=False, indent=4)

            print(f"Saved {filename} ({movie['title']})")
            movie_counter += 1

            time.sleep(0.2)

    else:
        print(f"Error when fetching page {page}: {response.status_code}")

print(f"\Done! We have collected {movie_counter-1} movies and saved them in '{SAVE_FOLDER}/'")
