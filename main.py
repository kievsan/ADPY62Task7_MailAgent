# ADPY-62
# Домашнее задание к лекции 7.«Подготовка к собеседованию»

from email_agent import MailAgent


if __name__ == '__main__':
    gmail_agent = MailAgent('my@example.com')
    gmail_agent.send_message(recipients=['user7@forexample.com', 'user7@example.ru'])
    gmail_agent.receive_message()
