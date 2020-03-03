from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from importer import daily_exports, tmdb_fetcher, api
from importer import shared_tasks
import json


def fetch_daily_production_companies(request):
	return HttpResponse(daily_exports.fetch_production_companies())


def fetch_daily_keywords(request):
	return HttpResponse(daily_exports.fetch_keywords())


def fetch_daily_persons(request):
	return HttpResponse(daily_exports.fetch_persons())


def fetch_daily_movies(request):
	return HttpResponse(daily_exports.fetch_movies())


def import_persons(request):
    return HttpResponse(tmdb_fetcher.fetch_persons())


def import_keywords(request):
    return HttpResponse(tmdb_fetcher.fetch_keywords())


def import_movies(request):
    return HttpResponse(tmdb_fetcher.fetch_movies())


def autocomplete(request, query):
    return HttpResponse(json.dumps(api.autocomplete(query)))


def search(request, query):
    return HttpResponse(api.search(query))


def health(request):
	return HttpResponse('{"Status": "OK"}')
