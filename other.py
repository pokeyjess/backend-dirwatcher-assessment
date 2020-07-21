import logging
logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d &%H:%M:%S')


logger.setLevel(logging.DEBUG)


def func():
    logger.error("This was logged from other")
