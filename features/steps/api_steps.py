from behave import given, when, then
import json
import uuid
from faker import Faker
from config import Config

fake = Faker()

@given('I have valid API credentials')
def step_impl(context):
    pass # Managed in APIClient/Config

@given('the specific workflow is "{workflow}"')
def step_impl(context, workflow):
    assert workflow == "DIRECT", f"Workflow must be DIRECT, got {workflow}"
    context.workflow = workflow

@given('I have a valid payload with minimal fields')
def step_impl(context):
    context.payload = {
        "amount": 1000,
        "currency": "USD",
        "account_id": Config.ACCOUNT_ID,
        "workflow": getattr(context, 'workflow', 'DIRECT')
    }
    if context.table:
        for row in context.table:
             # handle simple conversions if needed
             val = row['value']
             if val == 'false': val = False
             if val == 'true': val = True
             context.payload[row['field']] = val

@given('I have a valid payload with maximal fields')
def step_impl(context):
    context.payload = {
        "amount": 1000,
        "currency": "USD",
        "account_id": Config.ACCOUNT_ID,
        "workflow": getattr(context, 'workflow', 'DIRECT'),
        "customer_payer": {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email()
        },
        "additional_data": {
            "browser_info": fake.user_agent()
        }
    }

@given('I have a payload with an invalid card number')
def step_impl(context):
    context.payload = {
        "amount": 100,
        "currency": "USD",
        "account_id": Config.ACCOUNT_ID,
        "card": {
            "number": "invalid-card",
            "cvv": "123"
        },
        "workflow": getattr(context, 'workflow', 'DIRECT')
    }

@given('I have a valid customer payload')
def step_impl(context):
    context.payload = {
        "merchant_customer_id": str(uuid.uuid4()),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "workflow": getattr(context, 'workflow', 'DIRECT')
    }

@given('I have a valid enrollment payload')
def step_impl(context):
    context.payload = {
        "payment_method": {
             "type": "CARD",
             "token": "tok_" + str(uuid.uuid4())
        },
        "workflow": getattr(context, 'workflow', 'DIRECT')
    }

@given('I have a successful "{transaction_type}" transaction id')
def step_impl(context, transaction_type):
    # In a real test, we might actually perform the setup transaction here
    # For now, we generate a mock ID and rely on the mock client to handle it
    new_id = str(uuid.uuid4())
    context.last_transaction_type = transaction_type
    
    if transaction_type == "CUSTOMER":
        context.customer_id = new_id
    else:
        context.transaction_id = new_id

@given('I have a transaction id that is already "{status}"')
def step_impl(context, status):
    # The mock client can be configured to recognize this pattern
    context.transaction_id = f"tx-already-{status}"

@given('I have a non-existent transaction id')
def step_impl(context):
    context.transaction_id = "non-existent-id"

@when('I send a POST request to "{endpoint_param}"')
def step_impl(context, endpoint_param):
    # Map friendly Gherkin endpoints to actual API endpoints and set required payload fields
    endpoint_mappings = {
        "/payments/purchase": context.api.URI_PAYMENTS,
        "/payments/authorization": context.api.URI_PAYMENTS,
        "/payments/verify": context.api.URI_PAYMENTS,
        "/customers": context.api.URI_CUSTOMERS
    }
    endpoint = endpoint_mappings.get(endpoint_param, endpoint_param)

    # Set specific payload properties based on the operation
    if endpoint_param == "/payments/authorization" and context.payload.get("capture") is None:
        context.payload["capture"] = False
    elif endpoint_param == "/payments/verify":
        context.payload["verify"] = True

    context.response = context.api.post(endpoint, context.payload)

@when('I send a POST request to "{action_type}" with the transaction id')
def step_impl(context, action_type):
    payload = {}

    # Normalize action_type for robust matching
    normalized_action = action_type.lower()

    if "enroll" in normalized_action:
        # Enrollment requires a Customer ID, not a Transaction ID
        c_id = getattr(context, 'customer_id', getattr(context, 'transaction_id', None))
        endpoint = context.api.URI_ENROLLMENT.format(customer_id=c_id)
        payload = context.payload
        context.response = context.api.post(endpoint, payload)
        return

    # For transaction-based actions (Refund, Cancel, Capture)
    tx_id = context.transaction_id
    # Using the same ID for payment_id and transaction_id for simulation purposes
    sub_tx_id = tx_id

    if "refund" in normalized_action:
        endpoint = context.api.URI_REFUND.format(id=tx_id, transaction_id=sub_tx_id)
    elif "cancel" in normalized_action:
        endpoint = context.api.URI_CANCEL.format(payment_id=tx_id, transaction_id=sub_tx_id)
    elif "capture" in normalized_action:
        endpoint = context.api.URI_CAPTURE.format(payment_id=tx_id, transaction_id=sub_tx_id)
        payload = {"amount": 1000} # Capture usually needs amount
    else:
        raise ValueError(f"Unknown action type: {action_type}")

    context.response = context.api.post(endpoint, payload)

@then('the response status code should be {status_code_1} or {status_code_2}')
def step_impl(context, status_code_1, status_code_2):
    assert context.response.status_code in [int(status_code_1), int(status_code_2)], \
        f"Expected {status_code_1} or {status_code_2} but got {context.response.status_code}"

@then('the response status code should be {status_code}')
def step_impl(context, status_code):
    assert context.response.status_code == int(status_code), \
        f"Expected {status_code} but got {context.response.status_code}"

@then('the response should contain "{field}" equal to "{value}"')
def step_impl(context, field, value):
    json_resp = context.response.json()
    assert json_resp.get(field) == value, \
        f"Expected {field} to be {value} but got {json_resp.get(field)}"

@then('the response should contain "{field}"')
def step_impl(context, field):
    json_resp = context.response.json()
    assert field in json_resp, f"Response did not contain {field}"

@then('the response should contain error message "{message}"')
def step_impl(context, message):
    json_resp = context.response.json()
    # Check both "message" and "code" or other common error fields
    actual_message = json_resp.get("message") or json_resp.get("error") or str(json_resp)
    assert message in actual_message, f"Expected error '{message}' but got '{actual_message}'" 
