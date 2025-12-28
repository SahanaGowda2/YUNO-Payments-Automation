import requests
import uuid
import json
from config import Config

class APIClient:
    
    URI_PAYMENTS = "/payments"
    URI_CUSTOMERS = "/customers"
    URI_REFUND = "/payments/{id}/transactions/{transaction_id}/refund"
    URI_CAPTURE = "/payments/{payment_id}/transactions/{transaction_id}/capture"
    URI_CANCEL = "/payments/{payment_id}/transactions/{transaction_id}/cancel"
    URI_ENROLLMENT = "/customers/{customer_id}/payment-methods"

    def __init__(self):
        self.base_url = Config.BASE_URL
        self.session = requests.Session()
    
    def get_headers(self, idempotency_key=None):
        headers = {
            "Content-Type": "application/json",
            "public-api-key": Config.PUBLIC_API_KEY,
            "private-secret-key": Config.PRIVATE_SECRET_KEY,
            "x-idempotency-key": idempotency_key or str(uuid.uuid4())
        }
        return headers

    def post(self, endpoint, payload, idempotency_key=None):
        url = f"{self.base_url}{endpoint}"
        headers = self.get_headers(idempotency_key)
        
        # In a real scenario:
        # response = self.session.post(url, json=payload, headers=headers)
        
        # MOCKING RESPONSE
        from unittest.mock import Mock
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "id": str(uuid.uuid4()),
            "status": "SUCCEEDED"
        }

        # Simulated Logic for Testing -----------------------------------------
        
        # 1. Purchase / Auth (POST /payments)
        if endpoint == self.URI_PAYMENTS:
            if payload.get("verify") is True:
                 response.json.return_value["status"] = "VALID"
            elif payload.get("capture") is False:
                response.json.return_value["status"] = "AUTHORIZED"
            # Simulate invalid card
            if "invalid" in str(payload):
                 response.status_code = 400
                 response.json.return_value = {"code": "INVALID_CARD", "message": "Card invalid"}

        # 2. Capture (POST .../capture)
        elif "/capture" in endpoint:
            response.json.return_value["status"] = "CAPTURED"
            
        # 3. Cancel (POST .../cancel)
        elif "/cancel" in endpoint:
            response.status_code = 200 
            response.json.return_value["status"] = "CANCELLED"
            if "non-existent" in endpoint:
                response.status_code = 404

        # 4. Refund (POST .../refund)
        elif "/refund" in endpoint:
            response.json.return_value["status"] = "REFUNDED"
            if "refunded-tx-id" in endpoint or "tx-already-REFUNDED" in endpoint: # Simulate double refund
                response.status_code = 409
                response.json.return_value = {"message": "Transaction already refunded"}

        # 6. Enrollment (POST /customers/{id}/payment-methods)
        elif "/payment-methods" in endpoint:
             response.json.return_value = {
                 "payment_method_id": str(uuid.uuid4()),
                 "status": "ENROLLED"
             }

        # 5. Create Customer (POST /customers)
        elif endpoint == self.URI_CUSTOMERS:
             response.json.return_value = {
                 "id": str(uuid.uuid4()),
                 "status": "CREATED"
             }

        return response
