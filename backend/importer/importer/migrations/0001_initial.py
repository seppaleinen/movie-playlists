# Generated by Django 2.2.3 on 2020-02-17 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KeywordIds',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('fetched', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'keyword_ids',
            },
        ),
        migrations.CreateModel(
            name='MovieIds',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('popularity', models.DecimalField(decimal_places=3, max_digits=10)),
                ('fetched', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'movie_ids',
            },
        ),
        migrations.CreateModel(
            name='PersonIds',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('popularity', models.DecimalField(decimal_places=3, max_digits=10)),
                ('fetched', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'person_ids',
            },
        ),
        migrations.CreateModel(
            name='ProductionCompanyIds',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('fetched', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'production_company_ids',
            },
        ),
        migrations.AddIndex(
            model_name='productioncompanyids',
            index=models.Index(fields=['id'], name='production_company_pk_index'),
        ),
        migrations.AddIndex(
            model_name='personids',
            index=models.Index(fields=['id'], name='person_ids_pk_index'),
        ),
        migrations.AddIndex(
            model_name='movieids',
            index=models.Index(fields=['id'], name='movie_ids_pk_index'),
        ),
        migrations.AddIndex(
            model_name='keywordids',
            index=models.Index(fields=['id'], name='keyword_ids_pk_index'),
        ),
    ]
