import requests
from .base import BaseAdapter

class MediumAdapter(BaseAdapter):
    """
    Medium Adapter.
    Supports two modes:
    1. 'api': Official API (requires Integration Token)
    2. 'session': Session Injection (requires 'sid' and 'uid' cookies)
    """
    def __init__(self):
        self.credentials = {}
        self.mode = "api"

    def authenticate(self, credentials):
        self.credentials = credentials
        if isinstance(credentials, dict) and "sid" in credentials:
            self.mode = "session"
        else:
            self.mode = "api"

    def publish(self, title, content, **kwargs):
        if self.mode == "session":
            return self._publish_session(title, content, **kwargs)
        return self._publish_api(title, content, **kwargs)

    def _publish_api(self, title, content, **kwargs):
        token = self.credentials if isinstance(self.credentials, str) else self.credentials.get("token")
        base_url = "https://api.medium.com/v1"
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get User ID
        resp = requests.get(f"{base_url}/me", headers=headers)
        resp.raise_for_status()
        user_id = resp.json()["data"]["id"]

        data = {
            "title": title,
            "contentFormat": "markdown",
            "content": content,
            "publishStatus": kwargs.get("status", "draft")
        }
        
        resp = requests.post(f"{base_url}/users/{user_id}/posts", headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()["data"]["url"]

    def _publish_session(self, title, content, **kwargs):
        """
        Uses session cookies to create a draft. 
        Medium's internal endpoint for drafts.
        """
        sid = self.credentials.get("sid")
        uid = self.credentials.get("uid")
        
        url = "https://medium.com/_/api/posts"
        cookies = {"sid": sid, "uid": uid}
        
        # Medium's internal API expects specific JSON structure
        payload = {
            "title": title,
            "content": {"type": "markdown", "text": content},
            "publishStatus": "DRAFT"
        }
        
        # Note: This usually requires a CSRF token (x-xsrf-token) in real browser calls
        # For a truly robust OS tool, we'd scrape the token first.
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        
        resp = requests.post(url, cookies=cookies, json=payload, headers=headers)
        if resp.status_code == 201:
            return "Draft created via session injection. Check your Medium stories."
        else:
            raise Exception(f"Session injection failed: {resp.status_code} {resp.text}")
