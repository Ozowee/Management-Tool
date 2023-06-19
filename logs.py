from datetime import datetime
from colorama import Fore, Style, init
from discord_webhook import *
import json

with open("access.json",'r') as accessFile:
    jsonFile = json.load(accessFile)
    ErrorWebhookUrl = jsonFile['Keys']['ErrorWebhookUrl']

init(convert=True)
init(autoreset=True)

def log(content):
        print(f'[{datetime.now()}] {Fore.LIGHTMAGENTA_EX}{content}{Style.RESET_ALL}')
def log_info(content):
        print(f'[{datetime.now()}] {Fore.YELLOW}{content}{Style.RESET_ALL}')
def log_success(content):
        print(f'[{datetime.now()}] {Fore.LIGHTGREEN_EX}{content}{Style.RESET_ALL}')
def log_error(content):
        print(f'[{datetime.now()}] {Fore.LIGHTRED_EX}{content}{Style.RESET_ALL}')

        webhook = DiscordWebhook(url=ErrorWebhookUrl, username ="Error Monitor",avatar_url='https://i.imgur.com/RWFzrEi.png')
        embed = DiscordEmbed(title="Wykryto Error", color='0x50d68d')
        embed.add_embed_field(name='Error:', value=f"{content}",inline=True)
        embed.set_timestamp()
        webhook.add_embed(embed)
        webhook.execute()


