import sys
import yaml
from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessing
from src.model_trainer import ModelTrainer
from src.logger import auto_logger
from src.custom_exception import CustomException
from config.paths import *
from config.model_params import *
from utils.common_func import read_yaml, data_loader, clean_column_names

logger = auto_logger(__name__)

class pipeline():

    def __init__(self):
        pass

    def main(self):
        
        config = read_yaml(config_path)
        
        
        ##### DATA INGESTION PIPELINE #####
        #data_ingestion = DataIngestion(config)
        #data_ingestion.run_ingestion()
        

        ##### DATA PROCESSING PIPELINE #####
        # data_processing = DataProcessing(train_file_path,test_file_path,processed_dir,config_path)
        # data_processing.run_preprocessing()


        ##### MODEL TRAINING PIPELINE #####
        model_training = ModelTrainer(processed_train_data_path,processed_test_data_path,model_path)
        model_training.run_modeltrainer()



