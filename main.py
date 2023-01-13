# ADPY-62
# Домашнее задание к лекции 7.«Подготовка к собеседованию»

from email_agent import MailAgent


if __name__ == '__main__':
    gmail_agent = MailAgent('kievskiy.s@gmail.com')
    gmail_agent.send_message(recipients=['knhel7@gmail.com', 'knhel7@mail.ru'])
    gmail_agent.receive_message()
