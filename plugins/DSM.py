import requests
import os
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)
from main import getinfo, getwarning, geterror
def headers(token):
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        "Authorization": token
    }
def get_private_channels(token):
    url = 'https://discord.com/api/v9/users/@me/channels'
    response = requests.get(url, headers=headers(token))
    if response.status_code == 200:
        return response.json()
    else:
        return None
def send_message_to_private_channels(token, message):
    channels = get_private_channels(token)
    
    if channels is None:
        geterror("DSM","Failed to get private channels. Please make sure your token is valid.")
        return
    
    if not channels:
        getwarning("DSM","No private channels found.")
        return

    getinfo("Sending message to private channels:")
    for channel in channels:
        channel_id = channel['id']
        recipient_name = channel['recipients'][0]['username']
        getinfo(f" - {channel_id} ({recipient_name})")
        payload = {
            'content': message
        }
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
        response = requests.post(url, headers=headers(token), json=payload)
        if response.status_code == 200:
            getinfo("DSM",f"Successfully send message with token {token}")
        elif response.status_code == 401:
            geterror("DSM",f"Invalid account with token {token}")
        elif response.status_code == 403:
            getwarning("DSM",f"Locked account with token {token}")
        elif response.status_code == 429:
            getwarning("DSM",f"Ratelimited with token {token}")
        else:
            geterror("DSM",f"Faled to send message. Please, try again later. Error code: {response.status_code}")