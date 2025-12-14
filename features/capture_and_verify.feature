Feature: Capture and Verify
  As a merchant
  I want to capture funds and verify cards
  So that I can complete sales and check payment validity

  Background:
    Given I have valid API credentials
    And the specific workflow is "DIRECT"

  @sanity
  Scenario: Capture a Valid Authorization
    Given I have a successful "AUTHORIZATION" transaction id
    When I send a POST request to "/payments/capture" with the transaction id
    Then the response status code should be 200 or 201
    And the response should contain "status" equal to "CAPTURED"

  @regression
  Scenario: Verify a Valid Card
    Given I have a valid payload with minimal fields
    When I send a POST request to "/payments/verify"
    Then the response status code should be 200
    And the response should contain "status" equal to "VALID"

  @integration
  Scenario: Verify an Invalid Card
    Given I have a payload with an invalid card number
    When I send a POST request to "/payments/verify"
    Then the response status code should be 400
