pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-ci-demo'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        CONTAINER_NAME = 'flask-app'
        APP_PORT   = '5000'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Installing dependencies and linting...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install flake8
                    flake8 app/ --max-line-length=120 --ignore=E501,W292
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests with coverage...'
                sh '''
                    . venv/bin/activate
                    pytest tests/ -v --cov=app \
                           --cov-report=xml:coverage.xml \
                           --cov-report=term-missing
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag  ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                echo 'Deploying container...'
                sh '''
                    docker rm -f ${CONTAINER_NAME} || true
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p ${APP_PORT}:5000 \
                        --restart unless-stopped \
                        ${IMAGE_NAME}:latest
                    echo "App running at http://localhost:${APP_PORT}"
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! App is live.'
        }
        failure {
            echo 'Pipeline failed. Check the logs above.'
        }
        always {
            sh 'rm -rf venv || true'
        }
    }
}
