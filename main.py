import logging
import os
import time
import urllib3
import warnings
import requests
from modules.config import configwrite, configread
from modules.fileworker import readtokens,writetoken,writeinfo
from modules.checkers import *
from modules.log import printlogo
from concurrent.futures import ThreadPoolExecutor

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
            nitro_type = check_nitro(response)
            if checkonbadges:
                badges = check_badges(response)
                check('Badges on account:', badges)
            if writefulllogs:
                log.debug('If writefulllogs')
                info_to_write = (f'Token - {token}\n'
                                 f'Display name - {global_name}\n'
                                 f'Email - {email}\n'
                                 f'Phone - {phone}\n'
                                 f'Verified - {verified}\n'
                                 f'Nitro - {nitro_type}\n'
                                 f'Badges - {badges}\n')
                writeinfo(info_to_write)
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
    try:
        os.system('cls')
        configwrite()
        printdebug, simpleverify, checkonbadges, printinvalidtokens, sslverificationonrequest, num_threads, writefulllogs = configread()
        printlogo()

        if checkonbadges:
            log.warning(
                f'A badges check function has been detected,'
                f' please note that this function has not been tested under working conditions'
                f' and may not work correctly or may cause program crashes')

        if not sslverificationonrequest:
            log.warning('SSL Verification is turned off. Be careful!')

        time.sleep(1)
        tokens_file = log.input('Please, enter fullpath/name of tokens.txt file:')
        tokens = readtokens(tokens_file)
        log.info(f'Successfully found {len(tokens)} tokens')

        if num_threads == False:
            log.debug('Got error while getting number of threads, using 1 thread')
            with ThreadPoolExecutor() as executor:
                executor.map(check_token, tokens)
        else:
            log.debug(f'Using {num_threads} threads')
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                executor.map(check_token, tokens)
        log.info('All work is done! See you soon!')
        log.input("Press any key to exit...")
        sys.exit(0)
    except KeyboardInterrupt:
        logging.warning('User pressed Ctrl+C, exiting...')