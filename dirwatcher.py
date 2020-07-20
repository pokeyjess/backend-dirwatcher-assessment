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

'''

import signal
import time
import logging
import os

exit_flag = False


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically, it just sets a global flag, and main() will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    global exit_flag
    print(f"Handling signal {signal.Signals(sig_num).name}")
    exit_flag = True
    # call this function when program gets a signal (see below)

    # log the associated signal name
    #logger.warn('Received ' + signal.Signals(sig_num).name)

# function to watch directory

# function to look for magic text


def main():
    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.

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
        print("------------\nExiting normally\n------------")

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        # time.sleep(polling_interval)

    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start


if __name__ == '__main__':
    main()
