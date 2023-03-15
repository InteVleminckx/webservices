import requests

from .API_key import KEY


def get_no_of_items(total_items, total_pages, page_no):
    if total_items % total_pages == 0:
        return total_items // total_pages
    else:
        if total_pages == page_no:
            return total_items % (total_pages - 1)
        else:
            return total_items // (total_pages - 1)


def get_popular_movies(amount=None):
    # Eerste keer opvragen voor het bekijken hoeveel pagina's en items er zijn
    page_no: int = 1
    url: str = f'https://api.themoviedb.org/3/movie/popular?api_key={KEY}&page={page_no}'

    # uitvoeren van de request
    response = requests.get(url)

    if response.status_code != 200:
        return False, response  # False duidt aan dat het een error content bevat

    # Verkrijgen van de content
    content = response.json()

    # Verkrijgen van de het aantal pages en movies
    total_pages = content['total_pages']
    total_movies = content['total_results']

    result = {}

    # Als er geen getal is opgegeven dan moeten we alle populaire movies tonen
    if amount is None or amount >= total_movies:
        result['total_pages'] = total_pages
        result['pages'] = {}

        for i in range(page_no, total_pages):
            if i != 1:
                url: str = f'https://api.themoviedb.org/3/movie/popular?api_key={KEY}&page={i}'
                response = requests.get(url)

                if response.status_code != 200:
                    return False, response  # False duidt aan dat het een error content bevat

                # Verkrijgen van de content
                content = response.json()

            movies = content['results']

            all_movies = {}

            for j, movie in enumerate(movies):
                all_movies[j] = {}
                all_movies[j]['id'] = movie['id']
                all_movies[j]['title'] = movie['original_title']

            # page = {'movies': all_movies}

            result['pages'][i] = all_movies

        return True, result

    goal: int = amount

    result['pages'] = {}

    for i in range(page_no, total_pages):

        if i != 1:
            url: str = f'https://api.themoviedb.org/3/movie/popular?api_key={KEY}&page={i}'
            response = requests.get(url)

            if response.status_code != 200:
                return False, response  # False duidt aan dat het een error content bevat

            # Verkrijgen van de content
            content = response.json()

        items = goal

        no_items = get_no_of_items(total_movies, total_pages, i)

        if no_items <= goal:
            goal -= no_items
            items = no_items

        else:
            goal = 0

        movies = content['results']

        all_movies = {}

        for j, movie in enumerate(movies):

            if j == items:
                break

            all_movies[j] = {}
            all_movies[j]['id'] = movie['id']
            all_movies[j]['title'] = movie['original_title']

        # page = {'movies': all_movies}

        result['pages'][i] = all_movies

        if goal <= 0:
            result['total_pages'] = i
            break

    return True, result