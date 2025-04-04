import os
import sys
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import auto_logger
from src.custom_exception import CustomException
from config.paths import *
from utils.common_func import read_yaml

logger = auto_logger(__name__)


class DataIngestion():

    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]
        self.test_ratio = self.config["test_ratio"]

    os.makedirs(raw_dir, exist_ok=True)

    logger.info("Data Ingestion started from GCP bucket")

    
    
    def data_downloader(self):

        '''
        This function downloads the data from the GCP bucket and saves it to the local directory.

        '''
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            blob.download_to_filename(raw_file_path)
            logger.info(f"Data downloaded from GCP bucket {self.bucket_name} to {raw_file_path}")
        except Exception as e:
            logger.error(f"Error in data downloader: {e}")
            raise CustomException(e,sys)

    
    def train_test_data_split(self):

        '''
        This function splits the data into train and test sets and saves them to the local directory.
        The train and test sets are saved as CSV files.

        '''

        try:
            df = pd.read_csv(raw_file_path)
            
            logger.info(f"Data loaded from {raw_file_path}")

            train_data, test_data = train_test_split(df, test_size=self.test_ratio, random_state=42)

            train_data.to_csv(train_file_path, index=False)
            test_data.to_csv(test_file_path, index=False)

            logger.info(f"Data split into train and test sets and saved to {train_file_path} and {test_file_path}")

        except Exception as e:
            logger.error(f"Error in train test split: {e}")
            raise CustomException(e,sys)
    

    def run_ingestion(self):

        '''
        This function runs the data ingestion pipeline.

        '''

        try:
            self.data_downloader()
            self.train_test_data_split()
            logger.info("Data ingestion completed successfully")
        except Exception as e:
            logger.error(f"Error in data ingestion: {e}")
            raise CustomException(e,sys)
        

