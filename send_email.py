import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# 從 Jenkins 傳入的環境變數
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")
receiver = os.getenv("EMAIL_RECEIVER", sender)  # 沒指定就寄回自己

# 郵件標題與內容
msg = MIMEMultipart()
msg["From"] = sender
msg["To"] = receiver
msg["Subject"] = "Jenkins 測試報告"
msg.attach(MIMEText("您好，這是 Jenkins 自動化測試的結果，請查看附件報告。", "plain"))

# 附加 HTML 報告
report_path = "reports/report.html"
if os.path.exists(report_path):
    with open(report_path, "rb") as f:
        attachment = MIMEApplication(f.read(), Name="report.html")
    attachment['Content-Disposition'] = 'attachment; filename="report.html"'
    msg.attach(attachment)

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender, password)  # 用 Jenkins credentials
    server.sendmail(sender, receiver, msg.as_string())
    print("✅ 郵件寄送成功")
    server.quit()
except Exception as e:
    print("❌ 郵件寄送失敗：", e)
