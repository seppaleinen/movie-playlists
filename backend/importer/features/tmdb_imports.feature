Feature: TMDB Data Fetching

    Scenario: Fetching Movies
        Given 1 unfetched movies
        And mocked https://api.themoviedb.org/3/movie/1?api_key=test&language=en-US&append_to_response=alternative_titles,keywords,external_ids,images with json testdata/movie.json
        When I call "/import/tmdb/movies"
        Then the server should return status 200
        And a response like "All is in queue"
        And 1 movies should have been imported

