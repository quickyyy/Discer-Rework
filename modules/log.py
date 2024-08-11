import logging
from datetime import datetime
from colorama import init, Fore, Style
from configparser import ConfigParser

init(autoreset=True)
printdebug = False
try:
    cfg = ConfigParser()
    cfg.read('discer.q3')
    if cfg.getboolean('Main', 'printdebuglines'):
        printdebug = True
except:
    pass


class Logger:
    LEVEL_COLORS = {
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'DBG': Fore.CYAN,
        'INPUT': Fore.MAGENTA
    }

    def __init__(self, name='Logger'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def log(self, level, message):
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        color = self.LEVEL_COLORS.get(level, Fore.WHITE)
        log_message = f"[{now.split()[0]}] [{now.split()[1]}] [{level}] {message}"
        colored_message = f"{color}{log_message}{Style.RESET_ALL}"
        self.logger.debug(colored_message)

    def info(self, message):
        self.log('INFO', message)

    def warning(self, message):
        self.log('WARNING', message)

    def error(self, message):
        self.log('ERROR', message)

    def debug(self, message):
        if printdebug:
            self.log('DBG', message)
        else:
            pass

    def input(self, prompt):
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        color = self.LEVEL_COLORS.get('INPUT', Fore.WHITE)
        log_message = f"[{now.split()[0]}] [{now.split()[1]}] [INPUT] {prompt}"
        colored_message = f"{color}{log_message}{Style.RESET_ALL}"
        print(colored_message, end='')
        return input('')


log = Logger()


def printlogo():
    print(f'''
    ______________________________________________________
    $$$$$$$..|$$/..._______..._______...______....______..
    $$.|..$$.|/..|./.......|./.......|./......\../......\.
    $$.|..$$.|$$.|/$$$$$$$/./$$$$$$$/./$$$$$$..|/$$$$$$..|
    $$.|..$$.|$$.|$$......\.$$.|......$$....$$.|$$.|..$$/.
    $$.|__$$.|$$.|.$$$$$$..|$$.\_____.$$$$$$$$/.$$.|......
    $$....$$/.$$.|/.....$$/.$$.......|$$.......|$$.|......
    $$$$$$$/..$$/.$$$$$$$/...$$$$$$$/..$$$$$$$/.$$/....... Rework :D
    ______________________________________________________
    You can find me in telegram - @bredcookie
    ______________________________________________________
    ''')
