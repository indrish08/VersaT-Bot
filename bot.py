import os
import subprocess
from pyrogram import Client, emoji, filters
# from pyrogram.types import BotCommand
import utils

TARGET = 1118476751

api_id = '23275262'
api_hash = '13d854f2fa5a9ba3c03639fd67c522aa'
bot_token = '6533996464:AAF9JinShEREKWnwwZyD396fOmLnxmN-j0A'

app = Client("my_account", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command(['ping', 'p']))
async def ping_cmd(client, message):
    await utils.ping(client, message)

@app.on_message(filters.command(['start']))
def start_cmd(client, message):
    utils.start(client, message)

@app.on_message(filters.command(['help']))
def help_cmd(client, message):
    utils.help(client, message)

@app.on_message(filters.command(['ls']))
def list_directory_cmd(client, message):
    utils.list_directory(client, message)

@app.on_message(filters.command(['upload', 'up']))
def upload_media_cmd(client, message):
    utils.upload_media(client, message)

@app.on_message(filters.command(['download', 'dl']))
async def download_media_cmd(client, message):
    await utils.download_media(client, message)
      
@app.on_message(filters.command(['exec', 'e']))
def exec_cmd(client, message):
    utils.exec(client, message)

@app.on_message()
def hello(client, message):
    print(message.from_user.id, '-', message.from_user.first_name, ':', message.text)
    print(message)
    message.reply("Hi...I am Alive !!", True)

print("Starting Bot...") 
app.run()  # Automatically start() and idle()

# class message:
#     def __init__(self) -> None:
#         self.command = [""]

# if(input()=='ls'):
#     utils.list_directory(Client, message())