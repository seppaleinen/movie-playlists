from celery import shared_task
import logging, os, requests, json
from importer import models

logger = logging.getLogger(__name__)
api_key = os.getenv('TMDB_API', 'test')


@shared_task(bind=True, max_retries=3)
def fetch_movie(self, movie_id):
    logger.info("Fetching movie id: %s" % movie_id)
    movie = models.Movie.objects.get(pk=movie_id)
    try:
        movie = movie.append_info(__fetch_movie_info(movie_id))
        movie.save()
        return movie_id
    except Exception as exc:
        self.retry(exc=exc, countdown=60)


def __fetch_movie_info(id):
    url = "https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US&append_to_response=alternative_titles,keywords,external_ids,images".format(movie_id=id, api_key=os.getenv('TMDB_API', 'test'))
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.content)
    elif response.status_code == 404:
        logger.info("Movie: %s has been removed." % id)
    else:
        logger.error("Could not fetch data for movie_id=%s" % id)
        raise Exception("%s - %s" % (response.status_code, response.content))


@shared_task
def fetch_keyword(keyword_id):
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

