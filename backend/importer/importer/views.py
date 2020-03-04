from django.http import HttpResponse, JsonResponse
from importer import daily_exports, tmdb_fetcher, api


def fetch_dailies(request):
    fetch_daily_movies(request)
    fetch_daily_keywords(request)
    fetch_daily_production_companies(request)
    fetch_daily_persons(request)
    fetch_genres(request)
    return HttpResponse("Imported all dailies")


def fetch_daily_production_companies(request):
    return HttpResponse(daily_exports.fetch_production_companies())


def fetch_daily_keywords(request):
    return HttpResponse(daily_exports.fetch_keywords())


def fetch_daily_persons(request):
    return HttpResponse(daily_exports.fetch_persons())


def fetch_daily_movies(request):
    return HttpResponse(daily_exports.fetch_movies())


def fetch_genres(request):
    return HttpResponse(daily_exports.fetch_genres())


def import_persons(request):
    return HttpResponse(tmdb_fetcher.fetch_persons())


def import_keywords(request):
    return HttpResponse(tmdb_fetcher.fetch_keywords())


def import_movies(request):
    return HttpResponse(tmdb_fetcher.fetch_movies())


def autocomplete(request, query):
    return JsonResponse(api.autocomplete(query), safe=False)


def search(request, query):
    return JsonResponse(api.search(query), safe=False)


def health(request):
    return HttpResponse('{"Status": "OK"}')
