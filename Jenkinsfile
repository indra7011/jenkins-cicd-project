pipeline {
    agent any

    environment {
        IMAGE_NAME = 'my-project-image'
        TAR_FILE = 'my-project-image.tar'
        // REPLACE THIS WITH YOUR PRODUCTION SERVER PRIVATE IP
        PROD_SERVER_IP = '172.31.xx.xx' 
        PROD_USER = 'ubuntu'
        SSH_CRED_ID = 'prod-server-ssh-key' 
    }

    stages {
        stage('1. Fetch Code') {
            steps {
                checkout scm
                echo 'Code fetched successfully.'
            }
        }

        stage('2. Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('3. Convert into Tarfile') {
            steps {
                script {
                    echo 'Saving Docker image to .tar archive...'
                    sh "docker save ${IMAGE_NAME}:latest > ${TAR_FILE}"
                }
            }
        }

        stage('4. Deploy via SCP and Load') {
            steps {
                sshagent(credentials: ["${SSH_CRED_ID}"]) {
                    script {
                        echo 'Transferring .tar file via SCP...'
                        sh "scp -o StrictHostKeyChecking=no ${TAR_FILE} ${PROD_USER}@${PROD_SERVER_IP}:/home/${PROD_USER}/"
                        
                        echo 'Loading image and running container on Production Server...'
                        sh """
                        ssh -o StrictHostKeyChecking=no ${PROD_USER}@${PROD_SERVER_IP} "
                            sudo docker load < /home/${PROD_USER}/${TAR_FILE} &&
                            sudo docker stop my-running-app || true &&
                            sudo docker rm my-running-app || true &&
                            sudo docker run -d --name my-running-app -p 80:80 ${IMAGE_NAME}:latest
                        "
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up local workspace...'
            sh "rm -f ${TAR_FILE}"
            cleanWs()
        }
    }
}
