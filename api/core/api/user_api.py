from .client import APIClient

class UserAPI:
    def __init__(self, env="dev"):
        self.client = APIClient(env)

    def get_user(self, user_id):
        return self.client.get(f"/users/{user_id}")

    def list_users(self):
        return self.client.get("/users")

    def create_user(self, payload):
        return self.client.post("/users", json=payload)
