from __future__ import unicode_literals

from django.db import models

class ProductionCompanyIds(models.Model):
    id = models.IntegerField(db_index=True, primary_key=True)
    name = models.TextField()
    fetched = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=['id'], name='production_company_pk_index')]
        db_table = "production_company_ids"

    def create(dict_object):
        this = ProductionCompanyIds()
        this.id = dict_object['id']
        this.name = dict_object['name']
        return this

    def __str__(self):
        return "id:{id}, name:{name}, fetched={fetched}, deleted={deleted}".format(id=self.id, name=self.name, fetched=self.fetched, deleted=self.deleted)


class KeywordIds(models.Model):
    id = models.IntegerField(db_index=True, primary_key=True)
    name = models.TextField()
    fetched = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=['id'], name='keyword_ids_pk_index')]
        db_table = "keyword_ids"

    def create(dict_object):
        this = KeywordIds()
        this.id = dict_object['id']
        this.name = dict_object['name']
        return this

    def __str__(self):
        return "id:{id}, name:{name}, fetched={fetched}, deleted={deleted}".format(id=self.id, name=self.name, fetched=self.fetched, deleted=self.deleted)


class PersonIds(models.Model):
    id = models.IntegerField(db_index=True, primary_key=True)
    name = models.TextField()
    popularity = models.DecimalField(decimal_places=3, max_digits=10)
    fetched = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=['id'], name='person_ids_pk_index')]
        db_table = "person_ids"

    def create(dict_object):
        this = PersonIds()
        this.id = dict_object['id']
        this.name = dict_object['name']
        this.popularity = dict_object['popularity']
        return this

    def __str__(self):
        return "id:{id}, name:{name}, popularity={popularity}, fetched={fetched}, deleted={deleted}".format(
        	id=self.id, 
        	name=self.name, 
        	popularity=self.popularity, 
        	fetched=self.fetched, 
        	deleted=self.deleted)


class Movie(models.Model):
    id = models.IntegerField(db_index=True, primary_key=True)
    name = models.TextField(max_length=500)
    popularity = models.DecimalField(decimal_places=3, max_digits=10)
    fetched = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    budget = models.BigIntegerField(null=True, blank=True)
    imdb_id = models.TextField(max_length=30, null=True, db_index=True, unique=True)
    original_language = models.TextField(max_length=30, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    poster_path = models.TextField(max_length=40, null=True, blank=True)
    release_date = models.TextField(max_length=10, null=True, blank=True)
    revenue = models.BigIntegerField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    vote_average = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True)
    imdb_vote_average = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    imdb_vote_count = models.IntegerField(null=True, blank=True)
    raw_response = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=['id'], name='movie_pk_index')]
        db_table = "movie"

    def create(dict_object):
        this = Movie()
        this.id = dict_object['id']
        this.name = dict_object['original_title']
        this.popularity = dict_object['popularity']
        return this

    def append_info(self, fetched_movie):
        self.fetched = True
        self.raw_response = fetched_movie
        self.budget = fetched_movie['budget']
        self.imdb_id = fetched_movie['imdb_id'] if fetched_movie['imdb_id'] is not '' else None
        self.original_language = fetched_movie['original_language']
        self.overview = fetched_movie['overview']
        self.poster_path = fetched_movie['poster_path']
        self.release_date = fetched_movie['release_date']
        self.revenue = fetched_movie['revenue']
        self.runtime = fetched_movie['runtime']
        self.vote_average = fetched_movie['vote_average']
        self.vote_count = fetched_movie['vote_count']

        for fetch_alt_title in fetched_movie['alternative_titles']['titles']:
            title = fetch_alt_title['title'] if len(fetch_alt_title['title']) < 500 else (fetch_alt_title['title'][:498] + '..')
            alt_title = AlternativeTitle(movie_id=self.id,iso_3166_1=fetch_alt_title['iso_3166_1'],title=title,type=fetch_alt_title['type'])
            alt_title.save()
            self.alternative_titles.add(alt_title)
        for fetch_spoken_lang in fetched_movie['spoken_languages']:
            self.spoken_languages.add(Language.objects.get(iso_639_1=fetch_spoken_lang['iso_639_1']))
        for fetch_prod_country in fetched_movie['production_countries']:
            self.production_countries.add(Country.objects.get(iso_3166_1=fetch_prod_country['iso_3166_1']))

        return self


class Genre(models.Model):
    movies = models.ManyToManyField(Movie, related_name='genres')
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return "id:{id}, name:{name}".format(id=self.id, name=self.name)

    class Meta:
        indexes = [models.Index(fields=['id'], name='genre_pk_index')]
        db_table = "genre"



class AlternativeTitle(models.Model):
    movie = models.ForeignKey(Movie, related_name='alternative_titles', on_delete=models.CASCADE, db_index=True)
    iso_3166_1 = models.CharField(max_length=20)
    title = models.CharField(max_length=500)
    type = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return "iso:{iso}, title:{title}".format(iso=self.iso_3166_1, title=self.title)

    class Meta:
        db_table = "alternative_title"


class Country(models.Model):
    movies = models.ManyToManyField(Movie, related_name='production_countries')
    iso_3166_1 = models.CharField(primary_key=True, max_length=5, unique=True)
    name = models.CharField(max_length=50)
    native_name = models.TextField()

    class Meta:
        indexes = [models.Index(fields=['iso_3166_1'], name='iso_3166_1_pk_index')]
        db_table = "country"

    def __str__(self):
        return "iso:{iso}, name:{name}".format(iso=self.iso_3166_1, name=self.name)


class Language(models.Model):
    iso_639_1 = models.CharField(primary_key=True, max_length=5, unique=True)
    name = models.TextField()
    native_name = models.TextField()
    countries = models.ManyToManyField(Country, related_name="languages")
    movies = models.ManyToManyField(Movie, related_name='spoken_languages')

    class Meta:
        indexes = [models.Index(fields=['iso_639_1'], name='iso_639_1_pk_index')]
        db_table = "language"

