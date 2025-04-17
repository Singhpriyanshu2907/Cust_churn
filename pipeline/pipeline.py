import sys
import yaml
from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessing
from src.logger import auto_logger
from src.custom_exception import CustomException
from config.paths import *
from utils.common_func import read_yaml

logger = auto_logger(__name__)

class pipeline():

    def __init__(self):
        pass

    def main(self):
        config = read_yaml(config_path)
        #data_ingestion = DataIngestion(config)
        #data_ingestion.run_ingestion()
        data_processing = DataProcessing(train_file_path,test_file_path,processed_dir,config_path)
        data_processing.run_preprocessing()


