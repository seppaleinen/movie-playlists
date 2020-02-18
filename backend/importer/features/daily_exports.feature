Feature: TMDB Daily Exports 
	TMDB exposes a bunch of files each day, containing the ids of their database. 
	Which I then can use to fetch more data from.

    Scenario: Fetching the person ids
    	Given mocked http://files.tmdb.org/p/exports/person_ids_02_17_2020.json.gz with testdata testdata/person_ids.json
        When I call "/import/daily/tmdb/persons"
        Then the server should return status 200
        And a response like "Imported: 5, and deleted: 0, out of: 5"
