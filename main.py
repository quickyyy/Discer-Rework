import logging
import os
import sys
import time
import urllib3
import warnings
import requests
from modules.config import configwrite, configread
from modules.fileworker import readtokens,writetoken,writeinfo,readproxy
from modules.checkers import *
from modules.log import printlogo
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_billing(token, proxy=None):
    if proxy is not None:
        if proxytype == 'Socks5':
            proxy = {
                    'http': f'socks5://{proxy}',
                    'https':f'socks5://{proxy}'

                }  
        elif proxytype == 'http':
            proxy = {
                    'http': f'{proxy}',
                    'https':f'{proxy}'

                } 
    else:
        proxy = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
        'Authorization': token
    }
    if proxy is not None:
        if sslverificationonrequest:
            response = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers=headers, proxies=proxy)
        else:
            response = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers=headers, proxies=proxy, verify=False)
    else:
        if sslverificationonrequest:
            response = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers=headers)
        else:
            response = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers=headers, verify=False)
    #log.debug(response.text)
    resjson = response.json()
    if 'code' in resjson and resjson['code'] == 40002:
        log.debug('Account unverified. Billing check impossible.')
        return None
    if resjson:
        for source in resjson:
            if source['type'] == 1:
                last_4 = source['brand'] + ' ' + source['last_4']
                log.debug(f"Found card - {last_4}")
                return last_4
        log.debeg(f"Doesn't have card.")
        return None
    log.error(f"Billing info not found.")
    return None

def check_token(token, proxy=None):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
            'Authorization': token
        }
        if proxy is not None:
            if proxytype == 'Socks5':
                proxy = {
                    'http': f'socks5://{proxy}',
                    'https': f'socks5://{proxy}'
                }
            elif proxytype == 'http':
                proxy = {
                    'http': f'{proxy}',
                    'https': f'{proxy}'
                }
            if sslverificationonrequest:
                response = requests.get('https://discord.com/api/v9/users/@me', headers=headers, proxies=proxy)
            else:
                response = requests.get('https://discord.com/api/v9/users/@me', headers=headers, verify=False, proxies=proxy)
            cards = check_billing(token=token, proxy=proxy)
        else:
            if sslverificationonrequest:
                response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
            else:
                response = requests.get('https://discord.com/api/v9/users/@me', headers=headers, verify=False)
            cards = check_billing(token=token)

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
            check('Card', cards)
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
                                 f'Badges - {badges}\n'
                                 f'Card - {cards}')
                writeinfo(info_to_write)
            return True

        try:
            response_json = response.json()
            log.debug(f'Response JSON type: {type(response_json)}')
            if isinstance(response_json, dict) and 'message' in response_json:
                message = response_json['message']
            else:
                message = ''
                log.debug('No "message" key found or response is not a dictionary')
        except ValueError as e:
            log.debug(f'Response is not JSON: {e}')
            message = ''

        if '401' in message:
            log.debug('testcheck 124')
            log.error(f'Invalid - {token}')
        else:
            log.debug('testcheck 127')
            log.error(f'Hmm... It seems like bug...')
            log.debug(response.text)

        return

    except Exception as e:
        log.error(f'Invalid - {token}')
        log.debug(f'Exception occurred: {e}')




if __name__ == '__main__':
    try:
        os.system('cls')
        configwrite()
        printdebug, simpleverify, checkonbadges, sslverificationonrequest, num_threads, writefulllogs, useproxy, proxytype = configread()
        printlogo()

        if useproxy:
            log.warning(f'Useproxy function has been detected. Keep in mind what this function in early access')

        if not sslverificationonrequest:
            log.warning('SSL Verification is turned off. Be careful!')

        time.sleep(1)
        tokens_file = log.input('Please, enter fullpath/name of tokens.txt file: ')
        tokens = readtokens(tokens_file)
        log.info(f'Successfully found {len(tokens)} tokens')
        proxy_file = log.input('Please, enter a fullpath/name of proxy.txt file (or leave this clear): ')
        if proxy_file is not '': 
            proxy = readproxy(proxy_file)
            log.info(f'Successfully found {len(proxy)} proxy')
        else:
            log.info('Proxy disabled.')
            proxy = None
        if proxy == None:
            if num_threads == False:
                log.debug('Got error while getting number of threads, using 1 thread')
                with ThreadPoolExecutor() as executor:
                    executor.map(check_token, tokens)
            else:
                log.debug(f'Using {num_threads} threads')
                with ThreadPoolExecutor(max_workers=num_threads) as executor:
                    executor.map(check_token, tokens)
        else:
            if num_threads == False:
                log.debug('Got error while getting number of threads, using 1 thread')
                with ThreadPoolExecutor() as executor:
                    executor.map(check_token, tokens, proxy)
            else:
                log.debug(f'Using {num_threads} threads')
                with ThreadPoolExecutor(max_workers=num_threads) as executor:
                    executor.map(check_token, tokens, proxy)
        log.info('All work is done! See you soon!')
        log.input("Press any key to exit...")
        sys.exit(0)
    except KeyboardInterrupt:
        logging.warning('User pressed Ctrl+C, exiting...')