pipeline {
    agent any

    environment {
        VENV = "venv"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/arnohsu/api_test_project.git'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''#!/bin/bash
                python3 -m venv $VENV
                source $VENV/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''#!/bin/bash
                source $VENV/bin/activate
                mkdir -p reports
                pytest --junitxml=reports/results.xml --html=reports/report.html --self-contained-html
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
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'API 測試報告'
                ])
            }
        }
    }

    post {
        always {
            sh '''#!/bin/bash
            source $VENV/bin/activate
            python send_email.py
            '''
        }
    }
}
