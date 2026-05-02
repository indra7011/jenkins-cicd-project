pipeline {
    agent any

    environment {
        IMAGE_NAME = 'my-project-image'
        TAR_FILE = 'my-project-image.tar'
        // ENSURE THIS IS YOUR PRODUCTION SERVER PRIVATE IP
        PROD_SERVER_IP = '172.31.43.253' 
        PROD_USER = 'ubuntu'
        SSH_CRED_ID = 'prod-server-ssh-key' 
    }

    stages {
        stage('1. Fetch Code') {
            steps {
                checkout scm
            }
        }

        stage('2. Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('3. Prepare Deployment Artifacts') {
            steps {
                // Fixed: Added the > to ensure the image is saved to the file
                sh "docker save ${IMAGE_NAME}:latest > ${TAR_FILE}"
            }
        }

        stage('4. Deploy to Kubernetes') {
            steps {
                sshagent(credentials: ["${SSH_CRED_ID}"]) {
                    script {
                        echo 'Transferring image and YAML files...'
                        sh "scp -o StrictHostKeyChecking=no ${TAR_FILE} deployment.yaml service.yaml ${PROD_USER}@${PROD_SERVER_IP}:/home/${PROD_USER}/"
                        
                        echo 'Updating Kubernetes Cluster...'
                        sh """
                        ssh -o StrictHostKeyChecking=no ${PROD_USER}@${PROD_SERVER_IP} "
                            # Using absolute paths so SSH can find the commands
                            /usr/local/bin/minikube image load ${IMAGE_NAME}:latest
                            
                            /usr/local/bin/kubectl apply -f deployment.yaml
                            /usr/local/bin/kubectl apply -f service.yaml
                            
                            /usr/local/bin/kubectl rollout restart deployment/my-app-deployment
                        "
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            sh "rm -f ${TAR_FILE}"
            cleanWs()
        }
    }
}
