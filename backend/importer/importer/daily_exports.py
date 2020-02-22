import datetime, requests, gzip, json, logging
from importer.models import ProductionCompanyIds, KeywordIds, PersonIds, Movie


logger = logging.getLogger(__name__)


def fetch_all():
    # logger framework doesn't work for crond right now.
    print("Fetching TMDB daily exports")
    print("Production Companies Result: %s" % fetch_production_companies())
    print("Keywords Result: %s" % fetch_keywords())
    print("Persons Result: %s" % fetch_persons())
    print("Movies Result: %s" % fetch_movies())


def fetch_production_companies():
    yesterday = __get_date()
    dict_array = __download("http://files.tmdb.org/p/exports/production_company_ids_{date}.json.gz".format(date=yesterday), 'production_companies.json.gz')
    wrapper = __split_into_create_update_or_delete(ProductionCompanyIds, dict_array)
    return persist(ProductionCompanyIds, wrapper)


def fetch_keywords():
    yesterday = __get_date()
    dict_array = __download("http://files.tmdb.org/p/exports/keyword_ids_{date}.json.gz".format(date=yesterday), 'keywords.json.gz')
    wrapper = __split_into_create_update_or_delete(KeywordIds, dict_array)
    return persist(KeywordIds, wrapper)


def fetch_persons():
    yesterday = __get_date()
    dict_array = __download("http://files.tmdb.org/p/exports/person_ids_{date}.json.gz".format(date=yesterday), 'persons.json.gz')
    wrapper = __split_into_create_update_or_delete(PersonIds, dict_array)
    return persist(PersonIds, wrapper)


def fetch_movies():
    yesterday = __get_date()
    dict_array = __download("http://files.tmdb.org/p/exports/movie_ids_{date}.json.gz".format(date=yesterday), 'movies.json.gz')
    wrapper = __split_into_create_update_or_delete(Movie, dict_array)
    return persist(Movie, wrapper)


def persist(entity, wrapper):
    try:
        logger.info('Persisting...')
        for chunk in __chunks(wrapper['all_new_entities'], 100):
            entity.objects.bulk_create(chunk)
        logger.info("Deleting unfetched movies not in tmdb anymore")
        for id_to_delete in wrapper['ids_to_delete']:
            to_be_deleted = entity.objects.get(pk=id_to_delete)
            to_be_deleted.deleted = True
            to_be_deleted.save()
        return "Imported: %s, and deleted: %s, out of: %s" % (len(wrapper['all_new_entities']), len(wrapper['ids_to_delete']), wrapper['total_size'])
    except Exception as e:
        logger.error("Error: %s" % e)
        return "Exception: %s" % e



def __download(url, tmp_file):
    response = requests.get(url)
    if response.status_code == 200:
        with open(tmp_file, 'wb') as f:
            f.write(response.content)
        contents = __unzip_file(tmp_file)
        dict_array = []
        logger.info("Downloading {url}".format(url=url))
        for i in contents:
            try:
                if not i: # New str.split('\n') passes through empty lines which str.splitlines took care of.
                    pass
                else:
                    loaded = json.loads(i, strict=False)
                    if 'adult' in loaded and loaded['adult'] is False:
                        dict_array.append(loaded)
                    elif 'video' not in loaded:
                        dict_array.append(loaded)
            except Exception as e:
                logger.error("Could not parse json string: %s" % i)

        return dict_array
    else:
        return []


def __split_into_create_update_or_delete(entity, dicts):
    wrapper = dict()
    already_persisted_ids = set(entity.objects.all().values_list('id', flat=True))
    all_unfetched_ids = set(entity.objects.filter(fetched=False).all().values_list('id', flat=True))
    all_ids = set()
    wrapper['all_new_entities'] = []
    logger.info("Splitting into create/delete")
    for dic in dicts:
        all_ids.add(dic['id'])
        if dic['id'] not in already_persisted_ids:
            wrapper['all_new_entities'].append(entity.create(dic))
    wrapper['ids_to_delete'] = (all_unfetched_ids.difference(all_ids))
    wrapper['total_size'] = len(dicts)
    return wrapper


def __unzip_file(file_name):
    f = gzip.open(file_name, 'rt', encoding='utf-8')
    file_content = f.read()
    f.close()
    # there are names with line separators (<U+2028>) and line paragraphs (<U+2029>) which doesn't work so well with splitlines.
    return file_content.split('\n') 


def __get_date():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    return yesterday.strftime("%m_%d_%Y")


def __chunks(__list, n):
    """Yield successive n-sized chunks from list."""
    for i in range(0, len(__list), n):
        yield __list[i:i + n]


def __log_progress(iterable, message, length=None):
    datetime_format = "%Y-%m-%d %H:%M:%S"
    count = 1
    percentage = 0
    total_count = length if length else len(iterable)
    for i in iterable:
        temp_perc = int(100 * count / total_count)
        if percentage != temp_perc:
            percentage = temp_perc
            logger.info("{time} - {message} data handling in progress - {percentage}%".format(
                time=datetime.datetime.now().strftime(datetime_format),
                message=message, 
                percentage=percentage))
        count += 1
        yield i
