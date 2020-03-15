from __future__ import annotations


class PubSubMeta(type):
    # Singleton of PubSub class
    _instance = None

    def __call__(cls) -> PubSub:
        if cls._instance is None:
            cls._instance = super().__call__()
        return cls._instance


class PubSub(metaclass=PubSubMeta):
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event: str, callbackFn):
        if event not in self.subscribers:
            self.subscribers[event] = []
        self.subscribers[event].append(callbackFn)

    def publish(self, event: str, data=None):
        if event not in self.subscribers:
            return
        # Execute every function of the event's subscribers
        for subscriberCallbackFn in self.subscribers[event]:
            subscriberCallbackFn(data)
