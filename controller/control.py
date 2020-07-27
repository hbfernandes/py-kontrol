from controller.queue import Queue
from controller.informer import Informer
from typing import Callable
import time


class Controller:
    def __init__(self, list_function: Callable, **kwargs) -> None:
        self.queue = Queue()
        self.informer = Informer(
            list_function, on_all=self.queue.add, list_function_args=kwargs)

    def start(self) -> None:
        self.running = True
        self.informer.start()
        self.work()

    def stop(self) -> None:
        self.informer.stop()
        self.running = False

    def work(self) -> None:
        while not self.queue.is_empty():
            item = self.queue.get()

            print(
                f"Working {item['event'].value} event of {item['object']['metadata']['name']}")

            # do things
            
        time.sleep(2)

        if self.running:
            self.work()
