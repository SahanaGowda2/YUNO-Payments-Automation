# My Yuno Integration Test Project

Hi! This is my project for the Automation Engineer task. I have broken down everything I learnt and tested below.

## 1. Functional & Non-Functional Requirements

I have listed what the system *must* do (Functional) and how well it should do it (Non-Functional) based on my understanding.

### Functional Requirements
*   Purchases: We obviously need to be able to buy things! The system must verify the transaction details.
*   Refunds: If a customer isn't happy, we need to give their money back.
*   Authorization & Capture: Sometimes we just want to hold the money first (Auth) and take it later (Capture).
*   Cancellation: If an Auth was a mistake, we need to cancel it so the user gets their funds back.
*   Verification: We have to check if the card is real or just made up numbers.
*   Idempotency: This is a big one! We use 'x-idempotency-key' to make sure we don't accidentally charge someone twice for the same click.
*   Workflow: The 'workflow' field MUST always be "DIRECT". I made sure of this!

### Non-Functional Requirements
*   Speed: The API shouldn't be too slow, otherwise customers will leave.
*   Security: We shouldn't crash if someone sends bad data.
*   Error Handling: If I send garbage, the API should tell me 'why' clearly (like 400 Bad Request) instead of just exploding (500 Error).

---

## 2. Test Case Scenarios

I split the test cases so they are easier to read.

### 2.1 Purchase Scenarios
These ensure we can actually make money!

| ID | Priority | Scenario Description | Why is this important? |
|----|----------|----------------------|------------------------|
| PUR-01 | [Sanity] | Successful Purchase with just minimal fields | This is the most basic "happy path". If this fails, nothing works! |
| PUR-02 | [Regression] | Purchase with ALL fields (user details, etc) | We need to make sure extra data doesn't break anything. |

### 2.2 Refund Scenarios
Testing if we can return funds correctly.

| ID | Priority | Scenario Description | Why is this important? |
|----|----------|----------------------|------------------------|
| REF-01 |  [Sanity] | Full Refund of a transaction | Essential feature. Money back guarantee! |

### 2.3 Authorization, Capture & Cancel scenarios
The complex flows for holding and releasing funds.

| ID | Priority | Scenario Description | Why is this important? |
|----|----------|----------------------|------------------------|
| AUTH-01 | [Sanity] | Authorization (Minimal fields) | Testing the "hold" mechanism. |
| CAP-01 | [Sanity] | Capture a valid Authorization | Completing the "hold" mechanism. |
| CAN-01 | [Regression] | Cancel a valid Authorization | Testing the "release" mechanism. |

### 2.4 Verify Scenarios
Checking if cards are valid without charging them.

| ID | Priority | Scenario Description | Why is this important? |
|----|----------|----------------------|------------------------|
| VER-01 | [Regression] | Verify a valid card | Checking if the card is good to go. |

### 2.5 Customer & Enrollment Scenarios
We want to save customers so they don't type their card every time.

| ID | Priority | Scenario Description | Why is this important? |
|----|----------|----------------------|------------------------|
| CUST-01 | [Sanity] | Create a New Customer | We need a user before we save a card. |
| ENR-01 | [Sanity] | Enroll a Payment Method | Saving the card for valid future use. |

---

## 3. Negative Testing Suites

I also tried to think of ways to break the system ("Negative Testing") to make sure it's robust. These are mostly Integration tests.

| ID | Priority | Scenario Description | Expected Outcome |
|----|----------|----------------------|------------------|
| NEG-01 | [Integration] | **Purchase with Invalid Card** | Should fail with 400. We don't want fake money! |
| NEG-02 | [Integration] | **Refund a Transaction TWICE** | Should fail (409/400). You can't refund money you already gave back. |
| NEG-03 | [Integration] | **Capture an Expired/Invalid ID** | Should fail (404/400). Can't capture what isn't there. |
| NEG-04 | [Integration] | **Verify Invalid Card Format** | Should fail (400). Bad numbers shouldn't pass. |
| NEG-05 | [Integration] | **Wrong Workflow Value** | I forced the workflow to "INDIRECT". The system MUST reject this! |
| NEG-06 | [Integration] | **Enroll with invalid token** | Should fail. Token must be valid to save a card. |
