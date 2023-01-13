# ADPY-62
# Домашнее задание к лекции 7.«Подготовка к собеседованию»
# Задание 3. Почтовый агент. Рефакторинг кода.
# https://github.com/netology-code/py-homeworks-advanced/blob/master/7.Interview/PEP8.md


from email_config import MailConfig
from pprint import pprint
import re

import smtplib
import imaplib
import email
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import getpass


def check_email(text: str):
    text = text.strip()
    if not text:
        return ''

    addr = text.split('@')
    if not len(addr) or len(addr) > 2:
        return ''

    mail_addr = addr[0].strip()
    mail_domain = addr[1]
    if not (mail_domain and addr):
        return ''

    domains = mail_domain.split('.')
    for domain_ in domains:
        if domain_.strip() == '':
            return ''

    if not mail_addr[0].isalpha():
        return ''

    return f'{mail_addr}@{mail_domain}'


def get_recipients(recipients: list = None):
    def get_emails(recipients_: list):
        recipients_ = (check_email(recipient_.strip()) for recipient_ in recipients_)
        recipients_ = [recipient_ for recipient_ in recipients_ if recipient_]
        return recipients_

    recipients = get_emails(recipients)
    while not recipients:
        to_emails = input('\nВведите emails получателей через запятую: ').strip()
        recipients = get_emails([','.join(to_emails)])
    return recipients


def get_sender(sender: str = ''):
    providers = MailConfig()
    provider = {}
    sender = check_email(sender)
    while not provider:
        while not sender:
            self_email = input('\nВведите свой email: ').strip()
            sender = check_email(self_email)
        email_addr = sender.split('@')
        domain = email_addr[1]
        if domain == providers.GOOGLE['provider']:
            provider = providers.GOOGLE
        elif domain == providers.VK['provider']:
            provider = providers.VK
        elif domain == providers.YA['provider']:
            provider = providers.YA
        else:
            print('Провайдер не опознан. Выберите подходящий email из',
                  f"{providers.GOOGLE['provider']},",
                  f"{providers.VK['provider']},",
                  f"{providers.YA['provider']},")
            sender = ''

    username = ''
    while not username:
        username = input('\nInput your mail username: ').strip()
        if not username[0].isalpha():
            print('\tThe name must start with a letter...')
            username = ''

    return sender, username, provider


class MailAgent:

    def __init__(self, self_email: str = ''):
        self.my_email, self.my_name, self.provider = get_sender(self_email)
        self.header = None
        print(f'\nThe mail agent has been created for {self.my_name}!')

    def send_message(self, subject: str = 'Test mail.',
                     message: str = 'My test message',
                     recipients: list = None,
                     smtp_port: int = 0):
        def print_result():
            print(f'Отправлено сообщение:\n\t {message}'
                  f'\nна тему "{subject}" ',
                  f'по email-адресам:\n\t{recipients}\n')

        recipients = get_recipients(recipients)
        msg = MIMEMultipart()
        msg['From'] = self.my_email
        msg['To'] = ','.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))  # plain, html

        smtp_server = smtplib.SMTP(host=self.provider['smtp_host'],
                                   port=self.provider['smtp_port'] if not smtp_port else smtp_port)

        smtp_server.ehlo()  # identify ourselves to smtp gmail client
        smtp_server.starttls()  # secure our email with tls encryption
        smtp_server.ehlo()  # re-identify ourselves as an encrypted connection

        smtp_server.login(msg['From'], self.provider['password'])
        smtp_server.sendmail(msg['From'], recipients, msg.as_string())

        print_result()
        smtp_server.quit()

    def receive_message(self):
        print('Connecting to', self.provider['imap_host'])
        mail = imaplib.IMAP4_SSL(host=self.provider['imap_host'])  # , port=self.provider['imap_port'])

        print('Logging in as', self.my_email)
        try:
            mail.login(self.my_email, self.provider['password'])
        except Exception as err:
            print('ERROR!', err)
            mail.logout()
            return

        typ, resp = mail.list()
        print('Response code: ', typ)
        print('Response:')
        pprint(resp)

        mail.select("inbox".upper())
        criterion = '(HEADER Subject "%s")' % self.header if self.header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        pprint(raw_email)

        email_message = email.message_from_string(raw_email)
        pprint(email_message)

        mail.logout()


