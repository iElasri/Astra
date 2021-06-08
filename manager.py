import os
import pickle
import configparser
from time import sleep
from datetime import datetime

from colorama import init, Fore
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
from telethon.sync import TelegramClient
from modules.sms import GetSMSCode
from modules.configuration import Configuration

cfg_obj = Configuration()
config = cfg_obj.load()
sms = GetSMSCode(config)

api_id = config['myTelegram']['api_id']
api_hash = config['myTelegram']['api_hash']

init()

n = Fore.RESET
lg = Fore.LIGHTGREEN_EX
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [lg, r, w, cy, ye]

try:
    import requests
except ImportError:
    print(f'{lg}[i] Installing module - requests...{n}')
    os.system('pip install requests')


def banner():
    import random
    # fancy logo
    b = [
        '   _____             __',
        '  /  _  \    _______/  |_____________',
        ' /  /_\  \  /  ___/\   __\_  __ \__  \\',
        '/    |    \ \___ \  |  |  |  | \// __ \_',
        '\____|__  /____  >  |__|  |__|  (____   /',
        '        \/     \/                     \/'
    ]
    for char in b:
        print(f'{random.choice(colors)}{char}{n}')
    # print('=============SON OF GENISYS==============')
    print(f'   Version: 1.0 | Author: Cryptonian{n}\n')


def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def phone_code_callback(order_id):
    start_time = datetime.now()
    print(str(start_time) + " Waiting for Actication Code.")
    while True:
        sleep(10)
        status = sms.getStatus(order_id)["status"]
        elapsed = (datetime.now() - start_time).total_seconds()
        print(str(elapsed) + "Seconds :" + status, end='\r')
        if elapsed > 180:
            sms.setStatus(order_id, 'STATUS_CANCEL')
            return -1
        elif status == "STATUS_CANCEL":
            return -1
        elif status == "STATUS_OK":
            return sms.getStatus(order_id)['code']


