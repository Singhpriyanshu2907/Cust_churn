import os
import pandas as pd
import numpy as np
from src.logger import auto_logger
from src.custom_exception import CustomException
import yaml

logger = auto_logger(__name__)


def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found at : {file_path}")
        
        with open(file_path, "r") as y_file:
            config = yaml.safe_load(y_file)
        return config
    except Exception as e:
        raise CustomException(e)
