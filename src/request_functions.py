import requests

from .API_info import KEY, BASE_URL
from src.database import Database

db = Database()


def get_no_of_items(total_items, total_pages, page_no):
    if total_items % total_pages == 0:
        return total_items // total_pages
    else:
        if total_pages == page_no:
            return total_items % (total_pages - 1)
        else:
            return total_items // (total_pages - 1)


def get_movies():
    # Eerste keer opvragen voor het bekijken hoeveel pagina's en items er zijn
    url: str = f'{BASE_URL}/discover/movie?api_key={KEY}'

    # uitvoeren van de request
    response = requests.get(url + '&page=1')

    if not response.ok:
        return {"found": False, "response": response}

    # Verkrijgen van de content
    content = response.json()

    return concatenate_pages(content, url, amount=20)


def get_popular_movies(amount=10):
    # Eerste keer opvragen voor het bekijken hoeveel pagina's en items er zijn
    url: str = f'{BASE_URL}/discover/movie?api_key={KEY}&sort_by=popularity.desc'

    # uitvoeren van de request
    response = requests.get(url + '&page=1')

    if not response.ok:
        return {"found": False, "response": response}

    # Verkrijgen van de content
    content = response.json()

    return concatenate_pages(content, url, amount)


def concatenate_pages(content, url, amount=None, number_genres=None):
    # Verkrijgen van de het aantal pages en movies
    total_pages = content['total_pages']
    total_movies = content['total_results']

    if amount is None:
        amount = total_movies

    result = {'movies': {}}

    if db.deleted_all:
        return {"found": True, "response": result}

    movie_count: int = 0

    for i in range(1, total_pages):

        if i != 1:
            url_: str = url + f'&page={i}'
            response = requests.get(url_)

            if not response.ok:
                return {"found": False, "response": response}

            # Verkrijgen van de content
            content = response.json()

        no_items = get_no_of_items(total_movies, total_pages, i)

        movies = content['results']

        for j, movie in enumerate(movies):

            movie_id = movie['id']

            if db.movie_is_deleted(movie_id):
                continue

            if number_genres is not None:
                if number_genres != len(movie['genre_ids']):
                    continue

            if j == no_items or movie_count == amount:
                break

            result['movies'][movie_count] = {"id": movie_id, "title": movie['original_title'],
                                             "liked": db.movie_is_liked(movie_id)}

            movie_count += 1

        if movie_count == amount:
            break

    return {"found": True, "response": result}


def movie_exists(movie_id: int) -> bool:
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={KEY}')

    return response.status_code == 200


def get_movie_name(movie_id: int) -> str or None:
    response = requests.get(f'{BASE_URL}/movie/{movie_id}?api_key={KEY}&language=en-US')

    if response.ok:
        title = response.json()['original_title']

        return title

    return None


def get_movie_genres(movie_id: int) -> list[int] or None:
    response = requests.get(f'{BASE_URL}/movie/{movie_id}?api_key={KEY}')

    if response.ok:
        movie_genres = [genre['id'] for genre in response.json()['genres']]
        return movie_genres

    return None


def get_matching_movies_genre(genres: list[int]):
    url: str = f'{BASE_URL}/discover/movie?api_key={KEY}&with_genres={",".join(str(genre_id) for genre_id in genres)}'

    matching_movies_response = requests.get(url + '&page=1')

    result = concatenate_pages(matching_movies_response.json(), url, amount=20, number_genres=len(genres))

    if result['found']:
        return result['response']

    return None


def get_runtime_movie(movie_id: int) -> int or None:
    response = requests.get(f'{BASE_URL}/movie/{movie_id}?api_key={KEY}')

    if response.ok:
        return response.json()['runtime']

    return None


def get_similar_runtime_movies(runtime: int) -> list or None:
    url: str = f'{BASE_URL}/discover/movie?api_key={KEY}&with_runtime.gte={runtime - 10}&with_runtime.lte={runtime + 10}'

    similar_movies_response = requests.get(url + '&page=1')

    result = concatenate_pages(similar_movies_response.json(), url, amount=20)

    if result['found']:
        return result['response']

    return None


def get_cast_movie(movie_id: int) -> list or None:
    response = requests.get(f'{BASE_URL}/movie/{movie_id}/credits?api_key={KEY}')

    if response.ok:
        return response.json()['cast']

    return None


def get_overlapping_actors(cast):
    # Extract the first two actors from the cast
    actors_id = [actor['id'] for actor in cast[:2]]

    url: str = f'{BASE_URL}/discover/movie?api_key={KEY}&with_cast={actors_id[0]},{actors_id[1]}'

    overlapping_actors_response = requests.get(url + '&page=1')

    result = concatenate_pages(overlapping_actors_response.json(), url, amount=20)

    if result['found']:
        return result['response']

    return None


def get_average_vote(movie_id: int) -> float or None:
    response = requests.get(f'{BASE_URL}/movie/{movie_id}?api_key={KEY}')

    if response.ok:
        return response.json()['vote_average']

    return None
