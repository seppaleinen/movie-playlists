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


class MovieIds(models.Model):
    id = models.IntegerField(db_index=True, primary_key=True)
    name = models.TextField()
    popularity = models.DecimalField(decimal_places=3, max_digits=10)
    fetched = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=['id'], name='movie_ids_pk_index')]
        db_table = "movie_ids"

    def create(dict_object):
        this = PersonIds()
        this.id = dict_object['id']
        this.name = dict_object['original_title']
        this.popularity = dict_object['popularity']
        return this

    def __str__(self):
        return "id:{id}, name:{name}, popularity={popularity}, fetched={fetched}, deleted={deleted}".format(
        	id=self.id, 
        	name=self.name, 
        	popularity=self.popularity, 
        	fetched=self.fetched, 
        	deleted=self.deleted)
