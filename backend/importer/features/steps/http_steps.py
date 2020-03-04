from behave import given, when, then
import responses
import gzip
import io
import os
from freezegun import freeze_time
from importer import models
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@given(u'{number_of_movies} unfetched movies')
def given_unfetched_movies(context, number_of_movies):
    for i in range(1, int(number_of_movies) + 1):
        models.Movie.objects.create(id=i, popularity=1.2)


@given(u'keyword with id {keyword_id}')
def given_keyword(context, keyword_id):
    models.KeywordIds.objects.create(id=keyword_id)


@given(u'{number_of_movies} fetched movies')
def given_fetched_movies(context, number_of_movies):
    for i in range(1, int(number_of_movies) + 1):
        models.Movie.objects.create(id=i, popularity=1.2, fetched=True)


@given(u'movie exists with name "{movie_name}"')
def given_movie_with_name(context, movie_name):
    models.Movie.objects.create(
        name=movie_name,
        popularity=0.0,
        original_language=models.Language.objects.get(pk='en'))


@given(u'mocked {url} with gzipped {body}')
def given_mock2(context, url, body):
    mock = dict()
    mock['method'] = 'GET'
    mock['url'] = url
    with open("%s/%s" % (BASE_DIR, body), 'rb') as file:
        mock['body'] = __gzip_string(file.read())
    mock['status'] = int(200)
    mock['content_type'] = 'application/octet-stream'
    context.mocks.append(mock)


@given(u'mocked {url} with json {body}')
def given_mock3(context, url, body):
    mock = dict()
    mock['method'] = 'GET'
    mock['url'] = url
    with open("%s/%s" % (BASE_DIR, body), 'rt') as file:
        mock['body'] = file.read()
    mock['status'] = int(200)
    mock['content_type'] = 'application/json'
    context.mocks.append(mock)


@when(u'I call "{url}"')
def use_django_client(context, url):
    with responses.RequestsMock() as rsps:
        for mock in context.mocks:
            rsps.add(mock['method'], mock['url'], body=mock['body'],
                    status=mock['status'],
                    content_type=mock['content_type'],
                    stream=True)
        with freeze_time("2020-02-18"):
            context.response = context.test.client.get(url)


@then(u'the server should return status {status_code}')
def it_should_be_successful(context, status_code):
    context.test.assertEquals(context.response.status_code, int(status_code))


@then(u'a response like "{expected_message}"')
def response_be_like(context, expected_message):
    context.test.assertEquals(context.response.content.decode('utf-8'), expected_message)


@then(u'{expected_number_movies} movies should have been imported')
def movies_should_be_imported(context, expected_number_movies):
    context.test.assertEquals(models.Movie.objects.filter(fetched=True).count(), int(expected_number_movies))


@then(u'movie_id={movie_id} should have a keyword={expected_keyword} associated to it')
def then_keyword_should_be_connected_to_movie(context, movie_id, expected_keyword):
    all_keywords_in_movie = models.Movie.objects.get(pk=movie_id).keywords.all()
    context.test.assertTrue(expected_keyword in keyword.name for keyword in all_keywords_in_movie)


def __gzip_string(string):
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode="w") as f:
        f.write(string)
    return out.getvalue()
