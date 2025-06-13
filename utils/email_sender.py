import smtplib
from email.mime.text import MIMEText
from config import Config

def send_email(recipient, name):
    subject = "[NO REPLY!] Pendaftaran Berhasil"
    body = f"Halo {name},\n\nTerima kasih telah mendaftar! Kami telah menerima pendaftaran Anda.\n\nSalam,\nTim Kami"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = Config.EMAIL_SENDER
    msg['To'] = recipient

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(Config.EMAIL_SENDER, Config.EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email terkirim ke {recipient}")
    except Exception as e:
        print(f"Gagal mengirim email: {e}")
