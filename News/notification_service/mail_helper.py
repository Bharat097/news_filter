import os
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings


def send_email(to_email, data, category):

    subject = "New news of your subscribed category - {}".format(category)
    body = "This is an email sent from Python Service. Click on link to authenticate news of {} category.".format(category)
    sender_email = settings.SENDER_EMAIL
    password = settings.SENDER_PASSWORD

    if not sender_email or not password:
        print("Please configure email/password in .env")
        return False

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(to_email)
    message["Subject"] = subject

    for k, v in data.items():
        body = '<a href="{}">{}</a>'.format(v, k)
        message.attach(MIMEText(body, "html"))

    text = message.as_string()
    # print(text)

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, text)

    return True
