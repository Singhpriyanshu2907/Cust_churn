import os
import sys
import pandas as pd
import numpy as np
from src.logger import auto_logger
from src.custom_exception import CustomException
from config.paths import *
from utils.common_func import read_yaml, data_loader
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split


logger = auto_logger(__name__)


class DataProcessing:

    def __init__(self,train_path,test_path,processed_dir,config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config_path = read_yaml(config_path)
        
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    
    def process_data(self,data):
        try:
            logger.info("starting data processing")

            logger.info("Renaming the columns")
            
            data.rename(columns={'Support Calls': 'Support_calls','Usage Frequency':'Usage_frequency','Total Spend':'Total_spend'}, inplace=True)

            logger.info("dropping unecessary columns")
            
            data.drop(columns=['cust_id'], inplace=True)

            logger.info("dropping duplicates")
            
            data.drop_duplicates(inplace = True)

            

        except Exception as e:
            raise CustomException ("Data processing failed",e)