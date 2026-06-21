import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def send_report(
    recipient: str,
    subject: str,
    body_text: str,
    attachment_json: dict | None = None,
    smtp_user: str = "",
    smtp_pass: str = "",
):
    msg = MIMEMultipart("alternative")
    msg["From"] = smtp_user
    msg["To"] = recipient
    msg["Subject"] = subject

    html = f"""<html><body style="font-family: sans-serif;">
<pre style="font-size: 14px; line-height: 1.6;">{body_text}</pre>
<hr><p style="color: #666; font-size: 12px;">Gesendet am {datetime.now().strftime('%d.%m.%Y um %H:%M')}</p>
</body></html>"""

    msg.attach(MIMEText(body_text, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    if attachment_json:
        part = MIMEBase("application", "json")
        part.set_payload(json.dumps(attachment_json, indent=2, ensure_ascii=False))
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            "attachment; filename=assessment_data.json",
        )
        msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, recipient, msg.as_string())
