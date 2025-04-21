import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from src.logger import auto_logger
from src.custom_exception import CustomException
from config.paths import *
from config.model_params import *
from utils.common_func import read_yaml, data_loader, clean_column_names
from scipy.stats import randint
import mlflow
import mlflow.sklearn


logger = auto_logger(__name__)


class ModelTrainer():

    def __init__(self,train_path,test_path,model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.params = lgm_params
        self.random_search_params = random_search_params

    
    def load_split_data(self):

        try:
            logger.info("Starting loading train-data for model_training")
            train_data = data_loader(self.train_path)
            train_data = clean_column_names(train_data)

            logger.info("Starting loading test-data for model_training")
            test_data = data_loader(self.test_path)
            test_data = clean_column_names(test_data)

            logger.info("Splitting data into x_train, y_train, x_test and y_test")

            x_train = train_data.drop(columns=['booking_status'])
            y_train = train_data['booking_status']

            x_test = test_data.drop(columns=['booking_status'])
            y_test = test_data['booking_status']

            logger.info("Sucessfully Splited data into x_train, y_train, x_test and y_test")

            return x_train,y_train,x_test,y_test

        except Exception as e:
            logger.error(f"Error during loading data {e}")
            raise CustomException("Failed to load data", e)
        
    
    def model_trainer(self,x_train,y_train):

        try:

            logger.info("Initializing model")
            model = lgb.LGBMClassifier(random_state = self.random_search_params['random_state'])

            logger.info("Initializing random search CV for hyper-parameter tuning")
            random_search = RandomizedSearchCV(

                            estimator = model,
                            param_distributions = self.params,
                            n_iter = self.random_search_params['n_iter'],
                            cv = self.random_search_params['cv'],
                            n_jobs = self.random_search_params['n_jobs'],
                            verbose = self.random_search_params['verbose'],
                            random_state = self.random_search_params['random_state'],
                            scoring = self.random_search_params['scoring'],
                            error_score='raise'
            )

            logger.info("Starting hyper-parameter tuning model training")
            random_search.fit(x_train,y_train)

            logger.info("Saving best parameters")
            best_params = random_search.best_params_
            logger.info("Saving best model")
            best_model = random_search.best_estimator_

            return best_model

        except Exception as e:
            logger.error(f"Model training failed {e}")
            raise CustomException("Failed to train model", e)
        
    
    def evaluator(self,model,x_test,y_test):
        try:
            logger.info("starting prediction on x_test")
            y_pred = model.predict(x_test)

            logger.info("Collecting evaluation scores")
            accuracy = accuracy_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)
            F1_score = f1_score(y_test,y_pred)

            logger.info(f"Accuracy Score : {accuracy}")
            logger.info(f"Precision Score : {precision}")
            logger.info(f"Recall Score : {recall}")
            logger.info(f"F1_Score : {F1_score}")

            return {

                'Accuracy' : accuracy,
                'Precision' : precision,
                'recall' : recall,
                'F1_score' : F1_score
            }

        except Exception as e:
            logger.error(f"Failed to Evaluate Model {e}")
            raise CustomException("Failed to Evaluate Model", e)
        
    
    def save_model(self,model):
        try:
            logger.info("Initializing to save model")
            
            model_dir = os.path.dirname(self.model_output_path)
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)

            logger.info("saving model")
            joblib.dump(model,self.model_output_path)

            logger.info("Model saved succesfully")
                        
        except Exception as e:
            logger.error(f"Error while saving Model {e}")
            raise CustomException("Failed to save Model", e)
        
    def run_modeltrainer(self):
        try:
            with mlflow.start_run():
                logger.info("Starting Model Trainer Pipeline")

                logger.info("starting mlflow experimentation")

                logger.info("Logging the training and testing dataset with MLflow")
                mlflow.log_artifact(self.train_path, artifact_path = 'Datasets')
                mlflow.log_artifact(self.test_path, artifact_path = 'Datasets')

                x_train,y_train,x_test,y_test = self.load_split_data()
                best_model = self.model_trainer(x_train,y_train)
                evaluation = self.evaluator(best_model,x_test,y_test)
                self.save_model(best_model)

                logger.info("Logging the model into mlflow")
                mlflow.log_artifact(self.model_output_path)

                logger.info("Logging the params & metrics into mlflow")
                mlflow.log_params(best_model.get_params())
                mlflow.log_metrics(evaluation)

                logger.info("Model Training pipeline completed")

        except Exception as e:
            logger.error(f"Error while running mode_trainer {e}")
            raise CustomException("Failed to run model-trainer", e)