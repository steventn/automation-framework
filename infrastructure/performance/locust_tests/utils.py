# locust_tests/utils.py
import random
import string

def random_name(length=6):
    """Generate a random name for test payloads."""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def check_response(response, expected_status=200):
    """Reusable validation for API responses."""
    if response.status_code != expected_status:
        response.failure(f"Expected {expected_status}, got {response.status_code}: {response.text}")
    else:
        response.success()
