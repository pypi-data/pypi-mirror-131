import os
import logging
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler


def init_logger(
    name = 'default_logger',
    log_path = '/var/log/slg/default_location.log',
    log_level = logging.INFO,
    stream_log_level = logging.DEBUG,
    formatter_str = '%(asctime)s | %(levelname)-8s | Line %(lineno)-4s | %(pathname)s | %(message)s'
) -> logging.Logger:
    '''
    It's recommended to set name = __name__ as the name parameter when calling this function in order to get the logger name to be the same as the file's name.

    It's also advised to set the log_path to "/var/log/slg/{__file__.split("/")[-1]}.log" when calling from a script so you don't log to a default file but also one relevant to the script.
    '''

    try:
        logger = logging.getLogger(name)
        file_handler = RotatingFileHandler(log_path, maxBytes=10000000, backupCount=5)
        stream_handler = StreamHandler()

        file_formatter = Formatter(formatter_str, datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(file_formatter)

        # we also log to the stream where the logs are saved
        stream_formatter = Formatter(f'------- Log message saved to {log_path} ------- \n' + formatter_str, datefmt='%Y-%m-%d %H:%M:%S')
        stream_handler.setFormatter(stream_formatter)

        stream_handler.setLevel(stream_log_level)
        logger.addHandler(stream_handler)

        logger.setLevel(log_level)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)

        return logger

    except FileNotFoundError:
        print(f'\nLogging directory not found. Please create {os.path.dirname(log_path)} directory and change the user to the user running this script')
        print('\nUse the following commands to create the directory and set the user to the user running this script:')
        print(f'\nsudo mkdir -p {os.path.dirname(log_path)}')
        print(f'sudo chown -R $USER:$USER {os.path.dirname(log_path)}')
        exit(0)
