Feature: Health 
    In order to see that the server is up and running correctly this endpoint needs to be working

    Scenario: Calling the health endpoint
        When I call "/health"
        Then the server should return status 200
        And a response like "{"Status": "OK"}"
