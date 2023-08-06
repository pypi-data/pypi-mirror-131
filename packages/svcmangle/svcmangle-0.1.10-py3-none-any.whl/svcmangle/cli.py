import logging
import sys

import pywintypes

from svcmangle import ServiceControlManager


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if len(sys.argv) < 2:
        print("Usage: %s <service name>" % sys.argv[0])
        sys.exit(1)

    try:
        fh_svc = ServiceControlManager(sys.argv[1])
    except pywintypes.error as e:
        if e.winerror == 5:
            logging.error("Insufficient privileges. Run as administrator.")
            sys.exit(1)
        else:
            raise

    print(f"{sys.argv[1]} is running:", fh_svc.status.state.running)
    print(f"{sys.argv[1]} is start type:", fh_svc.config.start_type.type)
