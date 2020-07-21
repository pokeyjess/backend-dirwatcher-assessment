import logging
import time

logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d &%H:%M:%S')

# timestamp. put date on it. prefix every message to logger with time stamp
# this is formatting timestamp
# name will reference the program -- dirwatcher.py
# use file instead? because reading from file
# 03d -- three digit format. shorten to 12, 8 characters, etc.
# use: \ for line break in format above
logger.setLevel(logging.DEBUG)

for _ in range(10):
    time.sleep(1.0)
    logger.debug("Hey this is kinda cool")


#formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(message)s')
