from unittest import TestCase
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from ..scheduler import Scheduler
from ..pubsub import PubSub
from ..event import Event
import threading


class TestScheduler(TestCase):
    mock_function = MagicMock()
    pubSub = PubSub.instance

    def setUp(self):
        # Subscribe to TEST event to mock_function
        self.pubSub.subscribe('TEST', self.mock_function)
        # Add event to Scheduler
        past_date = datetime.now() - timedelta(seconds=2)
        old_event = Event(name='TEST', date=past_date, data=(1, 2, 3))
        future_date = datetime.now() + timedelta(minutes=2)
        new_event = Event(name='TEST', date=future_date, data=(1, 2, 3))
        self.scheduler = Scheduler(waitSec=1, events=[old_event, new_event])

    def test_scheduler(self):
        self.assertEqual(len(self.scheduler.all_events), 2)
        t = threading.Thread(target=self.scheduler.publish_missed_events)
        t.start()

        self.scheduler.active = False
        self.mock_function.assert_called_once_with((1, 2, 3))
