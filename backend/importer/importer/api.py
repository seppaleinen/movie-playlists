from importer import models
import json


def search(query):
    return models.Movie.objects.filter(name=query)


def autocomplete(query):
    data = []
    for movie in models.Movie.objects.filter(name__icontains=query).only('id', 'name')[:5]:
        data.append({'id':movie.id, 'name':movie.name})
    return json.dumps(data)
