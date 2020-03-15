from unittest import TestCase
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from ..scheduler import Scheduler
from ..pubsub import PubSub
from ..event import Event


class TestScheduler(TestCase):
    mock_function = MagicMock()
    pubSub = PubSub.instance

    def setUp(self):
        # Subscribe to TEST event to mock_function
        self.pubSub.subscribe('TEST', self.mock_function)
        # Add events to Scheduler
        past_date = datetime.now() - timedelta(seconds=10)
        past_event = Event(name='TEST', date=past_date, data=(1, 2, 3))
        future_date = datetime.now() + timedelta(minutes=2)
        future_event = Event(name='TEST', date=future_date, data=(1, 2, 3))
        self.scheduler = Scheduler(waitSec=0, events=[past_event, future_event])

    def test_scheduler(self):
        self.assertEqual(len(self.scheduler.all_events), 2)
        # past_event should be called here and deleted from list
        thread = self.scheduler.publish_missed_events()
        self.scheduler.active = False
        thread.join()
        # future_event should never be called but stays in events
        self.assertEqual(len(self.scheduler.all_events), 1)
        self.mock_function.assert_called_once_with((1, 2, 3))
