from unittest import TestCase
from unittest.mock import MagicMock
from ..pubsub import PubSub


class TestPubSub(TestCase):
    pubSub = PubSub.instance
    mock_function = MagicMock()

    def setUp(self):
        self.pubSub.subscribers["TEST"] = []
        self.pubSub.subscribe("TEST", self.mock_function)

    def test_subscribe(self):
        self.assertTrue("TEST" in self.pubSub.subscribers)
        self.assertEqual(1, len(self.pubSub.subscribers["TEST"]))

    def test_publish(self):
        self.pubSub.publish("TEST")
        self.mock_function.assert_called_once()
        self.pubSub.publish("TEST", (1, 2, 3))
        self.mock_function.assert_called_with((1, 2, 3))
