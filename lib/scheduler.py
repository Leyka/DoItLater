from .pubsub import PubSub
from datetime import datetime
from .event import Event
from threading import Thread
import time


class Scheduler:
    _pubSub = PubSub.instance

    def __init__(self, waitSec: int, events: [Event] = []):
        """
        Scheduler
        :param waitSec: Time to wait in seconds before next scan
        """
        self.waitSec = waitSec
        self._all_events = events
        self._active = True

    @property
    def all_events(self):
        return self._all_events

    def add_event(self, event):
        self.all_events.append(event)

    @property
    def active(self):
        """ Returns true to keep Scheduler running"""
        return self._active

    @active.setter
    def active(self, state: bool):
        self._active = state

    def __publish_missed_events(self):
        """
         Infinite loop to publish missed events between sleep time (run on separate thread)
         Publishing events meaning executing them through a Publish-Subscribe pattern.
         """
        while self.active:
            if not self.all_events or len(self.all_events) == 0:
                return

            for event in self.all_events:
                if event.date <= datetime.now():
                    # We missed an event, publish it
                    self._pubSub.publish(event.name, event.data)
                    self.all_events.remove(event)

            time.sleep(self.waitSec)

    def publish_missed_events(self) -> Thread:
        # Start infinite loop on a separate thread
        t = Thread(target=self.__publish_missed_events)
        t.start()
        return t
