import configparser
import os

import sys

from modules.log import log


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
                'sslverificationonrequest': True,
                'numberOfThreads': 4,
                'writefulllogs': False,
                'useproxy': False,
            }
            config.write(file)
            log.debug('Config file written.')
            log.info(
                'Config file was created. Please check settings in discer.q3 and restart program.'
            )



def configread():
    try:
        config.read('discer.q3')
        printdebug = config.getboolean('Main', 'printdebuglines')
        simpleverify = config.getboolean('Main', 'simpleverify')
        checkonbadges = config.getboolean('Main', 'checkonbadges')
        sslverificationonrequest = config.getboolean('Main', 'sslverificationonrequest')
        writefulllogs = config.getboolean('Main', 'writefulllogs')
        numberofthreads = config.getint('Main', 'numberOfThreads')
        useproxy = config.getboolean('Main', 'useproxy')
        proxytype = config.get('Main', 'proxytype')
        return (
            printdebug,
            simpleverify,
            checkonbadges,
            sslverificationonrequest,
            numberofthreads,
            writefulllogs,
            useproxy,
            proxytype
        )
    except FileNotFoundError:
        log.error('Couldn\'t find discer.q3 config file.')
    except Exception as e:
        log.error(
            'Oops.. Something went wrong. Please contact with Moder. Error: config_configread_Exception'
        )
        log.error(e)
        sys.exit(-2)
    return False, False, False, False, False, False, False, False, False