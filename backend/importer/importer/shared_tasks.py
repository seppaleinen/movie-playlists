from celery import shared_task
import logging
from importer import models

logger = logging.getLogger(__name__)


@shared_task
def build_something():
    for i in models.KeywordIds.objects.filter(pk=278).all():
        logger.info("Hej: %s" % i)
    return "hej"


@shared_task
def fetch_movie(movie_ids):
    logger.info("Fetching movie ids: %s" % movie_ids)
    return movie_ids


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

