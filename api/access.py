import requests
from utils import get_headers


class AccessClient:
    def __init__(self, connection_string: str, dev_mode: bool):
        self.connection_string = connection_string
        self.dev = dev_mode

    def get_user_details(self, headers):
        if self.dev:
            return {"username": "Test User1", "user_id": "1234-5678-99ab-cdef"}
        res = requests.get(
            f"{self.connection_string}/user-info/self", headers=get_headers(headers)
        )

        res.raise_for_status()
        if res.status_code == 200:
            return res.json()
