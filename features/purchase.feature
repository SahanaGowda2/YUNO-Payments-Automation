Feature: Purchase Transaction
  As a merchant
  I want to process purchase transactions
  So that I can accept payments from customers

  Background:
    Given I have valid API credentials
    And the specific workflow is "DIRECT"

  @sanity
  Scenario: Successful Purchase with Minimal Fields
    Given I have a valid payload with minimal fields
      | field        | value          |
      | duplicate    | false          |
    When I send a POST request to "/payments/purchase"
    Then the response status code should be 200 or 201
    And the response should contain "status" equal to "SUCCEEDED"

  @regression
  Scenario: Successful Purchase with Maximal Fields
    Given I have a valid payload with maximal fields
      | field            | value          |
      | customer_payer   | full_details   |
      | additional_data  | full_details   |
    When I send a POST request to "/payments/purchase"
    Then the response status code should be 200 or 201
    And the response should contain "id"
    And the response should contain "status" equal to "SUCCEEDED"

  @integration
  Scenario: Failed Purchase with Invalid Card
    Given I have a payload with an invalid card number
    When I send a POST request to "/payments/purchase"
    Then the response status code should be 400 or 402
