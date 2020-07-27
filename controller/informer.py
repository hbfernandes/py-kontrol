from typing import Callable, Dict
from enum import Enum
from kubernetes import watch
import threading


class EventType(Enum):
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    DELETE = "DELETED"
    ERROR = "ERROR"
    ALL = "ALL"


class Informer:
    on_event: dict = {}

    def __init__(self,
                 list_function: Callable,
                 list_function_args: Dict = {},
                 on_add: Callable = None,
                 on_modified: Callable = None,
                 on_delete: Callable = None,
                 on_all: Callable = None
                 ) -> None:
        self.list_function = list_function
        self.list_function_args = list_function_args
        self.on_event[EventType.ADDED] = on_add
        self.on_event[EventType.MODIFIED] = on_modified
        self.on_event[EventType.DELETE] = on_delete
        self.on_event[EventType.ALL] = on_all

        self.watcher = watch.Watch()

    def start(self) -> None:
        self.watch_thread = threading.Thread(target=self.watch, daemon=True)
        self.watch_thread.start()

    def stop(self):
        self.watcher.stop()

    def watch(self):
        events = self.watcher.stream(self.list_function, **self.list_function_args)
        for event in events:
            event_type = EventType(event['type'])
            event_object = event['object']
            event_callback = self.on_event[event_type] or self.on_event[EventType.ALL]

            print(
                f"Received {event_type.value} event for {event_object['metadata']['name']}")

            if event_callback:
                event_callback({
                    "event": event_type,
                    "object": event_object
                })
            else:
                print(f"No callback for {event_type}")


if __name__ == "__main__":
    pass
