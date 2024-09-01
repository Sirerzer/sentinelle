import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from config import email_from , email_to , smtp_password , smtp_port , smtp_server , smtp_username  , smtp_notifications

def send_email(message):
    if smtp_notifications:
        try:
            email_message = MIMEMultipart()
            email_message["From"] = email_from
            email_message["To"] = email_to
            email_message["Subject"] = "Nofication"

            email_message.attach(MIMEText(message, "plain"))

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                server.login(smtp_username, smtp_password)
                server.sendmail(email_from, email_to, email_message.as_string())

            print("Email envoyé avec succès")

        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email : {e}")