import requests, os
import os
import sys
import configparser
from colorama import Fore, Style
import requests
import emoji
import time
goodtokens = 0
badtokens = 0
valid_tokens = []
def great_message(message):
    print(emoji.emojize(f"{message}"))
def write_valid_tokens(filename, tokens):
    with open(filename, 'w', encoding="utf-8") as outfile:
        for token in tokens:
            outfile.write(token + '\n')
def write_runtime_token(filename,token):
    with open(filename, 'a', encoding="utf-8") as outfile:
        outfile.write(token + '\n')
def full_logsfile(filename, username, email, phone, verified, nitro, friends_list, token):
    nameinmes = emoji.emojize(f":memo:Username - {username}")
    if verified == True:
        verif = emoji.emojize(" :check_mark_button: Profile is verified!")
    else:
        verif = emoji.emojize(" :cross_mark: It seems like the account is auto-reg")
    if nitro in [1, 2, 3]:
        nitroinf = emoji.emojize(' :rocket: Account has nitro!')
    else:
        nitroinf = emoji.emojize(' :rock: Does not have an active nitro sub')
    mes = emoji.emojize(f" :clipboard: token - {token}\n :closed_mailbox_with_raised_flag:email - {email}\n :mobile_phone:phone - {phone}\n :people_hugging:friends - {friends_list}\n\n\n")
    log = f"{nameinmes}\n{nitroinf}\n{verif}\n{mes}\n"  # Convert the log tuple to a string
    with open(filename, 'a', encoding="utf-8") as outfile:
        outfile.write(log)


def check_token(token):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        "Authorization": token
    }
    global goodtokens
    global badtokens
    global valid_tokens
    username = "N/A"
    email = "N/A"
    phone = "N/A"
    verified = False
    nitro = 0
    friends_list = []
    token_response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    if token_response.status_code == 200:
        print(f"{Fore.GREEN}--------------------------------------------------------------------------------")
        print(emoji.emojize(f":check_mark_button: Valid - {token}{Style.RESET_ALL}"))
        great_message(":clipboard: Getting info about token..")
        req = requests.get("https://discord.com/api/v9/users/@me",headers=headers)
        username = req.json()['username']
        email = req.json()['email']
        phone = req.json()['phone']
        verified = req.json()['verified']
        great_message(f":memo:Username - {username}")
        if verified == True:
            great_message(" :check_mark_button: Profile is verified!")
        else:
            great_message(" :cross_mark: It seems like account auto-reg")
        nitro = req.json()['premium_type']
        if nitro in [1 , 2 , 3]:
            great_message(' :rocket: Account have nitro!')
        else:
            great_message(' :rock: Dont have active nitro sub')
        friends = requests.get('https://discord.com/api/v8/users/@me/relationships', headers=headers)
        for i in friends.json():
            friends_list.append(i, ' - ', ['username'])
        valid_tokens.append(token)
        great_message(f" :closed_mailbox_with_raised_flag:email - {email}\n :mobile_phone:phone - {phone}\n :people_hugging:friends - {friends_list}")
        goodtokens += 1
        write_runtime_token('valid_tokens.txt', token)
        #print("--------------------------------------------------------------------------------")
    else:
        print(f"{Fore.RED}--------------------------------------------------------------------------------")
        great_message(f":cross_mark:An error occurred or the Discord token is not valid: {token}")
        badtokens += 1
        print(f"--------------------------------------------------------------------------------{Style.RESET_ALL}")
    full_logsfile('full_logsfile.txt', username, email, phone, verified, nitro, friends_list, token)
    return username, email, phone, token, nitro, verified
def main():
    os.system("cls")
    print("Welcome to the Discer! Discord token checker\n Dev - https://zelenka.guru/quka/ | My Telegram blog - https://t.me/bredcookie")
    token_file = input("Please, enter a directory with tokens.txt (If not specified, the script directory will be checked): ")
    if token_file == '':
        token_file = os.getcwd() + "/tokens.txt"
    with open(token_file, 'r', encoding="utf-8") as infile:
        lines = infile.readlines()
        for line in lines:
            line = line.replace(u'\ufeff', '').encode('latin-1')
            token = line.strip().decode('utf-8')
            check_token(token)
    write_valid_tokens('valid_tokens.txt', valid_tokens)
    
    if badtokens > goodtokens:
        great_message(f":bar_chart:All work is done! Stat for this check: {Fore.GREEN}:chart_decreasing: Good tokens - {goodtokens}{Style.RESET_ALL} | {Fore.RED}:chart_increasing: Bad tokens - {badtokens}{Style.RESET_ALL} | :input_numbers: Amount of tokens : {goodtokens+badtokens}")
    else:
        great_message(f":bar_chart:All work is done! Stat for this check: {Fore.GREEN}:chart_increasing: Good tokens - {goodtokens}{Style.RESET_ALL} | {Fore.RED}:chart_decreasing: Bad tokens - {badtokens}{Style.RESET_ALL} | :input_numbers: Amount of tokens : {goodtokens+badtokens}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Get ctrl+c!")
        if badtokens > goodtokens:
            great_message(f":bar_chart:All work is done! Stats for this check: {Fore.GREEN}:chart_decreasing: Good tokens - {goodtokens}{Style.RESET_ALL} | {Fore.RED}:chart_increasing: Bad tokens - {badtokens}{Style.RESET_ALL} | :input_numbers: Amount of tokens : {goodtokens+badtokens}")
        else:
            great_message(f":bar_chart:All work is done! Stats for this check: {Fore.GREEN}:chart_increasing: Good tokens - {goodtokens}{Style.RESET_ALL} | {Fore.RED}:chart_decreasing: Bad tokens - {badtokens}{Style.RESET_ALL} | :input_numbers: Amount of tokens : {goodtokens+badtokens}")
        time.sleep(6)
        sys.exit()
