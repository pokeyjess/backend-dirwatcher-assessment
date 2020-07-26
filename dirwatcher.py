__author__ = 'pokeyjess, help from demos, Google searches, tips from Justin'

import signal
import time
import logging
import os
import datetime
import argparse

exit_flag = False

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d &%H:%M:%S')


def signal_handler(sig_num, frame):
    """
    Sets global flag, and handles SIGTERM and SIGINT signals.
    Will exit the loop if signal is detected.
    """
    global exit_flag
    logger.debug(f"Handling signal: {signal.Signals(sig_num).name}")
    exit_flag = True


def watch_directory(directory, magic, extension, interval):
    """"
    Watches a directory, looking for files with provided extension.
    Logs when file found, and if/when it is later deleted
    """
    files_list = {}
    while not exit_flag:
        for file in os.listdir(directory):
            if file.endswith(str(extension)) and file not in files_list:
                files_list[file] = 0
                logger.info(f'Now watching: {file}')
        for file in list(files_list):
            if file not in os.listdir(directory):
                files_list.pop(file)
                logger.info(f'The file {file} has been deleted')
        for file in files_list:
            full_path = os.path.join(directory, file)
            files_list[file] = find_magic_text(
                full_path, files_list[file], magic)
        time.sleep(interval)


def find_magic_text(filename, last_position, magic_text):
    """
   Searches for provided 'magic' text in file (from last line position)
   Logs the line number where found
   """
    line_number = 0
    with open(filename) as file:
        file = file.readlines()
        for line_number, line in enumerate(file):
            if line_number >= last_position:
                if magic_text in line:
                    logger.info(
                        f'"{magic_text}" at: {line_number + 1} in: {filename}'
                    )
    return line_number + 1


def create_parser():
    """
    Creates command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help="Directory to watch")
    parser.add_argument('--ext', default="txt",
                        help="File extension to filter on")
    parser.add_argument('--int', type=float, default=1.0,
                        help="Polling interval")
    parser.add_argument('magic', help="Magic text to look for")
    return parser


app_start_time = datetime.datetime.now()


def main():
    """
    Uses exception handler to keep the program running.
    Displays starting and ending banners
    """
    parser = create_parser()
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    logger.info(
        f'''\n{40 * '-'}\n Running: {__file__}\n \
Started on: {app_start_time.isoformat()}\n{40 * '-'}''')
    print(f"Process number: {os.getpid()} now running...")
    while not exit_flag:
        try:
            watch_directory(args.dir, args.magic, args.ext, args.int)
        except FileNotFoundError:
            logger.warning(f"Did not find {args.dir}")
        except Exception as e:
            logger.error(f'Unhandeled exception:{e}')
        time.sleep(3.0)
    uptime = datetime.datetime.now() - app_start_time
    logger.info(
        f'''\n{40 * '-'}\n Stopped: {__file__}\n \
Uptime was: {str(uptime)}\n{40 * '-'}''')


if __name__ == '__main__':
    main()
