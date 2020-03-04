from importer import models


def search(query):
    return list(models.Movie.objects.filter(name=query)[:10].values())


def autocomplete(query):
    return list(models.Movie.objects.filter(name__icontains=query).values('id', 'name')[:5])
