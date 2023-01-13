# ADPY-62
# Домашнее задание к лекции 7.«Подготовка к собеседованию»
# Задание 3. Почта. Рефакторинг кода.
# https://github.com/netology-code/py-homeworks-advanced/blob/master/7.Interview/PEP8.md

# ИСХОДНЫЙ КОД:

import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

PROVIDER = 'gmail.com'
SMTP_HOST = f'smtp.{PROVIDER}'
IMAP_HOST = f'imap.{PROVIDER}'
SMTP_PORT = 25
START_TLS_PORT = 587
SMTP_over_SSL_PORT = 465


class Post:

    def __init__(self):
        self.my_email = 'kievskiy.s@gmail.com'
        self.password = 'bodkzieztopbxtfu'  # Google password for apps
        self.subject = 'Test mail.'
        self.recipients = ['knhel7@gmail.com', 'knhel7@mail.ru']
        self.header = None

    def send_message(self, message: str = 'My test message'):
        msg = MIMEMultipart()
        msg['From'] = self.my_email
        msg['To'] = ','.join(self.recipients)
        msg['Subject'] = self.subject
        msg['Body'] = "\r\n".join((
            "From: %s" % msg['From'],
            "To: %s" % msg['To'],
            "Subject: %s" % msg['Subject'],
            "",
            message
        ))
        # msg.attach(MIMEText(message, 'plain'))
        msg.attach(MIMEText(message))

        smtp_server = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)

        # identify ourselves to smtp gmail client
        smtp_server.ehlo()
        # secure our email with tls encryption
        smtp_server.starttls()
        # re-identify ourselves as an encrypted connection
        smtp_server.ehlo()

        smtp_server.login(msg['From'], self.password)
        # smtp_server.sendmail(msg['From'], msg['To'], msg.as_string())
        smtp_server.sendmail(msg['From'], msg['To'], msg['Body'])

        smtp_server.quit()

    def receive_message(self):
        mail = imaplib.IMAP4_SSL(IMAP_HOST)
        mail.login(self.my_email, self.password)
        mail.list()
        mail.select("inbox")
        criterion = '(HEADER Subject "%s")' % self.header if self.header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        mail.logout()


#  https://code.tutsplus.com/ru/tutorials/sending-emails-in-python-with-smtp--cms-29975
