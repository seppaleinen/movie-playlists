import os, requests, json
from importer import models

api_key = os.getenv('TMDB_API', 'test')


def fetch_keywords():
    for keyword_id in models.KeywordIds.objects.all().values_list('id', flat=True):
        resp = __fetch_keyword_details(keyword_id)
        url = "https://api.themoviedb.org/3/keyword/{keyword_id}/movies?api_key={api_key}&language=en-US&include_adult=false".format(keyword_id=keyword_id, api_key=api_key)
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content)
            page = data['page']
            total_pages = data['total_pages']
            ids = [a['id'] for a in data['results']]
            print("Page: {page) - {total}. Ids: {ids}".format(page=page, total=total_pages, ids=ids))
        else:
            raise Exception("%s - %s" % (response.status_code, response.content))
        
def __fetch_keyword_details(keyword_id, page=1):
    url = "https://api.themoviedb.org/3/keyword/{keyword_id}/movies?api_key={api_key}&language=en-US&include_adult=false&page={page}".format(keyword_id=keyword_id, api_key=api_key, page=page)
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        page = data['page']
        total_pages = data['total_pages']
        ids = [a['id'] for a in data['results']]
        print("Page: {keyword}: {page} - {total}. Ids: {ids}".format(keyword=keyword_id, page=page, total=total_pages, ids=ids))
        #if int(page) < int(total_pages):
        #    return __fetch_keyword_details(keyword_id, ++page)
    else:
        raise Exception("%s - %s" % (response.status_code, response.content))
