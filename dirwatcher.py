# to run program:
# python dirwatcher.py  <directory to watch>  <magic text to search> -e .txt -1 5

'''
s̶i̶g̶n̶a̶l̶ ̶h̶a̶n̶d̶l̶e̶r̶
f̶u̶n̶c̶t̶i̶o̶n̶ ̶t̶o̶ ̶l̶o̶o̶k̶ ̶f̶o̶r̶ ̶m̶a̶g̶i̶c̶ ̶t̶e̶x̶t̶
-logging where found text (currently logging kill signal)
̶t̶i̶m̶e̶s̶t̶a̶m̶p̶
figure out how to watch a directory
-exception handling to keep running
    when no directory found
̶a̶r̶g̶p̶a̶r̶s̶e̶,̶ ̶a̶d̶d̶ ̶a̶r̶g̶u̶m̶e̶n̶t̶s̶
s̶h̶u̶t̶d̶o̶w̶n̶ ̶a̶n̶d̶ ̶s̶t̶a̶r̶t̶ ̶u̶p̶ ̶b̶a̶n̶n̶e̶r̶s̶
tests
gitignore -- no log or test files, etc.
flake8, docstrings, etc.


when using logging in more than one file per directory
why? what's going on there?
AttributeError: partially initialized module 'logging' has no attribute 'getLogger' 
(most likely due to a circular import)
'''

import signal
import time
import logging
import os
import datetime
import argparse

exit_flag = False

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%Y-%m-%d &%H:%M:%S')
# timestamp


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically, it just sets a global flag, and main() will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    global exit_flag
    logger.debug(f"Handling signal: {signal.Signals(sig_num).name}")
    exit_flag = True
    # call this function when program gets a signal (see below)

    # log the associated signal name


def watch_directory():
    pass
#  need function to watch directory****


'''
# dictionary.
# The keys = filenames
# values = last line position
# Keep track of the last position.

1. For every file in the directory, add to dictionary 
if it is not already there 
(exclude files without proper extensions). 
Report new files that are added to your dictionary.
1. For every entry in your dictionary, 
is it still in the directory? If not, remove it from dict, 
report it as deleted.

Log message if watched directory is deleted. with timestamp
log message if watched file is deleted. with timestamp
'''


def find_magic_text(filename, last_position, magic_text):
    """
   Function to look for magic text
   Searches for magic text in file (from last line position)
   logging line number where found

    """
    line_number = 0
    with open(filename) as file:
        for line_number, line in enumerate(file):
            if line_number >= last_position:
                if magic_text in line:
                    logger.info(
                        f'Magic text: "{magic_text}", found at line: {line_number + 1} in: {filename}')
    return line_number + 1
# don't log the occurrence of magic text again


def create_parser():
    """creates command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help="Directory to watch")
    parser.add_argument('--ext', help="File extension to filter on")
    parser.add_argument('--int', default=1.0, help="Polling interval")
    parser.add_argument('--magic', help="Magic text to look for")
    return parser
# when have watch_directory set up:
# remove "--" to make required args


def main():
    parser = create_parser()
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.
# startup banner:
    app_start_time = datetime.datetime.now()
    logger.info(
        f"\n{40 * '-'}\n Running: {__file__}\n Started on: {app_start_time.isoformat()}\n{40 * '-'}")


# change print statements to logging:
# https://www.youtube.com/watch?v=jxmzY9soFXg, last 5 min

    while not exit_flag:
        try:
            print(f"[{os.getpid()}] Tick...")
            time.sleep(1)
            # with open('nothing.here') as f:
            #    f.read()
            # call my directory watching function
        except FileNotFoundError:
            logger.warning("Did not find that file")
            raise  # need this to avoid infinite loop!!!!
        # want to keep program going even if file not found
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            pass

        # exit banner. make separate function?

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        # time.sleep(polling_interval)
# closing banner
    uptime = datetime.datetime.now() - app_start_time
    logger.info(
        f"\n{40 * '-'}\n Stopped: {__file__}\n Uptime was: {str(uptime)}\n{40 * '-'}")

    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start


if __name__ == '__main__':
    main()
