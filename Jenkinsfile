pipeline{
    agent any

    environment  {
        VENV_DIR = 'venv'
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
    }
}