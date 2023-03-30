import requests

from .API_info import KEY, BASE_URL
from src.database import Database

db = Database()


def get_no_of_items(total_items, total_pages, page_no):
    """
    Berekent het aantal films dat op de pagina staan.
    """
    if total_items % total_pages == 0:
        return total_items // total_pages
    else:
        if total_pages == page_no:
            return total_items % (total_pages - 1)
        else:
            return total_items // (total_pages - 1)


def get_movies():
    """
    Geeft alle films terug (voor tijd te besparen is de limiet op 20 gezet)
    """
    # Eerste keer opvragen voor het bekijken hoeveel pagina's en items er zijn
    url: str = f'{BASE_URL}/discover/movie?api_key={KEY}'

    # uitvoeren van de request
    response = requests.get(url + '&page=1')

    if not response.ok:
        return {"found": False, "response": response}

    # Verkrijgen van de content
    content = response.json()

    return concatenate_pages(content, url, amount=20)


def get_popular_movies(amount=20):
    """
    Geeft de populaire films terug voor een gegeven waarde.
    Als deze niet meegeven is, is dit 20.
    :param amount: de gegeven waarde die het aantal films bepaald.
    """
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
    """
    Vraagt telkens een nieuwe pagina op en voegt alle films samen tot we aan het gevraagde aantal films komen.
    """
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
    """
    Geeft weer of er een film bestaat voor een gegeven movie id.
    :param movie_id: de movie id die we gaan controleren.
    """
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={KEY}')

    return response.status_code == 200


def get_movie_name(movie_id: int) -> str or None:
    """
    Geeft de naam van een film terug voor een gegeven movie id.
    :param movie_id: De movie id waarvan we de filmnaam willen.
    """
    response = requests.get(f'{BASE_URL}/movie/{movie_id}?api_key={KEY}&language=en-US')

    if response.ok:
        title = response.json()['original_title']

        return title

    return None


def get_movie_genres(movie_id: int) -> list[int] or None:
    """
    Geeft alle genres van een film terug.
    :param movie_id: de id van de film waarvan we de genres willen opvragen.
    """
    response = requests.get(f'{BASE_URL}/movie/{movie_id}?api_key={KEY}')

    if response.ok:
        movie_genres = [genre['id'] for genre in response.json()['genres']]
        return movie_genres

    return None


def get_matching_movies_genre(genres: list[int]):
    """
    Vraagt alle films op die exact dezelfde genres heeft als de gegeven genres. (Ook limiet op 20 films)
    :param genres: de gegeven genres waarvan we de films willen verkrijgen.
    """
    url: str = f'{BASE_URL}/discover/movie?api_key={KEY}&with_genres={",".join(str(genre_id) for genre_id in genres)}'

    matching_movies_response = requests.get(url + '&page=1')

    result = concatenate_pages(matching_movies_response.json(), url, amount=20, number_genres=len(genres))

    if result['found']:
        return result['response']

    return None


def get_runtime_movie(movie_id: int) -> int or None:
    """
    Geeft de runtime van een film terug.
    :param movie_id: de id van de film waarvan we de runtime willen verkrijgen.
    """
    response = requests.get(f'{BASE_URL}/movie/{movie_id}?api_key={KEY}')

    if response.ok:
        return response.json()['runtime']

    return None


def get_similar_runtime_movies(runtime: int) -> list or None:
    """
    Vraagt alle films op die gelijkwaarde speeltijd heeft als de gegeven speeltijd. (Ook limiet op 20 films)
    :param runtime: de gegeven speeltijd waarvan we de films willen verkrijgen.
    """
    url: str = f'{BASE_URL}/discover/movie?api_key={KEY}&with_runtime.gte={runtime - 10}&with_runtime.lte={runtime + 10}'

    similar_movies_response = requests.get(url + '&page=1')

    result = concatenate_pages(similar_movies_response.json(), url, amount=20)

    if result['found']:
        return result['response']

    return None


def get_cast_movie(movie_id: int) -> list or None:
    """
    Geeft de cast terug van een gegeven film.
    :param movie_id: de id van de film waarvan we de cast willen.
    """
    response = requests.get(f'{BASE_URL}/movie/{movie_id}/credits?api_key={KEY}')

    if response.ok:
        return response.json()['cast']

    return None


def get_overlapping_actors(cast):
    """
    Geeft alle films terug die overlappende acteurs hebben, gegeven de acteurs.
    :param cast: de acteurs die we willen gebruiken voor overlappende films te vinden.
    """
    # Extract the first two actors from the cast
    actors_id = [actor['id'] for actor in cast[:2]]

    url: str = f'{BASE_URL}/discover/movie?api_key={KEY}&with_cast={actors_id[0]},{actors_id[1]}'

    overlapping_actors_response = requests.get(url + '&page=1')

    result = concatenate_pages(overlapping_actors_response.json(), url, amount=20)

    if result['found']:
        return result['response']

    return None


def get_average_vote(movie_id: int) -> float or None:
    """
    Geeft het gemiddelde aantal stemmen van een gegeven film.
    :param movie_id: de id van de film waarvan we de stemmen willen verkrijgen.
    """
    response = requests.get(f'{BASE_URL}/movie/{movie_id}?api_key={KEY}')

    if response.ok:
        return response.json()['vote_average']

    return None
