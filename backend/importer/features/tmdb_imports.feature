Feature: TMDB Data Fetching

    Scenario: Fetching Movies
        Given 1 unfetched movies
        And mocked https://api.themoviedb.org/3/movie/1?api_key=test&language=en-US&append_to_response=alternative_titles,keywords,external_ids,images with json testdata/movie.json
        When I call "/import/tmdb/movies"
        Then the server should return status 200
        And a response like "All is in queue"
        And 1 movies should have been imported


    Scenario: Fetching Keywords And Pagination
        Given 1 fetched movies
        And keyword with id 378
        And mocked https://api.themoviedb.org/3/discover/movie?api_key=test&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_keywords=378 with json testdata/keyword_378_page1.json
        And mocked https://api.themoviedb.org/3/discover/movie?api_key=test&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=2&with_keywords=378 with json testdata/keyword_378_page2.json
        When I call "/import/tmdb/keywords"
        Then the server should return status 200
        And a response like "All keywords in queue"
        And movie_id=1 should have a keyword=prison associated to it


    Scenario: Fetching Persons
        Given 1 fetched movies
        When I call "/import/tmdb/persons"
        Then the server should return status 200
        And a response like "All persons in queue"
        And 1 movies should have been imported

