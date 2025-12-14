Feature: Payment Authorization
  As a merchant
  I want to authorize payments
  So that I can capture funds later

  Background:
    Given I have valid API credentials
    And the specific workflow is "DIRECT"

  @sanity
  Scenario: Successful Authorization with Minimal Fields
    Given I have a valid payload with minimal fields
    When I send a POST request to "/payments/authorization"
    Then the response status code should be 200 or 201
    And the response should contain "status" equal to "AUTHORIZED"

  @regression
  Scenario: Successful Authorization with Maximal Fields
    Given I have a valid payload with maximal fields
    When I send a POST request to "/payments/authorization"
    Then the response status code should be 200 or 201
    And the response should contain "status" equal to "AUTHORIZED"
