#### Customer Churn Prediction
Predicting customer churn using machine learning with automated CI/CD deployment.

## Table of Contents
:- Project Overview
:- Project Structure
:- Requirements
:- Setup Instructions
    1. Jenkins Setup with Docker
    2. Project Dockerfile
    3. Google Cloud CLI Installation on Jenkins
    4. Docker Permissions for Jenkins User
:- CI/CD Pipeline Overview
:- Deployment
:- Usage
:- License

## Project Overview
This project implements a Customer Churn Prediction system using Python and machine learning libraries. The model is trained on customer data to predict churn, helping businesses retain customers proactively.

## The project includes:

:- Data ingestion, processing, and model training pipelines.
:- A Flask web application for serving predictions.
:- CI/CD pipeline using Jenkins, Docker, GitHub, Google Cloud Platform (GCP) Container Registry, and Cloud Run for automated build, test, and deployment.

## Project Structure

*************************************************************************************************************************************************************

CUST_CHURN/ │ ├── artifacts/ # Model artifacts and outputs │ ├── models/ │ ├── processed/ │ └── raw/ │ ├── config/ # Configuration files and model params │ ├── __pycache__/ │ ├── config.yaml │ ├── model_params.py │ └── paths.py │ ├── custom_jenkins/ # Jenkins Docker setup for CI/CD │ ├── Dockerfile │ └── Jenkinsfile │ ├── github/ # GitHub related files (e.g., workflows) │ ├── logs/ # Logs for training and pipeline runs │ ├── mlruns/ # MLflow experiment tracking data │ ├── notebooks/ # Jupyter notebooks for experiments │ ├── experiments.ipynb │ └── train.csv │ ├── pipeline/ # Training pipeline scripts │ ├── __pycache__/ │ └── pipeline.py │ ├── src/ # Source code for ingestion, processing, training │ ├── __pycache__/ │ ├── custom_exception.py │ ├── data_ingestion.py │ ├── data_processing.py │ ├── logger.py │ └── model_trainer.py │ ├── static/ # Static files for Flask app (CSS, images) │ └── style.css │ ├── templates/ # HTML templates for Flask app │ └── index.html │ ├── utils/ # Utility functions │ ├── __pycache__/ │ └── common_func.py │ ├── venv/ # Python virtual environment │ ├── .gitignore ├── app.py # Flask application entry point ├── Dockerfile # Dockerfile for project container ├── Jenkinsfile # Jenkins pipeline script ├── LICENSE ├── main.py # Main script to run training or inference ├── README.md ├── requirements.txt # Python dependencies └── setup.py # Package setup script

***************************************************************************************************************************************************************

## Requirements
**The project uses the following Python packages with specific versions to ensure compatibility:**

pandas==1.5.3 numpy==1.24.4 scikit-learn==1.2.2 scipy==1.10.1 pyyaml==6.0 pydantic==1.10.7 google-cloud-storage==2.8.0 matplotlib==3.7.4 seaborn==0.12.2 imbalanced-learn==0.10.1 lightgbm==3.3.5 mlflow==2.10.0 Flask==2.2.5

## Setup Instructions

1. Jenkins Setup with Docker
We use a custom Jenkins container with Docker-in-Docker (DinD) support to enable building and running Docker images inside Jenkins.

Create a folder custom_jenkins and add the following Dockerfile:
dockerfile

Copy
# Use the Jenkins image as the base image
FROM jenkins/jenkins:lts
# Switch to root user to install dependencies
USER root
# Install prerequisites and Docker
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean
# Add Jenkins user to the Docker group (create if it doesn't exist)
RUN groupadd -f docker && \
    usermod -aG docker jenkins
# Create the Docker directory and volume for DinD
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker
# Switch back to the Jenkins user
USER jenkins
Build and run the Jenkins container:
bash

Copy
cd custom_jenkins
docker build -t jenkins-dind .
docker run -d --name jenkins-dind --privileged -p 8080:8080 -p 50000:50000 -v //var/run/docker.sock:/var/run/docker.sock -v jenkins_home:/var/jenkins_home jenkins-dind
Access Jenkins at http://localhost:8080, enter the initial admin password from logs:
bash

Copy
docker logs jenkins-dind
Install suggested plugins and create your admin user.

Install Python and pip inside Jenkins container:

bash

Copy
docker exec -u root -it jenkins-dind bash
apt update -y
apt install -y python3 python3-pip python3-venv
ln -s /usr/bin/python3 /usr/bin/python
exit
docker restart jenkins-dind
2. Project Dockerfile
The project Dockerfile builds the app container, installs dependencies, trains the model, and runs the Flask app.

dockerfile

Copy
# Use a lightweight Python image
FROM python:slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY . .
RUN pip install --no-cache-dir -e .
RUN python pipeline/training_pipeline.py
EXPOSE 5000
CMD ["python", "application.py"]
3. Google Cloud CLI Installation on Jenkins
To deploy on GCP, install Google Cloud SDK inside Jenkins container:

bash

Copy
docker exec -u root -it jenkins-dind bash
apt-get update
apt-get install -y curl apt-transport-https ca-certificates gnupg
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
apt-get update && apt-get install -y google-cloud-sdk
gcloud --version
exit
4. Docker Permissions for Jenkins User
Grant Docker permissions to Jenkins user to allow building and running containers:

bash

Copy
docker exec -u root -it jenkins-dind bash
groupadd docker
usermod -aG docker jenkins
usermod -aG root jenkins
exit
docker restart jenkins-dind
CI/CD Pipeline Overview
Source Control: GitHub repository hosting the project code.
Build & Test: Jenkins builds the Docker image, runs tests, and trains the model.
Container Registry: Docker images are pushed to Google Container Registry (GCR).
Deployment: Google Cloud Run deploys the containerized Flask app for serving predictions.
CI/CD Pipeline

Deployment
Build Docker Image:
bash

Copy
docker build -t gcr.io/<your-project-id>/customer-churn:latest .
Push to Google Container Registry:
bash

Copy
docker push gcr.io/<your-project-id>/customer-churn:latest
Deploy to Cloud Run:
bash

Copy
gcloud run deploy customer-churn-service --image gcr.io/<your-project-id>/customer-churn:latest --platform managed --region <region> --allow-unauthenticated
Usage
Access the Flask web app via the Cloud Run URL.
Upload customer data or input features to get churn predictions.
Monitor model performance and retrain using the pipeline as needed.
License
This project is licensed under the MIT License.
