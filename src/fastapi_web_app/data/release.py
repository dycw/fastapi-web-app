import datetime as dt


class Release:
    def __init__(self, version: str, latest_release: dt.datetime) -> None:
        self.version = version
        self.latest_release = latest_release
        self.created_date = dt.datetime.now()
