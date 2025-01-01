import logging
import sys


class LoggerConfigurator:
    @staticmethod
    def configure(logging_level_str: str) -> None:
        logging_level: int = LoggerConfigurator.__get_logging_level_from_string(logging_level_str)

        logging.basicConfig(level=logging_level, format='[%(levelname)s][%(name)s] %(message)s', stream=sys.stdout)

    @staticmethod
    def __get_logging_level_from_string(logging_level_str: str) -> int:
        if logging_level_str == 'debug':
            return logging.DEBUG
        if logging_level_str == 'info':
            return logging.INFO
        if logging_level_str == 'warn':
            return logging.WARNING
        if logging_level_str == 'error':
            return logging.ERROR
        if logging_level_str == 'fatal':
            return logging.FATAL

        raise Exception(f'Unable to get logging level from string - unknown logging level "{logging_level_str}"!')
