import sys
from modules.log import log
import os

def readtokens(filename):
    filename = filename.strip('\'"')
    if not os.path.isabs(filename):
        filename = os.path.abspath(filename)
        log.debug(f'Converted relative path to absolute path: {filename}')

    log.debug(f'Trying to read tokens from file: {filename}')
    lines = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                lines.append(line.strip())
        log.debug(f'Successfully read {len(lines)} tokens.')
    except FileNotFoundError:
        log.error(f'File not found: {filename}')
        log.input('press any key to exit...')
        sys.exit(-522)
    except Exception as e:
        log.error(f'An error occurred while reading tokens: {e}')
        log.input('press any key to exit...')
        sys.exit(-521)

    return lines


def writetoken(token, filename='good_tokens.txt'):
    #log.debug(f'Trying to write {token} to {filename}')
    with open(filename, 'a') as file:
        file.write(token + '\n')
        # log.debug(f'Wrote {token} to {filename}')

def writeinfo(info, filename='fulltokens.txt'):
    #log.debug(f'Trying to write {info} to {filename}')
    data_to_write = f'{info}\n\n===============================\n\n'
    with open(filename, 'a') as file:
        file.write(data_to_write)


def readproxy(filename):
        filename = filename.strip('\'"')
        if not os.path.isabs(filename):
            filename = os.path.abspath(filename)
            log.debug(f'Converted relative path to absolute path: {filename}')

        log.debug(f'Trying to read proxy from file: {filename}')
        proxy = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    proxy.append(line.strip())
            log.debug(f'Successfully read {len(proxy)} proxy.')
        except FileNotFoundError:
            log.error(f'File not found: {filename}')
            log.input('press any key to exit...')
            sys.exit(-522)
        except Exception as e:
            log.error(f'An error occurred while reading proxy: {e}')
            log.input('press any key to exit...')
            sys.exit(-521)

        return proxy