import datetime as dt
from typing import Optional


class User:
    def __init__(self, name: str, email: str, hashed_password: str) -> None:
        self.id = 1
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.created_date = None
        self.profile_image_url = ""
        self.last_login: Optional[dt.datetime] = None
