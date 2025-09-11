import requests
import yaml
import os

class APIClient:
    def __init__(self, env="dev"):
        config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config", "config.yml")
        config_path = os.path.abspath(config_path)
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        env_config = config["environments"][env]
        self.base_url = env_config["base_url"]

    def get(self, endpoint, **kwargs):
        return requests.get(f"{self.base_url}{endpoint}", **kwargs)

    def post(self, endpoint, data=None, json=None, **kwargs):
        return requests.post(f"{self.base_url}{endpoint}", data=data, json=json, **kwargs)

    def put(self, endpoint, data=None, json=None, **kwargs):
        return requests.put(f"{self.base_url}{endpoint}", data=data, json=json, **kwargs)

    def delete(self, endpoint, **kwargs):
        return requests.delete(f"{self.base_url}{endpoint}", **kwargs)
