import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os

smtp_host = os.environ["SMTP_HOST"]
smtp_port = int(os.environ["SMTP_PORT"])
smtp_user = os.environ["SMTP_USER"]
smtp_pass = os.environ["SMTP_PASS"]
to_email = os.environ["TO_EMAIL"]
report_file = os.environ["REPORT_FILE"]

# 建立安全的 SSL context
context = ssl.create_default_context()

# 建立郵件內容
msg = MIMEMultipart("alternative")
msg["Subject"] = "API Test Report"
msg["From"] = smtp_user
msg["To"] = to_email

# 讀取測試報告
with open(report_file, "r", encoding="utf-8") as f:
    report_html = f.read()

msg.attach(MIMEText(report_html, "html"))

# 寄信
with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
    server.login(smtp_user, smtp_pass)
    server.sendmail(smtp_user, to_email, msg.as_string())
