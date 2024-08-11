import configparser
import sys

from modules.log import log
import os

config = configparser.ConfigParser()

def configwrite():
    if not os.path.exists('discer.q3'):
        log.debug('Config file is missing. Trying to create it.')
        with open('discer.q3', 'w') as file:
            config['Main'] = {
                'PrintDebugLines': True,
                'SimpleVerify': False,
                'CheckOnBadges': True,
                'PrintInvalidTokens': False,
                'sslverificationonrequest': True
            }
            config.write(file)
            log.debug('Config file written.')
            log.info('Config file was created. Please check settings in discer.q3 and restart program.')


def configread():
    try:
        config.read('discer.q3')
        printdebug = config.getboolean('Main', 'printdebuglines')
        simpleverify = config.getboolean('Main', 'simpleverify')
        checkonbadges = config.getboolean('Main', 'checkonbadges')
        printinvalidtokens = config.getboolean('Main', 'printinvalidtokens')
        sslverificationonrequest = config.getboolean('Main', 'sslverificationonrequest')
        return printdebug, simpleverify, checkonbadges, printinvalidtokens, sslverificationonrequest
    except FileNotFoundError:
        log.error('Couldn\'t find discer.q3 config file.')
    except Exception as e:
        log.error('Oops.. Something went wrong. Please contact with Moder. Error: config_configread_Exception')
        log.error(e)
        sys.exit(-2)
    return False, False, False, False, False