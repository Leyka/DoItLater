class PubSub:
    _instance = None

    @staticmethod
    @property
    def instance(self):
        # Singleton
        if not PubSub._instance:
            PubSub._instance = PubSub()
        return PubSub._instance

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
