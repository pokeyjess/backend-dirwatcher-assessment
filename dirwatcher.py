# to run program:
# python dirwatcher.py  <directory to watch>  <magic text to search> -e .txt -1 5

'''
signal handler
function to look for magic text
logging where found text
timestamp
figure out how to watch a directory
exception handling to keep running
    when no directory found
argparse, add arguments
shutdown and start up banners
tests
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


#  need function to watch directory****


def find_magic_text(filename, last_position, magic_text):
    """
   Function to look for magic text
   Searches for magic text in file (from last line position)

    """
    line_number = 0
    with open(filename) as file:
        for line_number, line in enumerate(file):
            if line_number >= last_position:
                if magic_text in line:
                    logger.info(
                        f'Magic text: "{magic_text}", found at line: {line_number + 1} in: {filename}')
    return line_number + 1


# need argparse

def main():
    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.

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
            print("Did not find that file")
            raise  # need this to avoid infinite loop!!!!
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            pass

        # exit banner. make separate function?
        print(f"{16 * '-'}\nExiting normally\n{16 * '-'}")

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        # time.sleep(polling_interval)

    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start


if __name__ == '__main__':
    main()
