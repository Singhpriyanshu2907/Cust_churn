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
        self.config = read_yaml(config_path)
        
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

            cat_cols = self.config["data_processing"]["categorical_col"]
            num_cols = self.config["data_processing"]["numerical_col"]

            logger.info("Applying label encoding")

            label_encoder = LabelEncoder()

            mappings = {}
            for col in cat_cols:
                data[col] = label_encoder.fit_transform(data[col])
                mappings[col] = {label:code for label,code in zip(label_encoder.classes_,label_encoder.transform(label_encoder.classes_))}

            logger.info("label mappings are :")
            for col,mappings in mappings.items():
                logger.info(f"{col}:{mappings}")
            
            logger.info("Handling Skewness")

            skew_threshold = self.config["data_processing"]["skewness_threshold"]

            skewness = data[num_cols].apply(lambda x:x.skew())

            for col in skewness[skewness>skew_threshold].index:
                data[col] = np.log1p(data[col])
            
            return data

            

        except Exception as e:
            logger.error(f"Error during preprocess step {e}")
            raise CustomException ("Data processing failed",e)
    

    def balance_data(self,data):

        try:
            logger.info("Handling imbalanced dataset")
            x = data.drop(columns="booking_status")
            y = data["booking_status"]

            smote = SMOTE(random_state= 42)

            x_resampled,y_resampled = smote.fit_resample(x,y)

            balance_df = pd.DataFrame(x_resampled,columns=x.columns)
            balance_df["booking_status"] = y_resampled

            logger.info("data balancing completed")

            return balance_df
        
        except Exception as e:
            logger.error(f"Error during data_balancing step {e}")
            raise CustomException("Balancing dataset failed")
        
    
    def select_features(self,balance_df):
        try:
            logger.info("Starting our Feature selection step")

            X = balance_df.drop(columns='booking_status')
            y = balance_df["booking_status"]

            model =  RandomForestClassifier(random_state=42)
            model.fit(X,y)

            feature_importance = model.feature_importances_

            feature_importance_df = pd.DataFrame({
                        'feature':X.columns,
                        'importance':feature_importance
                            })
            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)

            num_features_to_select = self.config["data_processing"]["num_of_features"]

            top_10_features = top_features_importance_df["feature"].head(num_features_to_select).values

            logger.info(f"Features selected : {top_10_features}")

            top_10_df = balance_df[top_10_features.tolist() + ["booking_status"]]

            logger.info("Feature slection completed sucesfully")

            return top_10_df
        
        except Exception as e:
            logger.error(f"Error during feature_selection step {e}")
            raise CustomException("Error while feature selection", e)
    
    
    def data_save(self,df,file_path):
        try:
            logger.info("Saving processed data")
            df.to_csv(file_path)

        except Exception as e:
            logger.error(f"Error during data_saving step {e}")
            raise CustomException("Data saving after pre-processing failed")

    
    
    def run_preprocessing(self):

        '''
        This function runs the data processing pipeline.

        '''

        try:
            test_df = data_loader(self.test_path)
            train_df = data_loader(self.train_path)
            
            test_df = self.process_data(test_df)
            train_df = self.process_data(train_df)
            
            test_df = self.balance_data(test_df)
            train_df = self.balance_data(train_df)
            
            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]
            
            test_df = self.data_save(test_df,processed_test_data_path)
            train_df = self.data_save(train_df,processed_train_data_path)
            
            logger.info("Data pre-processing completed successfully")
        except Exception as e:
            logger.error(f"Error in data pre-processing: {e}")
            raise CustomException(e,sys)