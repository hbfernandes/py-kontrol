from controller.queue import Queue
from controller.informer import Informer
import time

from kubernetes import client
from kubernetes.client.rest import ApiException


class AssetInstanceController:
    template_plural = "assettemplates"
    instance_plural = "assetinstances"
    group = "hv.com"
    version = "v1"
    namespace = "default"

    def __init__(self) -> None:
        co_api = client.CustomObjectsApi()

        self.queue = Queue()
        self.informer = Informer(
            co_api.list_namespaced_custom_object,
            on_all=self.queue.add,
            list_function_args={
                "group": self.group,
                "version": self.version,
                "namespace": self.namespace,
                "plural": self.instance_plural
            })

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

            event = item['event'].value
            obj = item['object']
            metadata = obj['metadata']
            name = metadata['name']
            ray = obj['status']['ray']

            if ray['generation'] != metadata['generation']:
                co_api = client.CustomObjectsApi()
                print(f"Working {event} event of {name}")
                # do things

                template = obj['spec']['template']
                try:
                    template_obj = co_api.get_namespaced_custom_object(
                        self.group,
                        self.version,
                        self.namespace,
                        self.template_plural,
                        template,
                    )
                except ApiException as e:
                    ray['created'] = False
                    ray['message'] = f"Template {template}: {e.reason}"
                else:
                    ray['created'] = True
                    ray['message'] = "Actor created"

                # update status
                ray['generation'] = metadata['generation']

                co_api.replace_namespaced_custom_object_status(
                    self.group,
                    self.version,
                    self.namespace,
                    self.instance_plural,
                    name,
                    obj
                )

        time.sleep(2)
        if self.running:
            self.work()
