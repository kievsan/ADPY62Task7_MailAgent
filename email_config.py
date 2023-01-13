import configparser


class MailConfig:
    config = configparser.ConfigParser()

    try:
        config.read('email_agent.ini')

        GOOGLE = config['Google']
        VK = config['VKontakte']
        YA = config['Yandex']

        GOOGLE_ACC_pwd = GOOGLE['password']
        VK_ACC_pwd = VK['password']
        YA_ACC_pwd = YA['password']

    except Exception as err:
        print('Отсутствует настройки почтового агента!', err)
        GOOGLE_ACC_pwd = ''
        VK_ACC_pwd = ''
        YA_ACC_pwd = ''

    if not (GOOGLE_ACC_pwd and VK_ACC_pwd and YA_ACC_pwd):

        while not GOOGLE_ACC_pwd:
            GOOGLE_ACC_pwd = input('\nGoogle account password / password for app: ').strip()
        config['Google'] = {
            'provider': 'gmail.com',
            'smtp_port': 25,
            'smtp_host': 'smtp.gmail.com',
            'imap_port': 25,
            'imap_host': 'imap.gmail.com',
            'password': GOOGLE_ACC_pwd
        }

        while not VK_ACC_pwd:
            VK_ACC_pwd = input('\nVK account password / password for app: ').strip()
        config['VKontakte'] = {
            'provider': 'mail.ru',
            'smtp_port': 25,
            'smtp_host': '',
            'imap_port': 25,
            'imap_host': '',
            'password': VK_ACC_pwd
        }

        while not YA_ACC_pwd:
            YA_ACC_pwd = input('\nVK account password / password for app: ').strip()
        config['Yandex'] = {
            'provider': 'yandex.ru',
            'smtp_port': 25,
            'smtp_host': '',
            'imap_port': 25,
            'imap_host': '',
            'password': YA_ACC_pwd
        }

        GOOGLE = config['Google']
        VK = config['VKontakte']
        YA = config['Yandex']

        with open('email_agent.ini', 'w') as configfile:
            config.write(configfile)
