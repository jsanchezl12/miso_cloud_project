from datetime import datetime, timedelta
from flask import request
from flask_restful import Resource, reqparse
from dateutil.parser import parse

PSW_MAIL = 'loucwkjvkpifjiou'
SENDER_MAIL = 'nubedtg23@gmail.com'

class VistaHealthCheck(Resource):
    def get(self):
        return 'pong', 200


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class VistaSendMail(Resource):
    def post(self):
        try:
            data = request.get_json()
            print('data', data)
            receiver = data['receiver']
            subject = data['subject']
            sender = SENDER_MAIL
            password = PSW_MAIL
            message = MIMEMultipart("alternative")
            message["From"] = sender
            message["To"] = receiver
            message["Subject"] = subject #"Send an email in Python"
            body = data['body_mail']
            plain_text = "Send an email with both HTML and plain text."
            mime_text = MIMEText(plain_text)
            message.attach(mime_text)
            html_markup = body # "<h1>Test sending email in Python.<h1>"
            mime_html = MIMEText(html_markup, "html")
            message.attach(mime_html)
            server = smtplib.SMTP(host="smtp.gmail.com", port=587)
            server.starttls(context=ssl.create_default_context())
            server.login(sender, password)

            server.sendmail(
                from_addr=sender,
                to_addrs=receiver,
                msg=message.as_string(),
            )
            server.quit()
            return 'ok', 200
        except Exception as err:
            print("Error sending email: %s" % err)
            return 'Error enviando el correo', 500
