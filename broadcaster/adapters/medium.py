import requests
from .base import BaseAdapter

class MediumAdapter(BaseAdapter):
    def __init__(self, token=None):
        self.token = token
        self.base_url = "https://api.medium.com/v1"

    def authenticate(self, token):
        self.token = token

    def _get_user_id(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        resp = requests.get(f"{self.base_url}/me", headers=headers)
        resp.raise_for_status()
        return resp.json()["data"]["id"]

    def publish(self, title, content, **kwargs):
        if not self.token:
            raise ValueError("Medium token not set.")
        
        user_id = self._get_user_id()
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "title": title,
            "contentFormat": "markdown",
            "content": content,
            "publishStatus": kwargs.get("status", "draft")
        }
        
        resp = requests.post(
            f"{self.base_url}/users/{user_id}/posts",
            headers=headers,
            json=data
        )
        resp.raise_for_status()
        return resp.json()["data"]["url"]
