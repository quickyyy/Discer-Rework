import colorama
from colorama import Fore, Style
from datetime import datetime
import requests


def reroll_info_good(message, token, processed_tokens, result, goodtokens, badtokens, dupedtokens):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    checkedtokens = goodtokens + badtokens + dupedtokens
    total_info = f"Total: {Fore.GREEN}{goodtokens}{Style.RESET_ALL} {Fore.RED}{badtokens}{Style.RESET_ALL} {Fore.YELLOW}{dupedtokens}{Style.RESET_ALL} {Fore.BLACK}Total checked: {checkedtokens}{Style.RESET_ALL}"
    if result == 'good':
        print(f"{Fore.GREEN}[Good {timestamp}] {token} {Style.RESET_ALL} {message} {total_info}", end=" \r")
    elif result == 'bad':
        print(f"{Fore.RED}[Bad {timestamp}] {token}{Style.RESET_ALL} {message} {total_info}", end=" \r")
    elif token in processed_tokens:
        print(f"{Fore.YELLOW}[Duped {timestamp}] duped token - {token}{Style.RESET_ALL} {message} {total_info}", end=" \r")
# def actual_info():
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     total_info = f"Total: {Fore.GREEN}{goodtokens}{Style.RESET_ALL} {Fore.RED}{badtokens}{Style.RESET_ALL} {Fore.YELLOW}{dupedtokens}{Style.RESET_ALL}"
#     print(f"{Style.RESET_ALL} {total_info}", end="\r")
def getinfo(what, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.GREEN}[{timestamp} {what}]{Style.RESET_ALL} {message}")
def getwarning(what, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.YELLOW}[{timestamp} {what}]{Style.RESET_ALL} {message}")
def geterror(what, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.RED}[{timestamp} {what}]{Style.RESET_ALL} {message}")
def getchangelog(linkraw):
    #url = 'https://githubraw.com/quickyyy/DSM/main/changelog.txt'

    response = requests.get(linkraw)

    if response.status_code == 200:
        content = response.text
        lines = content.split('\n')
        
        for line in lines:
            getinfo(line)
def compare_versions(version1, version2):
    # Split the versions and convert each component to an integer
    vergh= "https://githubraw.com/quickyyy/Discer/main/version"
    lastver = getver(vergh)
    version1 = list(map(int, version1.split(".")))
    version2 = list(map(int, version2.split(".")))

    # Compare the versions
    if version1 > version2:
        return 1
    elif version1 < version2:
        return -1
    else:
        return 0
def getver(linkraw):
    response = requests.get(linkraw)
    if response.status_code == 200:
        lastver = response.text
        return lastver
    else:
        geterror("get error when getting version")



def coolinput(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    perem = f"{Fore.LIGHTMAGENTA_EX}[{timestamp} Input] {message}{Style.RESET_ALL}"
    return input(perem)