import os
import time
import urllib3
import warnings
import requests
from modules.config import configwrite, configread
from modules.fileworker import readtokens,writetoken
from modules.checkers import *
from modules.log import printlogo

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_token(token):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
            'Authorization': token
        }
        if sslverificationonrequest:
            response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
        else:
            response = requests.get('https://discord.com/api/v9/users/@me', headers=headers, verify=False)
        log.debug(f'Trying to check token {token}')
        if response.status_code == 200:
            login, email, phone, verified, global_name = getinfo(response)
            writetoken(token=token)
            log.info(f'Good token - {token}')
            if simpleverify:
                return
            check('Display name', global_name)
            check('Username', login)
            check('Email', email)
            check('Phone', phone)
            check('Verified', verified)
            check_nitro(response)
            if checkonbadges:
                check('Badges on account:', check_badges(response))
            return True
        else:
            if printinvalidtokens:
                log.error(f'Invalid - {token}')
            else:
                log.error('Something went wrong, or token is invalid')
            log.debug(response.text)
            return
    except urllib3.exceptions.SSLError as e:
            log.error(
                'Error with connecting to Discord because of SSL error. Try to turn off SSL verification in config.')

if __name__ == '__main__':
    os.system('cls')
    configwrite()
    printdebug, simpleverify, checkonbadges, printinvalidtokens, sslverificationonrequest = configread()
    printlogo()
    if checkonbadges:
        log.warning(
            f'A badges check function has been detected,'
            f' please note that this function has not been tested under working conditions'
            f' and may not work correctly or may cause program crashes')
    if not sslverificationonrequest:
        log.warning('Ssl Verification is turned off. Be careful!')
    time.sleep(1)
    tokens_file = log.input('Please, enter fullpath/name of tokens.txt file:')
    tokens = readtokens(tokens_file)
    log.info(f'Successfully found {len(tokens)} tokens')
    for token in tokens:
        check_token(token)
    log.info('All work is done! See you soon!')
    log.input("press any key to exit...")
    sys.exit(0)