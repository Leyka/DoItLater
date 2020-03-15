from unittest import TestCase
from unittest.mock import MagicMock
from ..pubsub import PubSub


class TestPubSub(TestCase):
    pubSub = PubSub.instance
    mock_function = MagicMock()

    def subscribe_mock_func(self):
        self.pubSub.subscribe("TEST", self.mock_function)

    def test_subscribe(self):
        self.subscribe_mock_func()
        self.assertTrue("TEST" in self.pubSub.subscribers)
        self.assertEqual(len(self.pubSub.subscribers["TEST"]), 1)

    def test_publish(self):
        self.subscribe_mock_func()
        self.pubSub.publish("TEST")
        self.mock_function.assert_called_once()
        self.pubSub.publish("TEST", (1, 2, 3))
        self.mock_function.assert_called_with((1, 2, 3))
