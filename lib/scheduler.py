from .pubsub import PubSub
from datetime import datetime
from .event import Event
import time

"""
PoC: Event Scanner and Publisher
J'ai un systeme qui verifie toutes les 5 minutes
si y a des événements à faire (comme publier une annonce kijiji)

Scanner les événements à faire qui se sont passé dans les 5 minutes.
Mettre les événements dans une Queue.
Faire un système qui publie les événements (pubsub).

1) Faire le programme normalement
2) En faire une librairie générique
"""


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

    def publish_missed_events(self):
        """
        Infinite loop to publish missed events between sleep time (run on separate thread)
        Publishing events meaning executing them through a Publish-Subscribe pattern.
        """
        while self.active:
            print('Checking...')
            if not self.all_events or len(self.all_events) == 0:
                return

            for event in self.all_events:
                if event.date <= datetime.now():
                    # We missed an event, publish it
                    self._pubSub.publish(event.name, event.data)
                    self.all_events.remove(event)

            time.sleep(self.waitSec)
