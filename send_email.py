cat > send_email.py << 'EOF'
import os, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

smtp_host = os.environ.get("SMTP_HOST")
smtp_port = int(os.environ.get("SMTP_PORT", "465"))
smtp_user = os.environ.get("SMTP_USER")
smtp_pass = os.environ.get("SMTP_PASS")
to_email  = os.environ.get("TO_EMAIL")
report_file = os.environ.get("REPORT_FILE", "reports/report.html")

msg = MIMEMultipart()
msg["From"] = smtp_user
msg["To"] = to_email
msg["Subject"] = "Jenkins 自動化 API 測試報告"

msg.attach(MIMEText("主管您好：\n\n附件為 Jenkins 自動化 API 測試報告。\n\nBest Regards,\nCI/CD 測試系統","plain","utf-8"))

with open(report_file, "rb") as f:
    attach = MIMEApplication(f.read(), _subtype="html")
    attach.add_header("Content-Disposition", "attachment", filename="report.html")
    msg.attach(attach)

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
    server.login(smtp_user, smtp_pass)
    server.sendmail(smtp_user, to_email, msg.as_string())
print("Email sent successfully to", to_email)
EOF
