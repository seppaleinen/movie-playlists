# Backend


### Notes
* To fetch images, prefix with: https://image.tmdb.org/t/p/w500/

* DB Migration Guide
  1. ```bash docker exec -ti worldinmovies_db_1 pg_dump -U postgres postgres --clean --file=/tmp/dbexport.pgsql ```
  2. Move postgres-data/dbexport.pgsql to machine where it should be imported
  3. ```bash docker exec -ti worldinmovies_db_1 psql -U postgres --file=/tmp/dbexport.pgsql ```



### Requirements

* Python3
* Postgresql


```bash
# Install requirements
pip3 install -r requirements

# To create and update database
./manage.py makemigrations && ./manage.py migrate

# To start server with gunicorn
gunicorn --config=gunicorn.config.py settings.wsgi

# To start server without gunicorn
./manage.py runserver

# Lint project
pylint --load-plugins pylint_django importer/ settings/

# Run mutation tests
mutmut --paths-to-mutate=importer/ --runner="./manage.py behave" --tests-dir=features/ run
```