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

    def append_info(self, json):
        self.fetched = True
        self.imdb_id = json['imdb_id']
        return self


class Genre(models.Model):
    movies = models.ManyToManyField(Movie, related_name='genres')
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

    def __str__(self):
        return "id:{id}, name:{name}".format(id=self.id, name=self.name)


class SpokenLanguage(models.Model):
    movies = models.ManyToManyField(Movie, related_name='spoken_languages')
    iso_639_1 = models.TextField(max_length=4, unique=True)
    name = models.TextField(max_length=50)

    def __str__(self):
        return "iso:{iso}, name:{name}".format(iso=self.iso_639_1, name=self.name)
