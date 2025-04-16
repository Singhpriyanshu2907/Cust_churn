import os
import pandas as pd
import numpy as np
from src.logger import auto_logger
from src.custom_exception import CustomException
import yaml
import pandas as pd

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
    

def data_loader(file_path):
    try:
        logger.info(f"Loading data from {file_path}")
        if os.path.exists(file_path):
            data = pd.read_csv(file_path)
            logger.info(f"Data loaded successfully from {file_path}")
            return data
    except Exception as e:
        raise CustomException("Failed to load data",e)
    
