from setuptools import setup, find_packages


with open('requirements.txt', 'r') as f: ## Reading the requirements file and storing it in a variable
    # This will read the requirements file and store it in a list
    requirements = f.read().splitlines()



setup(
    name='Customer_churn',
    version='0.1',
    author='priyanshu Singh',
    packages=find_packages(),
    install_requires=requirements
    )