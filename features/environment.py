from features.utils.api_client import APIClient

def before_all(context):
    context.api = APIClient()

def before_scenario(context, scenario):
    context.payload = {}
    context.response = None
    context.last_transaction_id = None
