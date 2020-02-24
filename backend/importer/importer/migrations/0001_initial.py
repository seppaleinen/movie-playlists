# Generated by Django 3.0.3 on 2020-02-22 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlternativeTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_3166_1', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=500)),
                ('type', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'db_table': 'alternative_title',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('iso_3166_1', models.CharField(max_length=5, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('native_name', models.TextField()),
            ],
            options={
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
            options={
                'db_table': 'genre',
            },
        ),
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
            name='Language',
            fields=[
                ('iso_639_1', models.CharField(max_length=5, primary_key=True, serialize=False, unique=True)),
                ('name', models.TextField()),
                ('native_name', models.TextField()),
            ],
            options={
                'db_table': 'language',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=500)),
                ('popularity', models.DecimalField(decimal_places=3, max_digits=10)),
                ('fetched', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('budget', models.BigIntegerField(blank=True, null=True)),
                ('imdb_id', models.TextField(db_index=True, max_length=30, null=True, unique=True)),
                ('original_language', models.TextField(blank=True, max_length=30, null=True)),
                ('overview', models.TextField(blank=True, null=True)),
                ('poster_path', models.TextField(blank=True, max_length=40, null=True)),
                ('release_date', models.TextField(blank=True, max_length=10, null=True)),
                ('revenue', models.BigIntegerField(blank=True, null=True)),
                ('runtime', models.IntegerField(blank=True, null=True)),
                ('vote_average', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('vote_count', models.IntegerField(blank=True, null=True)),
                ('imdb_vote_average', models.DecimalField(blank=True, decimal_places=1, max_digits=10, null=True)),
                ('imdb_vote_count', models.IntegerField(blank=True, null=True)),
                ('raw_response', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'movie',
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
            model_name='movie',
            index=models.Index(fields=['id'], name='movie_pk_index'),
        ),
        migrations.AddField(
            model_name='language',
            name='countries',
            field=models.ManyToManyField(related_name='languages', to='importer.Country'),
        ),
        migrations.AddField(
            model_name='language',
            name='movies',
            field=models.ManyToManyField(related_name='spoken_languages', to='importer.Movie'),
        ),
        migrations.AddIndex(
            model_name='keywordids',
            index=models.Index(fields=['id'], name='keyword_ids_pk_index'),
        ),
        migrations.AddField(
            model_name='genre',
            name='movies',
            field=models.ManyToManyField(related_name='genres', to='importer.Movie'),
        ),
        migrations.AddField(
            model_name='country',
            name='movies',
            field=models.ManyToManyField(related_name='production_countries', to='importer.Movie'),
        ),
        migrations.AddField(
            model_name='alternativetitle',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alternative_titles', to='importer.Movie'),
        ),
        migrations.AddIndex(
            model_name='language',
            index=models.Index(fields=['iso_639_1'], name='iso_639_1_pk_index'),
        ),
        migrations.AddIndex(
            model_name='genre',
            index=models.Index(fields=['id'], name='genre_pk_index'),
        ),
        migrations.AddIndex(
            model_name='country',
            index=models.Index(fields=['iso_3166_1'], name='iso_3166_1_pk_index'),
        ),
    ]
