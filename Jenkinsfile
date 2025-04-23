pipeline{
    agent any

    environment  {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'cutstomerchurn'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin' 
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to jenkins.............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Singhpriyanshu2907/Cust_churn.git']])
                }
            }
        }

        stage('Setting up venv and installing dependencies'){
            steps{
                script{
                    echo 'Setting up venv and installing dependencies.............'
                    sh '''
                    python3.10 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''                    
                }
            }
        }

        stage('Building & Pushing docker image to GCR'){
            steps{
                withcredentials([file(credentialsId : 'jenkins-secret-gcp', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and Pushing Docker Image to GCR.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker build -t gcr.io/${GCP_PROJECT}/cust-churn:latest .
                        docker push gcr.io/${GCP_PROJECT}/cust-churn:latest
                        '''
                    }
                }
            }
        }
    }
}