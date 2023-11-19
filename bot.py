import config
from helper.TGFileHandler import TGFileHandler

from time import time
import os
import subprocess
from pyrogram import Client, emoji, filters
# from pyrogram.types import BotCommand
import utils

api_id = config.api_id
api_hash = config.api_hash
bot_token = config.bot_token

app = Client("VersaT-bot", api_id, api_hash, bot_token=bot_token)

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
    TGFileHandler.upload_media(client, message)

@app.on_message(filters.command(['download', 'dl']))
def download_media_cmd(client, message):
    TGFileHandler.download_media(client, message)
      
@app.on_message(filters.command(['exec', 'e']))
def exec_cmd(client, message):
    utils.exec(client, message)

@app.on_message(filters.command(['forward', 'f']))
def forward(client, message):
    utils.forward(client, message)

# @app.on_message()
# def hello(client, message):
#     print(message.from_user.id, '-', message.from_user.first_name, ':', message.text)
#     print(message)
#     message.reply("Hi...I am Alive !!", True)
if not os.path.exists('./downloads'):
    os.mkdir('downloads')
print("Starting Bot...") 
app.run()  # Automatically start() and idle()
