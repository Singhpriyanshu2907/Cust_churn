import yaml
from pipeline.pipeline import pipeline

if __name__ == "__main__":
    try:
        obj = pipeline()
        obj.main()
    except Exception as e:
        print(e)