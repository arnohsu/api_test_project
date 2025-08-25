import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

# 讀取 Jenkins 傳入的參數
subject = sys.argv[1] if len(sys.argv) > 1 else "Jenkins 測試報告"
body = sys.argv[2] if len(sys.argv) > 2 else "您好，這是 Jenkins 自動化測試的結果，請查看附件報告。"
sender = sys.argv[3] if len(sys.argv) > 3 else None
password = sys.argv[4] if len(sys.argv) > 4 else None
receiver = sender  # 可以改成固定收件人或從參數傳入

if not sender or not password:
    print("❌ 發送失敗：缺少郵件帳號或密碼")
    sys.exit(1)

# 建立郵件
msg = MIMEMultipart()
msg["From"] = sender
msg["To"] = receiver
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

# 附件
report_path = "reports/report.html"
if os.path.exists(report_path):
    with open(report_path, "rb") as f:
        attachment = MIMEApplication(f.read(), Name="report.html")
    attachment['Content-Disposition'] = 'attachment; filename="report.html"'
    msg.attach(attachment)

# 寄送
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    print("✅ 郵件寄送成功")
    server.quit()
except Exception as e:
    print("❌ 郵件寄送失敗：", e)
