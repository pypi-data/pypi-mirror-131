import os
import logging
from pathlib import Path

### @package log_setup
#
# Setup of logging
#

# path for databases or config files
log_path = f'{Path.home()}/.domain-check/'
if not os.path.exists(log_path):
    os.mkdir(log_path)

# set logging format
formatter = logging.Formatter("[{asctime}] [{levelname}] [{module}.{funcName}] {message}", style="{")

# logger for writing to file
file_logger = logging.FileHandler(f'{log_path}/events.log')
file_logger.setFormatter(formatter)

# logger for console prints
console_logger = logging.StreamHandler()
console_logger.setFormatter(formatter)

# get new logger
logger = logging.getLogger('domain-check')
logger.setLevel(logging.DEBUG)

# register loggers
logger.addHandler(file_logger)
logger.addHandler(console_logger)
