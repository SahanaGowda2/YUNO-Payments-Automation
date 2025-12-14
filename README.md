# Yuno Automation Framework

This repository contains the test automation framework for Yuno payment integration.

## Stack
- **Language**: Python 3.x
- **Framework**: Behave (Gherkin BDD)
- **HTTP Client**: Requests
- **Data Generation**: Faker
- **Author**: [SahanaGowda2](https://github.com/SahanaGowda2)

## Folder Structure
```
.
├── features/
│   ├── purchase.feature       # Purchase scenarios
│   ├── refund.feature         # Refund scenarios
│   ├── authorization.feature  # Auth scenarios
│   ├── cancel.feature         # Cancel/Void scenarios
│   ├── capture_and_verify.feature # Capture & Verify scenarios
│   ├── customer.feature       # Customer & Enrollment scenarios
│   ├── environment.py         # Behave hooks
│   ├── steps/
│   │   └── api_steps.py       # Step definitions
│   └── utils/
│       └── api_client.py      # API helper class (Mocked)
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── test_cases.md              # Detailed Test Case Documentation & Requirements
```

## Prerequisites
- **Python 3.7+**: Ensure Python is installed and added to your system PATH.
  - Verify with `python --version` or `py --version`.
- **Git**: For version control.

## Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Create a Virtual Environment** (recommended):
   ```bash
   # Windows
   python -m venv venv
   ./venv/Scripts/activate
   
   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**:
   - The project is configured to hit `https://api.y.uno/v1` by default.
   - For this demonstration, the `APIClient` in `features/utils/api_client.py` mocks the responses to simulate successful Yuno API interactions without needing real credentials.
   - To use real credentials, update `config.py` or set environment variables:
     - `PUBLIC_API_KEY`
     - `PRIVATE_SECRET_KEY`
     - `ACCOUNT_ID`

## Execution

### Run All Tests
To run all feature files:
```bash
behave
```

### Run Specific Tags
To run only Sanity tests:
```bash
behave --tags=@sanity
```

To run Regression tests:
```bash
behave --tags=@regression
```

## Documentation
See [test_cases.md](./test_cases.md) for a detailed breakdown of:
- Functional & Non-Functional Requirements
- Test Scenarios prioritized by Sanity/Regression/Integration
- Reference to official Yuno docs used:
  - Create Payment: https://docs.y.uno/reference/create-payment
  - Refund: https://docs.y.uno/reference/refund-payment
