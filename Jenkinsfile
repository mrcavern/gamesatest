pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Running build automation'
                sh './gradlew build --no-daemon'
                archiveArtifacts artifacts: 'app/demoapi.zip'
            }
        }
        stage('Build Docker Image') {
            when {
                branch 'master'
            }
            steps {
                script {
                    app = docker.build("mrcavern/gamesatest")
                    app.inside {
                        sh 'echo $(curl localhost:8080)'
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
                withCredentials([usernamePassword(credentialsId: 'webserver_login', usernameVariable: 'USERNAME', passwordVariable: 'USERPASS')]) {
                    script {
                        sh "sshpass -p '$USERPASS' -v ssh -o StrictHostKeyChecking=no -p2299 $USERNAME@$prod_ip \"docker pull mrcavern/gamesatest:${env.BUILD_NUMBER}\""
                        try {
                            sh "sshpass -p '$USERPASS' -v ssh -o StrictHostKeyChecking=no -p2299 $USERNAME@$prod_ip \"docker stop gamesatest\""
                            sh "sshpass -p '$USERPASS' -v ssh -o StrictHostKeyChecking=no -p2299 $USERNAME@$prod_ip \"docker rm gamesatest\""
                        } catch (err) {
                            echo: 'caught error: $err'
                        }
                        sh "sshpass -p '$USERPASS' -v ssh -o StrictHostKeyChecking=no -p2299 $USERNAME@$prod_ip \"docker run --restart always --name gamesatest -p 8080:8080 -d mrcavern/gamesatest:${env.BUILD_NUMBER}\""
                    }
                }
            }
        }
    }
}