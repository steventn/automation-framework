# locust_tests/login_tasks.py
from locust import HttpUser
from config.settings import BASE_URL, TEST_USER, DEFAULT_WAIT_TIME

class AuthenticatedUser(HttpUser):
    """
    Base user class that logs in and stores a Bearer token for subsequent requests.
    """
    host = BASE_URL

    def on_start(self):
        """Executed once per user — perform authentication."""
        with self.client.post("/api/login", json=TEST_USER, catch_response=True) as response:
            if response.status_code == 200:
                token = response.json().get("token")
                if token:
                    self.client.headers.update({"Authorization": f"Bearer {token}"})
                    response.success()
                else:
                    response.failure("Login succeeded but no token found.")
            else:
                response.failure(f"Login failed with {response.status_code}: {response.text}")

    def on_stop(self):
        """Teardown logic if needed (logout, cleanup, etc.)."""
        self.client.headers.pop("Authorization", None)
