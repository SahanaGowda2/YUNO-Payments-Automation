Feature: Refund Transaction
  As a merchant
  I want to refund transactions
  So that I can return money to customers when needed

  Background:
    Given I have valid API credentials
    And the specific workflow is "DIRECT"

  @sanity
  Scenario: Full Refund of a Settled Transaction
    Given I have a successful "PURCHASE" transaction id
    When I send a POST request to "/payments/refund" with the transaction id
    Then the response status code should be 200 or 201
    And the response should contain "status" equal to "REFUNDED"

  @integration
  Scenario: Refund of Already Refunded Transaction
    Given I have a transaction id that is already "REFUNDED"
    When I send a POST request to "/payments/refund" with the transaction id
    Then the response status code should be 400 or 409
    And the response should contain error message "Transaction already refunded"
