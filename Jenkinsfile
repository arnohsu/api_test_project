pipeline {
    agent any

    environment {
        REPORT_DIR = "reports"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/arnohsu/api_test_project.git'
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/ --junitxml=${REPORT_DIR}/results.xml --html=${REPORT_DIR}/report.html --self-contained-html
                '''
            }
        }

        stage('Collect Results') {
            steps {
                junit "${REPORT_DIR}/results.xml"
            }
        }

        stage('Publish HTML Report') {
            steps {
                publishHTML(target: [
                    allowMissing: false,
                    keepAll: true,
                    reportDir: "${REPORT_DIR}",
                    reportFiles: 'report.html',
                    reportName: 'API 測試報告'
                ])
            }
        }
    }

    post {
        success {
            withCredentials([usernamePassword(credentialsId: 'gmail-credentials', usernameVariable: 'SMTP_USER', passwordVariable: 'SMTP_PASS')]) {
                sh '''
                    . venv/bin/activate
                    python send_email.py "API 自動化測試成功 ✅" "測試狀態：全部通過 🎉\\n詳細報告請參考附件。" "${SMTP_USER}" "${SMTP_PASS}" "C107178157@nkust.edu.tw"
                '''
            }
        }
        failure {
            withCredentials([usernamePassword(credentialsId: 'gmail-credentials', usernameVariable: 'SMTP_USER', passwordVariable: 'SMTP_PASS')]) {
                sh '''
                    . venv/bin/activate
                    python send_email.py "API 自動化測試失敗 ❌" "測試失敗，請盡快檢查 Jenkins 中的測試結果！" "${SMTP_USER}" "${SMTP_PASS}" "C107178157@nkust.edu.tw"
                '''
            }
        }
    }
}
