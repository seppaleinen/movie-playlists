Feature: API 
    
    Scenario Outline: Testing out the autocomplete
        Given movie exists with name "Fight Club"
        When I call "/api/autocomplete/<search_query>"
        Then the server should return status 200
        And a response like "<expected_result>"

        Examples: Simple cases
            | search_query  | expected_result                       |
            | Fight Club    | [{"id": 1, "name": "Fight Club"}]     |
            | Fight         | [{"id": 1, "name": "Fight Club"}]     |


    Scenario Outline: Testing out the search
        Given movie exists with name "Fight Club"
        When I call "/api/search/<search_query>"
        Then the server should return status 200
        And a response like "<expected_result>"

        Examples: Simple cases
            | search_query  | expected_result                       |
            | Fight Club    | [{"id": 1, "name": "Fight Club", "popularity": "0.000", "fetched": false, "deleted": false, "budget": null, "original_language_id": "en", "imdb_id": null, "overview": null, "poster_path": null, "release_date": null, "revenue": null, "runtime": null, "vote_average": null, "vote_count": null, "imdb_vote_average": null, "imdb_vote_count": null, "raw_response": null}]     |


