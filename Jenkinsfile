pipeline {
    agent any
    environment {
        PY_ENV = "venv"
        REPORT_DIR = "reports"
        REPORT_FILE = "reports/report.html"
        SMTP_HOST = "smtp.gmail.com"
        SMTP_PORT = "465"
        TO_EMAIL = "example@example.com" // 替換為你的收件人郵件地址
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup Python env') {
            steps {
                sh '''
                python3 -m venv ${PY_ENV}
                source ${PY_ENV}/bin/activate
                echo "pytest" > requirements.txt
                echo "requests" >> requirements.txt
                echo "pytest-html" >> requirements.txt
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }
        stage('Run pytest & report') {
            steps {
                sh '''
                source ${PY_ENV}/bin/activate
                mkdir -p ${REPORT_DIR}
                pytest tests/ --html=${REPORT_FILE} --self-contained-html
                '''
            }
        }
        stage('Archive report') {
            steps {
                archiveArtifacts artifacts: "${REPORT_FILE}", fingerprint: true
            }
        }
        stage('Send email') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'SMTP_CRED', usernameVariable: 'SMTP_USER', passwordVariable: 'SMTP_PASS')]) {
                    sh '''
                    source ${PY_ENV}/bin/activate
                    export SMTP_HOST=${SMTP_HOST}
                    export SMTP_PORT=${SMTP_PORT}
                    export TO_EMAIL=${TO_EMAIL}
                    export REPORT_FILE=${REPORT_FILE}
                    python3 send_email.py
                    '''
                }
            }
        }
    }
}
