import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from time import gmtime

DATE_TIME_FORMAT_LOGGING = '%Y-%b-%d %H:%M:%S'
FORMATTER = logging.Formatter('%(asctime)s.%(msecs)03d UTC - %(process)d - %(levelname)s '
                              '%(message)s', DATE_TIME_FORMAT_LOGGING)
FORMATTER.converter = gmtime


def setup_logger(log_file: str | Path | None = None, level: str = 'INFO'):
    root = logging.getLogger()
    root.setLevel(level)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(FORMATTER)
    if log_file:
        Path(log_file).parent.mkdir(exist_ok=True, parents=True)
        file_handler = RotatingFileHandler(filename=log_file,
                                           mode='a',
                                           maxBytes=10 * 1024,
                                           backupCount=1,
                                           encoding=None,
                                           delay=False,
                                           )
        file_handler.setFormatter(FORMATTER)
        file_handler.setLevel(level=level)
        root.addHandler(file_handler)
    root.addHandler(stream_handler)
    logging.captureWarnings(True)
