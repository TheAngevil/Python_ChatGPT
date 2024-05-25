import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders
from docx2pdf import convert
import json
from pathlib import Path


class MailBridge():
    def __init__(self, password_path=Path("secrets.json").resolve()):
        self.secret = json.load(open(Path(password_path).resolve()))
        self.msg = MIMEMultipart()
        self.sender = "ufo00816@gmail.com"
        self.receiver = "cathay.michael@gmail.com"
        convert("IAmAWord.docx", "covered.pdf")
        self.attach_file_path = "covered.pdf"
        self.msg["Subject"] = Header("Test mail", "utf-8").encode()
        self.body = "This is an email sent by Python"
        self.msg_content = MIMEText(self.body)
        self.msg.attach(self.msg_content)
        print

    def attatch_file(self, attach_path):
        with open(attach_path, "rb") as attach:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attach.read())
            encoders.encode_base64(part)
            part.add_header("content-Disposition", f"attachment; filename={self.attach_file_path}")
            self.msg.attach(part)

    def send_email(self):
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as server:
                server.login("ufo00816@gmail.com", self.secret["gmail_device_password"])
                server.sendmail(self.sender, self.receiver, self.msg.as_string())
        except BaseException:
            print("Email Sending failed")


mail = MailBridge()
mail.attatch_file("./covered.pdf")
mail.send_email()
