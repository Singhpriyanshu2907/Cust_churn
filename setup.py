from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='Customer_churn',
    version='0.1',
    author='Priyanshu Singh',
    packages=find_packages(where='.', exclude=['tests*']),  # Modified this line
    install_requires=requirements,
    python_requires='>=3.10',
)