while True:
    clr()
    banner()
    print(lg + '[0] Add Account from sms.avtivate' + n)
    print(lg + '[1] Add new accounts' + n)
    print(lg + '[2] Filter all banned accounts' + n)
    print(lg + '[3] Delete specific accounts' + n)
    print(lg + '[4] Update your Astra' + n)
    print(lg + '[5] Quit' + n)
    a = int(input('\nEnter your choice: '))
    if a == 0:
        new_accs = []
        with open('vars.txt', 'ab') as g:
            print("Balance is : " + sms.getBalance)
            ORDER_ID, phone_number = sms.get_mobile_number()  # Get the phone number from the API
            parsed_number = ''.join(phone_number.split())  # re -----

            new_accs.append(parsed_number)

            print(f'\n{lg} [i] Saved the {phone_number} in vars.txt')
            clr()
            print(f'\n{lg} [*] Logging in from new accounts\n')
            for number in new_accs:
                c = TelegramClient(f'sessions/{number}', api_id, api_hash)  # Change his api and hash
                try:
                    c.start(phone=number, code_callback=phone_code_callback(ORDER_ID))
                    pickle.dump([parsed_number], g)
                    print(f'{lg}[+] Login successful')
                    c.disconnect()
                except Exception as e:
                    print(e)
                    print(f'\n{lg} [*] An Error Happened Number Not registred \n')

            input(f'\n Press enter to goto main menu...')

        g.close()
    elif a == 1:
        new_accs = []
        with open('vars.txt', 'ab') as g:
            number_to_add = int(input(f'\n{lg} [~] Enter number of accounts to add: {r}'))
            for i in range(number_to_add):
                phone_number = str(input(f'\n{lg} [~] Enter Phone Number: {r}'))
                parsed_number = ''.join(phone_number.split())
                pickle.dump([parsed_number], g)
                new_accs.append(parsed_number)
            print(f'\n{lg} [i] Saved all accounts in vars.txt')
            clr()
            print(f'\n{lg} [*] Logging in from new accounts\n')
            for number in new_accs:
                c = TelegramClient(f'sessions/{number}', api_id,
                                   api_hash)  # Change his api and hash
                c.start(number)
                print(f'{lg}[+] Login successful')
                c.disconnect()
            input(f'\n Press enter to goto main menu...')

        g.close()
    elif a == 2:
        accounts = []
        banned_accs = []
        h = open('vars.txt', 'rb')
        while True:
            try:
                accounts.append(pickle.load(h))
            except EOFError:
                break
        h.close()
        if len(accounts) == 0:
            print(r + '[!] There are no accounts! Please add some and retry')
            sleep(3)
        else:
            for account in accounts:
                phone = str(account[0])
                client = TelegramClient(f'sessions/{phone}', api_id, api_hash)
                client.connect()
                if not client.is_user_authorized():
                    try:
                        client.send_code_request(phone)
                        # client.sign_in(phone, input('[+] Enter the code: '))
                        print(f'{lg}[+] {phone} is not banned{n}')
                    except PhoneNumberBannedError:
                        print(r + str(phone) + ' is banned!' + n)
                        banned_accs.append(account)
            if len(banned_accs) == 0:
                print(lg + 'Congrats! No banned accounts')
                input('\nPress enter to goto main menu...')
            else:
                for m in banned_accs:
                    accounts.remove(m)
                with open('vars.txt', 'wb') as k:
                    for a in accounts:
                        Phone = a[0]
                        pickle.dump([Phone], k)
                k.close()
                print(lg + '[i] All banned accounts removed' + n)
                input('\nPress enter to goto main menu...')

    elif a == 3:
        accs = []
        f = open('vars.txt', 'rb')
        while True:
            try:
                accs.append(pickle.load(f))
            except EOFError:
                break
        f.close()
        i = 0
        print(f'{lg}[i] Choose an account to delete\n')
        for acc in accs:
            print(f'{lg}[{i}] {acc[0]}{n}')
            i += 1
        index = int(input(f'\n{lg}[+] Enter a choice: {n}'))
        phone = str(accs[index][0])
        session_file = phone + '.session'
        if os.name == 'nt':
            os.system(f'del sessions\\{session_file}')
        else:
            os.system(f'rm sessions/{session_file}')
        del accs[index]
        f = open('vars.txt', 'wb')
        for account in accs:
            pickle.dump(account, f)
        print(f'\n{lg}[+] Account Deleted{n}')
        input(f'\nPress enter to goto main menu...')
        f.close()
    elif a == 4:
        # thanks to github.com/th3unkn0n for the snippet below
        print(f'\n{lg}[i] Checking for updates...')
        try:
            # https://raw.githubusercontent.com/Cryptonian007/Astra/main/version.txt
            version = requests.get('https://raw.githubusercontent.com/Cryptonian007/Astra/main/version.txt')
        except:
            print(f'{r} You are not connected to the internet')
            print(f'{r} Please connect to the internet and retry')
            exit()
        if float(version.text) > 1.1:
            prompt = str(input(f'{lg}[~] Update available[Version {version.text}]. Download?[y/n]: {r}'))
            if prompt == 'y' or prompt == 'yes' or prompt == 'Y':
                print(f'{lg}[i] Downloading updates...')
                if os.name == 'nt':
                    os.system('del add.py')
                    os.system('del manager.py')
                else:
                    os.system('rm add.py')
                    os.system('rm manager.py')
                # os.system('del scraper.py')
                os.system('curl -l -O https://raw.githubusercontent.com/Cryptonian007/Astra/main/add.py')
                os.system('curl -l -O https://raw.githubusercontent.com/Cryptonian007/Astra/main/manager.py')
                print(f'{lg}[*] Updated to version: {version.text}')
                input('Press enter to exit...')
                exit()
            else:
                print(f'{lg}[!] Update aborted.')
                input('Press enter to goto main menu...')
        else:
            print(f'{lg}[i] Your Astra is already up to date')
            input('Press enter to goto main menu...')
    elif a == 5:
        clr()
        banner()
        exit()
