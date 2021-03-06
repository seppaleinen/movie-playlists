Feature: TMDB Daily Exports 
    TMDB exposes a bunch of files each day, containing the ids of their database. 
    Which I then can use to fetch more data from.

    Scenario: Fetching the person ids
        Given mocked http://files.tmdb.org/p/exports/person_ids_02_17_2020.json.gz with gzipped testdata/person_ids.json
        When I call "/import/daily/tmdb/persons"
        Then the server should return status 200
        And a response like "Imported: 10, and deleted: 0, out of: 10"

    Scenario: Fetching the keyword ids
        Given mocked http://files.tmdb.org/p/exports/keyword_ids_02_17_2020.json.gz with gzipped testdata/keyword_ids.json
        When I call "/import/daily/tmdb/keywords"
        Then the server should return status 200
        And a response like "Imported: 10, and deleted: 0, out of: 10"

    Scenario: Fetching the keyword ids
        Given mocked http://files.tmdb.org/p/exports/production_company_ids_02_17_2020.json.gz with gzipped testdata/production_company_ids.json
        When I call "/import/daily/tmdb/production/companies"
        Then the server should return status 200
        And a response like "Imported: 10, and deleted: 0, out of: 10"

    Scenario: Fetching the movie ids
        Given mocked http://files.tmdb.org/p/exports/movie_ids_02_17_2020.json.gz with gzipped testdata/movie_ids.json
        When I call "/import/daily/tmdb/movies"
        Then the server should return status 200
        And a response like "Imported: 10, and deleted: 0, out of: 10"

    Scenario: Fetching Genres
        Given mocked https://api.themoviedb.org/3/genre/movie/list?api_key=test&language=en-US with json testdata/genres.json
        When I call "/import/daily/tmdb/genres"
        Then the server should return status 200
        And a response like "Imported: 19 genres"
