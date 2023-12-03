import config
import helper.TGFileHandler as TGFileHandler
import helper.RcloneHandler as RC

from time import time
import os
import subprocess
from pyrogram import Client, idle, emoji, filters
from pyrogram.types import BotCommand
import utils

api_id = config.api_id
api_hash = config.api_hash
bot_token = config.bot_token
ids = [1118476751, -1001956807784] # [5502597376]
bot_commands = [
    BotCommand('start','Check bot alive status.'),
    BotCommand('help', 'Get available commands.'),
    BotCommand('ls', 'Get list of available files and folders.'),
    BotCommand('download', 'or /dl to download files.'),
    BotCommand('upload', 'or /up to upload files.'),
    BotCommand('exec', 'or /e to execute shell commands.'),
    BotCommand('speedtest', 'or /st to check internet speed.'),
    BotCommand('ping', 'Check ping.')
]

app = Client("VersaT-bot", api_id, api_hash, bot_token=bot_token)

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
    TGFileHandler.upload(client, message)

@app.on_message(filters.command(['download', 'dl']))
def download_media_cmd(client, message):
    TGFileHandler.download_media(client, message)
      
@app.on_message(filters.command(['rclone', 'rc']))
def rclone_copy_cmd(client, message):
    RC.copy(message)
      
@app.on_message(filters.command(['exec', 'e']))
def exec_cmd(client, message):
    utils.exec(client, message)

@app.on_message(filters.command(['speedtest', 'st']))
def speedtest_cmd(client, message):
    utils.speedtest(client, message)

@app.on_message(filters.command(['systeminfo']))
def system_info_cmd(client, message):
    utils.system_info(client, message)

@app.on_message(filters.command(['forward', 'f']))
def forward(client, message):
    utils.forward(client, message)

@app.on_message(filters.command(['ping', 'p']))
async def ping_cmd(client, message):
    await utils.ping(client, message)

@app.on_message(filters.command(['restart', 'r']))
async def restart(_,__):
    print("Restarting Bot...") 
    await app.stop()
    await app.start()
    print("Restarting Bot...") 
    await utils.sendMessage(app, ids, 'Restart')
    # await app.set_bot_commands(bot_commands)
    await idle()

# @app.on_message()
# def hello(client, message):
#     print(message.from_user.id, '-', message.from_user.first_name, ':', message.text)
#     print(message)
#     message.reply("Hi...I am Alive !!", True)

if not os.path.exists('./downloads'):
    os.mkdir('downloads')

async def main():
    await app.start()
    print("Starting Bot...") 
    await utils.sendMessage(app, ids, 'Start')
    # await app.set_bot_commands(bot_commands)
    await idle()
    
app.run(main())
