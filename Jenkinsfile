pipeline {
    agent any

    environment {
        EMAIL_RECEIVER = '收件者@gmail.com'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/arnohsu/api_test_project.git'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest tests/ --junitxml=reports/results.xml --html=reports/report.html --self-contained-html
                '''
            }
        }

        stage('Collect Results') {
            steps {
                junit 'reports/results.xml'
            }
        }

        stage('Publish HTML Report') {
            steps {
                publishHTML(target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'API 測試報告'
                ])
            }
        }
    }

    post {
        always {
            withCredentials([usernamePassword(
                credentialsId: 'my-smtp-cred',
                usernameVariable: 'EMAIL_USER',
                passwordVariable: 'EMAIL_PASS'
            )]) {
                sh '''
                    source venv/bin/activate
                    python send_email.py
                '''
            }
        }
    }
}
