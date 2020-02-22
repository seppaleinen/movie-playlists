from behave import given, when, then
import responses, gzip, io, os
from freezegun import freeze_time
from importer import models
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@given(u'{number_of_movies} unfetched movies')
def given_unfetched_movies(context, number_of_movies):
    for i in range(1, int(number_of_movies) + 1):
        movie = models.Movie()
        movie.id = i
        movie.popularity = 1.2
        movie.save()


@given(u'mocked {method} with {url}, and {body} and {status}, with {content_type}')
def given_mock(context, method, url, body, status, content_type):
    mock = dict()
    mock['method'] = method
    mock['url'] = url
    with open("%s/%s" % (BASE_DIR, body), 'rb') as file:
        mock['body'] = __gzip_string(file.read())
    mock['status'] = int(status)
    mock['content_type'] = content_type
    context.mocks.append(mock)


@given(u'mocked {url} with testdata {body}')
def given_mock(context, url, body):
    mock = dict()
    mock['method'] = 'GET'
    mock['url'] = url
    with open("%s/%s" % (BASE_DIR, body), 'rb') as file:
    	mock['body'] = __gzip_string(file.read())
    mock['status'] = int(200)
    mock['content_type'] = 'application/octet-stream'
    context.mocks.append(mock)


@given(u'mocked {url} with json {body}')
def given_mock(context, url, body):
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
            rsps.add(mock['method'], mock['url'], body=mock['body'], status=mock['status'], content_type=mock['content_type'], stream=True)
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


def __gzip_string(string):
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode="w") as f:
        f.write(string)
    return out.getvalue()

