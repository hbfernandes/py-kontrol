from kubernetes import config
import sys
import traceback

from controller.control import AssetInstanceController

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
controller = AssetInstanceController()


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
