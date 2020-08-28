import argparse

from process import ProcessFlow
from common.logger import get_logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", '--test-file', dest='test_file', required=True, help='Provide the test file.')
    parser.add_argument("-d", '--debug-logging', dest='debug_logging', help='Provide to enable Debug Logging.')

    args = parser.parse_args()

    # Enable Logger
    logger = get_logger(__name__, "DEBUG" if args.debug_logging else "INFO")

    # Pass it to the Pre validation file for schema check, linting check, Security check.
    # If everything passes on pre validation level, pass it for deployment.
    # If deployment is successful, pass it for Post deployment validation
    ProcessFlow(args.test_file, logger)


if __name__ == '__main__':
    main()
