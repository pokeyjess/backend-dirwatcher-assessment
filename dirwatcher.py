# to run program:
# python dirwatcher.py  <directory to watch>  <magic text to search> -e .txt -1 5
# python dirwatcher.py --dir watchdir --ext "txt" --magic magic
'''
s̶i̶g̶n̶a̶l̶ ̶h̶a̶n̶d̶l̶e̶r̶
f̶u̶n̶c̶t̶i̶o̶n̶ ̶t̶o̶ ̶l̶o̶o̶k̶ ̶f̶o̶r̶ ̶m̶a̶g̶i̶c̶ ̶t̶e̶x̶t̶
-logging where found text (currently logging kill signal)
̶t̶i̶m̶e̶s̶t̶a̶m̶p̶
f̶i̶g̶u̶r̶e̶ ̶o̶u̶t̶ ̶h̶o̶w̶ ̶t̶o̶ ̶w̶a̶t̶c̶h̶ ̶a̶ ̶d̶i̶r̶e̶c̶t̶o̶r̶y̶
̶e̶x̶c̶e̶p̶t̶i̶o̶n̶ ̶h̶a̶n̶d̶l̶i̶n̶g̶ ̶t̶o̶ ̶k̶e̶e̶p̶ ̶r̶u̶n̶n̶i̶n̶g̶
̶ ̶ ̶ ̶ ̶w̶h̶e̶n̶ ̶n̶o̶ ̶d̶i̶r̶e̶c̶t̶o̶r̶y̶ ̶f̶o̶u̶n̶d̶
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
import sys

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
    global exit_flag  # false, keeps running program
    logger.debug(f"Handling signal: {signal.Signals(sig_num).name}")
    exit_flag = True
    # call this function when program gets a signal (see below)

    # log the associated signal name

    #  need function to watch directory****

# poll with os.listdir
# keep a list of all files looking at. add new files to be watched?
# then go through each file


def watch_directory(directory, magic, extension, interval):
    """"Watches a directory, looking for files
    Then checks files for a "magic" text provided on command line
    """
    # create dictionary
    files_list = {}
    # log what it's doing
    logger.info(
        f'Watching "{directory}" to see if files with a "{extension}" extension contain "{magic}"')
    # loop through directory, check for file/extension
    # add files to dictionary
    # and log now watching the file
    while not exit_flag:
        for file in os.listdir(directory):
            if file.endswith(str(extension)) and file not in files_list:
                files_list[file] = 0
                logger.info(f'Now watching: {file}')
    # remove files that no longer exist
    # log that has been deleted
    # add time stamp!
        for file in list(files_list):
            if file not in os.listdir(directory):
                files_list.pop(file)
                logger.info(f'The file {file} has been deleted')
    # loop through files, look for text.
    # log if found (function find_magic_text does that)
        for file in files_list:
            full_path = os.path.join(directory, file)
            files_list[file] = find_magic_text(
                full_path, text, files_list[file])
    # put to sleep before running through all over again
        time.sleep(interval)


'''
#timestamps for when file is deleted
#also for when directory is deleted!
And for when magic is found

# dictionary.
# The keys = filenames
# values = last line position -- each entry, file and last line
open, readlines. read line by line

# Keep track of the last position.

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
# add a time stamp!


def create_parser():
    """creates command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', help="Directory to watch")
    parser.add_argument('--ext', help="File extension to filter on")
    parser.add_argument('--int', default=1.0,
                        help="Polling interval")
    parser.add_argument('--magic', help="Magic text to look for")
    return parser


app_start_time = datetime.datetime.now()


def main():
    parser = create_parser()
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.
# startup banner:

    logger.info(
        f"\n{40 * '-'}\n Running: {__file__}\n Started on: {app_start_time.isoformat()}\n{40 * '-'}")
    while not exit_flag:
        try:
            print(f"[{os.getpid()}] Tick...")
            # call my directory watching function..
            watch_directory(args.dir, args.magic, args.ext, args.int)
        except FileNotFoundError:
            logger.warning("Did not find that directory")
            # raise
        except Exception as e:
            logger.error(f'Unhandeled exception:{e}')
        time.sleep(3.0)
    uptime = datetime.datetime.now() - app_start_time
    logger.info(
        f"\n{40 * '-'}\n Stopped: {__file__}\n Uptime was: {str(uptime)}\n{40 * '-'}")


# put a sleep inside my while loop so I don't peg the cpu usage at 100%
# time.sleep(polling_interval)

if __name__ == '__main__':
    main()
