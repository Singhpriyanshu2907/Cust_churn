import os
import pathlib

list_of_files = [
    "github/workflows/.gitkeep",
    "src/__init__.py",
    "artifacts/",  
    "config/__init__.py",  
    "notebooks/experiments.ipynb",
    "static/",
    "templates/",
    "utils/__init__.py",
    "requirements.txt",
    "setup.py"
]

for filepath in list_of_files:
    filepath = pathlib.Path(filepath)

    if filepath.suffix:  # If there's a file extension, treat it as a file
        filedir = filepath.parent
        if filedir and not filedir.exists():
            os.makedirs(filedir, exist_ok=True)  # Create the parent directory if it doesn't exist

        if not filepath.exists():  # Create file only if it doesn't exist
            with open(filepath, "w") as f:
                pass
            print(f"Created empty file: {filepath}")

    else:  # If no file extension, treat it as a folder
        if not filepath.exists():
            os.makedirs(filepath, exist_ok=True)
            print(f"Created directory: {filepath}")
