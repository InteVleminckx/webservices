import requests

from .API_info import KEY, BASE_URL


def get_no_of_items(total_items, total_pages, page_no):
    if total_items % total_pages == 0:
        return total_items // total_pages
    else:
        if total_pages == page_no:
            return total_items % (total_pages - 1)
        else:
            return total_items // (total_pages - 1)


def get_popular_movies(amount=10):
    # Eerste keer opvragen voor het bekijken hoeveel pagina's en items er zijn
    url: str = f'{BASE_URL}/movie/popular?api_key={KEY}'

    # uitvoeren van de request
    response = requests.get(url + '&page=1')

    if not response.ok:
        return {"found": False, "response": response}

    # Verkrijgen van de content
    content = response.json()

    return concatenate_pages(content, url, amount)


def concatenate_pages(content, url, amount=None):
    # Verkrijgen van de het aantal pages en movies
    total_pages = content['total_pages']
    total_movies = content['total_results']

    if amount is None:
        amount = total_movies

    result = {'movies': {}}

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

            if j == no_items or movie_count == amount:
                break

            result['movies'][movie_count] = {}
            result['movies'][movie_count] = movie['id']
            result['movies'][movie_count] = movie['original_title']

            movie_count += 1

        if movie_count == amount:
            break

    return {"found": True, "response": result}


def get_movie_id(movie_name: str) -> int or None:
    response = requests.get(f'{BASE_URL}/search/movie?api_key={KEY}&query={movie_name}')

    if response.ok:
        results = response.json()['results']
        if len(results) > 0:
            return results[0]['id']

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

    result = concatenate_pages(matching_movies_response.json(), url)

    if result['found']:
        return result['response']

    return None
