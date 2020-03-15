from unittest import TestCase
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from ..scheduler import Scheduler
from ..pubsub import PubSub
from ..event import Event


class TestScheduler(TestCase):
    pubSub = PubSub.instance

    def setUp(self):
        self.mock_function = MagicMock()
        # Subscribe to TEST event to mock_function
        self.pubSub.subscribe('TEST', self.mock_function)
        # Add events to Scheduler
        past_date = datetime.now() - timedelta(seconds=10)
        past_event = Event(name='TEST', date=past_date, data=(1, 2, 3))
        future_date = datetime.now() + timedelta(minutes=2)
        future_event = Event(name='TEST', date=future_date, data=(1, 2, 3))
        self.scheduler = Scheduler(waitSec=0, events=[past_event, future_event])

    def test_event_list_count(self):
        self.assertEqual(2, len(self.scheduler.all_events))

    def test_past_event(self):
        # Past event should be called here and deleted from list
        thread = self.scheduler.publish_missed_events()
        self.scheduler.active = False
        thread.join()
        # mock_function should be called one time only (past)
        self.mock_function.assert_called_once_with((1, 2, 3))

    def test_future_event(self):
        # Future event should never be called but stays in events
        thread = self.scheduler.publish_missed_events()
        self.scheduler.active = False
        thread.join()
        # We should have one remaining event (future)
        self.assertEqual(1, len(self.scheduler.all_events))
