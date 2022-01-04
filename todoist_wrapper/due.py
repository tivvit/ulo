import datetime


class TDDue:
    def __init__(self, due: dict):
        self.date: datetime = datetime.datetime.fromisoformat(due["date"].replace('Z', '+00:00'))
        self.is_recurring: bool = due["is_recurring"]
        self.lang: str = due.get("lang", None)
        self.string: str = due.get("string", None)
        self.timezone: str = due.get("timezone", None)
