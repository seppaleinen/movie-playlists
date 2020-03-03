Feature: API 
    
    Scenario Outline: Testing out the autocomplete
        Given movie exists with name "Fight Club"
        When I call "/api/autocomplete/<search_query>"
        Then the server should return status 200
        And a response like "<expected_result>"

        Examples: Simple cases
            | search_query  | expected_result                                   |
            | Fight Club    | "[{\"id\": 1, \"name\": \"Fight Club\"}]"     |
            | Fight         | "[{\"id\": 1, \"name\": \"Fight Club\"}]"     |


    Scenario Outline: Testing out the search
        Given movie exists with name "Fight Club"
        When I call "/api/search/<search_query>"
        Then the server should return status 200
        And a response like "<expected_result>"

        Examples: Simple cases
            | search_query  | expected_result                                   |
#            | Fight Club    | "[{\"id\": 1, \"name\": \"Fight Club\"}]"     |


