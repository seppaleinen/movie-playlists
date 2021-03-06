# Generated by Django 2.2.3 on 2020-02-22 20:06

from django.db import migrations
import csv, json, os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0001_initial'),
    ]

    def forwards(apps, schema_editor):
        Language = apps.get_model("importer", "Language")
        Country = apps.get_model("importer", "Country")
        with open(os.path.join(BASE_DIR, 'migrations/languages.csv'), mode='r') as languages:
            reader = csv.reader(languages)
            for row in reader:
                Language.objects.create(iso_639_1=row[0], name=row[1], native_name=row[2])

        with open(os.path.join(BASE_DIR, 'migrations/countries-and-languages.csv'), mode='r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                country = Country.objects.create(iso_3166_1=row[0],name=row[1],native_name=row[2])
                languages = row[3].strip().lower().split(',')
                for language_code in languages:
                    try:
                        country.languages.add(Language.objects.get(pk=language_code.strip()))
                    except Exception as exc:
                        print("Could not find language: '%s'" % language_code)
                        raise exc
                country.save()

        with open(os.path.join(BASE_DIR, 'migrations/tmdb_languages.json'), mode='r') as languages_json:
            data = json.load(languages_json)
            for i in data:
                try:
                    Language.objects.get(pk=i['iso_639_1'])
                except Exception as exc:
                    print("Could not match %s" % i)
                    raise exc

        with open(os.path.join(BASE_DIR, 'migrations/tmdb_countries.json'), mode='r') as countries_json:
            data = json.load(countries_json)
            for i in data:
                try:
                    Country.objects.get(pk=i['iso_3166_1'])
                except Exception as exc:
                    print("Could not match %s" % i)
                    raise exc


    operations = [
        migrations.RunPython(forwards),
    ]
