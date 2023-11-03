import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO

import qrcode
from dotenv import load_dotenv

load_dotenv()


def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


"""
Я не буду предоставлять свои креды реальные для отправки email, вставлю тестовые данные
"""


def send_qr_code_email(distributor):
    qr_data = (
        f"Distributor: {distributor.name_of_manufacture}, Email: {distributor.email}"
    )

    qr_code = generate_qr_code(qr_data)

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = os.getenv("EMAIL_HOST_USER")
    smtp_password = os.getenv("EMAIL_HOST_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = "test@gmail.com"
    msg["To"] = distributor.email
    msg["Subject"] = "QR Code for Distributor"

    text = MIMEText("Here is your QR code:")
    msg.attach(text)

    img = MIMEImage(qr_code)
    msg.attach(img)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, "vladpomalejko@gmail.com", msg.as_string())
        server.quit()
        print(f"QR code sent to {distributor.email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
