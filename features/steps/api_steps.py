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
    # For now, we generate a mock ID or rely on the mock client to handle it
    context.transaction_id = str(uuid.uuid4())
    # In a real test, we might actually perform the setup transaction here
    # For now, we generate a mock ID or rely on the mock client to handle it
    context.transaction_id = str(uuid.uuid4())
    context.last_transaction_type = transaction_type
    
    if transaction_type == "CUSTOMER":
        # Simulate creating a customer so we have an ID for enrollment
        # effectively doing nothing but setting the ID, but semantically clear
        pass

@given('I have a transaction id that is already "{status}"')
def step_impl(context, status):
    context.transaction_id = str(uuid.uuid4())
    # The mock client needs to know to fail this
    context.transaction_id = "refunded-tx-id" 

@given('I have a non-existent transaction id')
def step_impl(context):
    context.transaction_id = "non-existent-id"

@when('I send a POST request to "{endpoint_param}"')
def step_impl(context, endpoint_param):
    # If endpoint_param is a generic name like "/payments/purchase", map it to official API
    endpoint = endpoint_param
    if endpoint_param == "/payments/purchase":
        endpoint = "/payments"
    elif endpoint_param == "/payments/authorization":
        endpoint = "/payments"
        # Ensure payload has capture=False for Auth if not already set
        if context.payload.get("capture") is None:
             context.payload["capture"] = False
    elif endpoint_param == "/payments/verify":
        endpoint = "/payments"
        context.payload["verify"] = True

    context.response = context.api.post(endpoint, context.payload)

@when('I send a POST request to "{action_type}" with the transaction id')
def step_impl(context, action_type):
    # Construct paths like /payments/{id}/refunds
    tx_id = context.transaction_id
    
    if "refund" in action_type:
        endpoint = f"/payments/{tx_id}/refunds"
        payload = {} # Refund amount often optional for full refund
    elif "cancel" in action_type:
        endpoint = f"/payments/{tx_id}/cancellation"
        payload = {}
    elif "capture" in action_type:
        endpoint = f"/payments/{tx_id}/capture"
        payload = {"amount": 1000} # Capture usually needs amount
    elif "capture" in action_type:
        endpoint = f"/payments/{tx_id}/capture"
        payload = {"amount": 1000} # Capture usually needs amount
    elif "enrollment" in action_type or "enroll" in action_type or "ENROLL" in action_type:
        # Assuming endpoint pattern /customers/{id}/enrollment based on context
        endpoint = f"/customers/{tx_id}/enrollment"
        payload = context.payload
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
