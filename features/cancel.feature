Feature: Cancel Authorization
  As a merchant
  I want to cancel an authorization
  So that I can release the held funds if the purchase is not completed

  Background:
    Given I have valid API credentials
    And the specific workflow is "DIRECT"

  @regression
  Scenario: Cancel a Valid Authorization
    Given I have a successful "AUTHORIZATION" transaction id
    When I send a POST request to "/payments/cancel" with the transaction id
    Then the response status code should be 200
    And the response should contain "status" equal to "CANCELLED"

  @integration
  Scenario: Cancel an Invalid Transaction ID
    Given I have a non-existent transaction id
    When I send a POST request to "/payments/cancel" with the transaction id
    Then the response status code should be 404
