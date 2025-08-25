import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Jenkins 會提供的環境變數
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")
REPORT_FILE = os.getenv("REPORT_FILE", "reports/report.html")

def send_report():
    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = TO_EMAIL

    # 判斷測試結果（依照 reports/results.xml）
    subject = "【API 測試報告】結果通知"
    body_status = "⚠️ 測試完成，但無法判斷狀態"

    if os.path.exists("reports/results.xml"):
        with open("reports/results.xml", "r") as f:
            xml_content = f.read()
            if "failures=\"0\"" in xml_content and "errors=\"0\"" in xml_content:
                subject = "【API 測試報告】✅ 全部通過"
                body_status = "測試狀態：✅ 全部通過"
            else:
                subject = "【API 測試報告】❌ 測試失敗"
                body_status = "測試狀態：❌ 發生失敗，請檢查 Jenkins"

    msg["Subject"] = subject

    body = f"""
    <p>您好，</p>
    <p>{body_status}</p>
    <p>完整測試內容請參考附件 <code>report.html</code>，或至 Jenkins UI 的「API 測試報告」分頁查看。</p>
    <p>自動化測試系統</p>
    """
    msg.attach(MIMEText(body, "html"))

    # 附加 HTML 測試報告
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "rb") as f:
            report = MIMEApplication(f.read(), Name="report.html")
        report["Content-Disposition"] = 'attachment; filename="report.html"'
        msg.attach(report)

    # 發送郵件
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, TO_EMAIL, msg.as_string())
        print("✅ 郵件已成功寄出！")
    except Exception as e:
        print("❌ 郵件寄送失敗：", str(e))

if __name__ == "__main__":
    send_report()
