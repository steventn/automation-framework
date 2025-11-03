# locust_tests/user_tasks.py
from locust import task, between
from locust_tests.login_tasks import AuthenticatedUser
from locust_tests.utils import random_name, check_response
from config.settings import DEFAULT_WAIT_TIME

class ReqresUser(AuthenticatedUser):
    """
    Simulates user behavior with GET and POST endpoints from reqres.in.
    """
    wait_time = between(*DEFAULT_WAIT_TIME)

    @task(3)
    def list_users(self):
        """List all users (paginated)."""
        with self.client.get("/api/users?page=2", catch_response=True) as response:
            check_response(response, expected_status=200)

    @task(2)
    def get_user(self):
        """Fetch a specific user profile."""
        user_id = 2
        with self.client.get(f"/api/users/{user_id}", catch_response=True) as response:
            check_response(response, expected_status=200)

    @task(1)
    def create_user(self):
        """Simulate creating a user."""
        payload = {"name": random_name(), "job": "leader"}
        with self.client.post("/api/users", json=payload, catch_response=True) as response:
            check_response(response, expected_status=201)

    @task(1)
    def update_user(self):
        """Simulate updating a user."""
        payload = {"name": "morpheus", "job": "crab resident"}
        with self.client.put("/api/users/2", json=payload, catch_response=True) as response:
            check_response(response, expected_status=200)
