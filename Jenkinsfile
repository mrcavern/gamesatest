pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Running build automation'
            }
        }
        stage('Build Docker Image') {
            when {
                branch 'master'
            }
            steps {
                script {
                    app = docker.build("dcuevas86/gamesademo")
                    app.inside {
                        sh 'echo $(curl localhost:8080)'
                    }
                }
            }
        }
        stage('Push Docker Image') {
            when {
                branch 'master'
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker_hub_id') {
                        app.push("${env.BUILD_NUMBER}")
                        app.push("latest")
                    }
                }
            }
        }
        stage('DeployToProduction') {
            when {
                branch 'master'
            }
            steps {
                input 'Deploy to Production?'
                milestone(1)
                withCredentials([usernamePassword(credentialsId: 'webserver_login', usernameVariable: 'USERNAME', passwordVariable: 'SSHPASS')]) {
                    script {
                        sh "sshpass -p 'Cueva\$\$18' ssh -o StrictHostKeyChecking=no -p2299 $USERNAME@$prod_ip \"docker pull dcuevas86/gamesademo:${env.BUILD_NUMBER}\""
                        try {
                            sh "sshpass -p 'Cueva\$\$18' ssh -o StrictHostKeyChecking=no -p2299 $USERNAME@$prod_ip \"docker stop gamesademo\""
                            sh "sshpass -p 'Cueva\$\$18' ssh -o StrictHostKeyChecking=no -p2299 $USERNAME@$prod_ip \"docker rm gamesademo\""
                        } catch (err) {
                            echo: 'caught error: $err'
                        }
                        sh "sshpass -p 'Cueva\$\$18' ssh -o StrictHostKeyChecking=no -p2299 $USERNAME@$prod_ip \"docker run --restart always --name gamesademo -p 5050:5000 -d dcuevas86/gamesademo:${env.BUILD_NUMBER}\""
                    }
                }
            }
        }
    }
}
