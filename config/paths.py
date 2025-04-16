import os


################## DATA INGESTION ###################


raw_dir = "artifacts/raw"
raw_file_path = os.path.join(raw_dir, "raw.csv")
train_file_path = os.path.join(raw_dir, "train.csv")
test_file_path = os.path.join(raw_dir, "test.csv")

config_path = "config/config.yaml"



############### DATA PROCESSING #######################

processed_dir = "artifacts/processed"
processed_train_data_path = os.path.join(processed_dir,"processed_train.csv")
processed_test_data_path = os.path.join(processed_dir,"processed_test.csv")