import json
from datetime import datetime
from pathlib import Path
from lib.event import Event
from lib.scheduler import Scheduler
from lib.pubsub import PubSub
from example.utils import print_console, write_quote_file

pubSub = PubSub()


def import_events() -> [Event]:
    events = []
    events_path = Path('events.json').resolve()

    with open(events_path, 'r') as f:
        data = f.read()
        events_json = json.loads(data)
        for event_json in events_json:
            event = Event(**event_json)
            event.date = datetime.strptime(event_json['date'], '%Y-%m-%d %H:%M')  # format date
            events.append(event)
        return events


def subscribe_events_to_functions():
    pubSub.subscribe('PRINT_CONSOLE', print_console)
    pubSub.subscribe('WRITE_QUOTE_FILE', write_quote_file)


if __name__ == '__main__':
    subscribe_events_to_functions()
    events = import_events()
    # Just for testing, we will publish_missed_events one time only
    scheduler = Scheduler(waitSec=1, events=events)
    scheduler.publish_missed_events()
    scheduler.active = False
