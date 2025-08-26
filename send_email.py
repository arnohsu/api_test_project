import smtplib
import sys
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def main():
    if len(sys.argv) < 6:
        print("❌ 使用方式: python send_email.py <主題> <內容> <寄件人> <密碼> <收件人>")
        sys.exit(1)

    subject = sys.argv[1]
    body = sys.argv[2]
    sender = sys.argv[3]
    password = sys.argv[4]
    receiver = sys.argv[5]

    # 郵件標題與內容
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body.replace("\\n", "\n"), "plain"))

    # 附加 HTML 報告
    report_path = "reports/report.html"
    if os.path.exists(report_path):
        with open(report_path, "rb") as f:
            attachment = MIMEApplication(f.read(), Name="report.html")
        attachment['Content-Disposition'] = 'attachment; filename="report.html"'
        msg.attach(attachment)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        print(f"✅ 郵件已成功寄送給 {receiver}")
        server.quit()
    except Exception as e:
        print("❌ 郵件寄送失敗：", e)

if __name__ == "__main__":
    main()
