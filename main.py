# def main():
#     print("Hello from cust-churn!")




from src.logger import auto_logger
from src.custom_exception import CustomException
import sys

logger = auto_logger(__name__)

def divide(a, b):
    try:
        logger.info("Dividing two numbers")
        return a / b
    except Exception as e:
        raise CustomException(e, sys)    



if __name__ == "__main__":
    try:
        divide(10, 0)
    except CustomException as e:
        logger.error(str(e))