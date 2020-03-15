from datetime import datetime
from uuid import uuid4


class Event:
    def __init__(self, name: str, date: datetime, data={}):
        """
        An Event is an action to be executed in the future
        :param name: Name of the event that we need to publish in order to be executed
        :param date: Date of when the event will be executed
        :param data: (Optional) Data to be passed to function
        """
        self.id = uuid4()
        self.name = name
        self.date = date
        self.data = data
