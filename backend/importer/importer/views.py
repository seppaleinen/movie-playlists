from django.shortcuts import render
from django.http import HttpResponse
from importer import daily_exports, tmdb_fetcher


def fetch_daily_production_companies(request):
	return HttpResponse(daily_exports.fetch_production_companies())


def fetch_daily_keywords(request):
	return HttpResponse(daily_exports.fetch_keywords())


def fetch_daily_persons(request):
	return HttpResponse(daily_exports.fetch_persons())


def fetch_daily_movies(request):
	return HttpResponse(daily_exports.fetch_movies())


def import_keywords(request):
    return HttpResponse(tmdb_fetcher.fetch_keywords())


def health(request):
	return HttpResponse("Status: OK")