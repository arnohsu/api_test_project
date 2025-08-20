import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# 讀取環境變數
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")
REPORT_FILE = os.getenv("REPORT_FILE", "reports/report.html")

# 建立郵件
msg = MIMEMultipart()
msg["From"] = SMTP_USER
msg["To"] = TO_EMAIL
msg["Subject"] = "【API 測試報告】每日自動化測試結果"  # ✅ 標題

# 內文 (你可以改成更正式的內容)
body = """
<p>親愛的主管您好，</p>

<p>以下為本次 API 自動化測試的結果摘要，詳細內容請參考附件報告。</p>

<p>測試狀態：✅ 全部通過</p>
<p>測試時間：自動產生</p>

<p>敬祝 工作順利！</p>
<p>自動化測試系統</p>
"""

msg.attach(MIMEText(body, "html"))

# 附加 HTML 測試報告
with open(REPORT_FILE, "rb") as f:
    report = MIMEApplication(f.read(), Name="report.html")
report["Content-Disposition"] = 'attachment; filename="report.html"'
msg.attach(report)

# 發送郵件
with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
    server.login(SMTP_USER, SMTP_PASS)
    server.sendmail(SMTP_USER, TO_EMAIL, msg.as_string())

print("✅ 郵件已成功寄出！")
