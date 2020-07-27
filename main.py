from kubernetes import client, config
import sys
import traceback

from controller.control import Controller

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CustomObjectsApi()
controller = Controller(
    v1.list_namespaced_custom_object,
    group="hv.com",
    version="v1",
    namespace="default",
    plural="assets"
)


def main():
    controller.start()


try:
    main()
except KeyboardInterrupt:
    print('Stopped by user')
    controller.stop()

    sys.exit(0)
except Exception:
    traceback.print_exc(file=sys.stdout)

sys.exit(0)
