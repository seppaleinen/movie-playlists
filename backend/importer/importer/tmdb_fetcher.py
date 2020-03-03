import os, requests, json, logging
from importer import models, shared_tasks

api_key = os.getenv('TMDB_API', 'test')
logger = logging.getLogger(__name__)

def fetch_keywords():
    for id in models.KeywordIds.objects.filter(fetched=False, deleted=False).values_list('id', flat=True):
        shared_tasks.fetch_keyword.delay(keyword_id=id)
    return "All keywords in queue"


def fetch_movies():
    movies = ((id,) for id in models.Movie.objects.filter(fetched=False, deleted=False).values_list('id', flat=True))
    shared_tasks.fetch_movie.chunks(movies, 99).group().delay()
    return "All is in queue"


def fetch_persons():
    persons = ((id,) for id in models.PersonIds.objects.filter(fetched=False, deleted=False).values_list('id', flat=True))
    shared_tasks.fetch_person.chunks(persons, 99).group().delay()
    return "All persons in queue"


def __fetch_keyword_details(keyword_id, page=1):
    url = "https://api.themoviedb.org/3/discover/movie"\
        "?api_key={api_key}"\
        "&language=en-US"\
        "&sort_by=popularity.desc"\
        "&include_adult=false"\
        "&include_video=false"\
        "&page={page}"\
        "&with_keywords={keyword_id}".format(keyword_id=keyword_id, api_key=api_key, page=page)
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        page = data['page']
        total_pages = data['total_pages']
        ids = [a['id'] for a in data['results']]
        logger.info("Keyword: {keyword}: Page: {page} - {total}. Ids: {ids}".format(keyword=keyword_id, page=page, total=total_pages, ids=ids))
        yield {"keyword_id": keyword_id, "movie_ids": ids}
        if int(page) < int(total_pages):
            yield from __fetch_keyword_details(keyword_id, int(page) + 1)
    else:
        logger.error("Could not get response calling %s" % url)
        raise Exception("%s - %s" % (response.status_code, response.content))
