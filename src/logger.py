import logging
import os
from datetime import datetime


log_dir = "logs"

## creates a log directory if it does not exist
if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"log-{datetime.now().strftime('%y-%m-%d')}.log")

logging.basicConfig(

    filename=log_file,
    level = logging.INFO,
    format = "[%(asctime)s] %(levelname)s - %(message)s"

)


def auto_logger(name):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    return logger


