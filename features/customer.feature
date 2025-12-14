Feature: Customer and Enrollment
  As a merchant
  I want to create customers and enroll payment methods
  So that I can process payments for returning users

  Background:
    Given I have valid API credentials
    And the specific workflow is "DIRECT"

  @sanity
  Scenario: Create a New Customer
    Given I have a valid customer payload
    When I send a POST request to "/customers"
    Then the response status code should be 200 or 201
    And the response should contain "id"

  @sanity
  Scenario: Enroll a Payment Method
    Given I have a successful "CUSTOMER" transaction id
    And I have a valid enrollment payload
    When I send a POST request to "/enrollment" with the transaction id
    Then the response status code should be 200 or 201
    And the response should contain "status" equal to "ENROLLED"
