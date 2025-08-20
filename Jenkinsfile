pipeline {
    agent any

    environment {
        PY_ENV = "venv"
        REPORT_DIR = "reports"
        REPORT_FILE = "reports/report.html"
        SMTP_HOST = "smtp.gmail.com"
        SMTP_PORT = "465"
        TO_EMAIL  = "C107178157@nkust.edu.tw"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm // 從 GitHub 取最新原始碼（Jenkins Job 會指定 repo）
            }
        }
        stage('Setup Python env') {
            steps {
                sh '''
                set -e
                python3 -m venv ${PY_ENV}
                . ${PY_ENV}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }
        stage('Run pytest & report') {
            steps {
                sh '''
                set -e
                . ${PY_ENV}/bin/activate
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
                    set -e
                    . ${PY_ENV}/bin/activate
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
