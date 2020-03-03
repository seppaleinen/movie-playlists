from celery import shared_task
import logging, os, requests, json
from importer import models

logger = logging.getLogger(__name__)
    

@shared_task(bind=True, max_retries=3)
def fetch_movie(self, movie_id):
    logger.info("Fetching movie id: %s" % movie_id)
    movie = models.Movie.objects.get(pk=movie_id)
    try:
        url = "https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US&append_to_response=alternative_titles,keywords,external_ids,images".format(movie_id=id, api_key=os.getenv('TMDB_API', 'test'))
        response = requests.get(url)
        if response.status_code == 200:
            movie = movie.append_info(json.loads(response.content))
            movie.save()
        elif response.status_code == 404:
            logger.info("Movie: %s has been removed." % id)
            movie.deleted = True
            movie.save()
        else:
            logger.error("Unknown error fetching movie_id=%s, %s" % (id, response.content))
    except requests.exceptions.RequestException as exc:
        logger.error("Error. Retrying later. %s" % exc)
        self.retry(exc=exc, countdown=60)
    except Exception as exc:
        logger.error("Unknown error for movie_id=%s. %s" % (movie_id, exc))


@shared_task(bind=True, max_retries=3)
def fetch_person(self, person_id):
    logger.info("Fetching person id: %s" % person_id)
    try:
        person = models.PersonId.objects.get(pk=person_id)
    except requests.exceptions.RequestException as exc:
        logger.error("Error. Retrying later. %s" % exc)
        self.retry(exc=exc, countdown=60)
    except Exception as exc:
        logger.error("Error. %s" % exc)


@shared_task(bind=True, max_retries=3)
def fetch_keyword(self, keyword_id, page=1):
    api_key = os.getenv('TMDB_API', 'test')
    unformatted_url = "https://api.themoviedb.org/3/discover/movie"\
        "?api_key={api_key}"\
        "&language=en-US"\
        "&sort_by=popularity.desc"\
        "&include_adult=false"\
        "&include_video=false"\
        "&page={page}"\
        "&with_keywords={keyword_id}"

    response = requests.get(unformatted_url.format(keyword_id=keyword_id, api_key=api_key, page=page))
    if response.status_code == 200:
        data = json.loads(response.content)
        total_pages = data['total_pages']
        ids = [result['id'] for result in data['results']]
        logger.info("Keyword: {keyword}: Page: {page} - {total}. Ids: {ids}".format(keyword=keyword_id, page=data['page'], total=total_pages, ids=ids))
        keyword = models.KeywordIds.objects.get(pk=keyword_id)
        for movie in models.Movie.objects.filter(pk__in=ids, fetched=True):
            movie.keywords.add(keyword)
            movie.save()

        if int(page) < int(total_pages):
            fetch_keyword(keyword_id=keyword_id, page=int(page) + 1)
    else:
        logger.error("Could not get response calling %s" % url)
        raise Exception("%s - %s" % (response.status_code, response.content))

