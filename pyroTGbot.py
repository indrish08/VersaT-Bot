import os
import subprocess
from pyrogram import Client, emoji, filters
# from pyrogram.types import BotCommand
from utils import start, download_media
from datetime import datetime

TARGET = 1118476751

api_id = '23275262'
api_hash = '13d854f2fa5a9ba3c03639fd67c522aa'
bot_token = '6533996464:AAF9JinShEREKWnwwZyD396fOmLnxmN-j0A'

app = Client("my_account", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# bot_commands = [
#     BotCommand(command="/start", description="Start the bot"),
#     BotCommand(command="/help", description="Show help information"),
#     # Add more commands as needed
# ]
# Set the bot's commands
# app.set_bot_commands(bot_commands)

@app.on_message(filters.command(["ping"]))
def ping(client, message):
    ping_time = (datetime.now() - message.date).total_seconds() * 1000 
    message.reply(f"Pong! \n{ping_time:.2f} ms" , True)

@app.on_message(filters.command(["start"]))
def start_command(client, message):
    start(client, message)
    # message.reply_text("Welcome to JackUser bot! You can use /help to see available commands.")

@app.on_message(filters.command(["help"]))
def help_command(client, message):
    help_text = """
    Here are the available commands:
    - /start - Start using the bot.
    - /help - Display this help message.
    - /ls - List directory.
    - /download - or /dl to download files.
    - /upload - or /up to upload files.
    - /exec - or /e to execute shell commands.
    - /ping - Check ping.
    """
    message.reply_text(help_text)

@app.on_message(filters.command(["ls"]))
def list_directory(client, message):
    # print(message)
    path = os.getcwd()
    if(len(message.command) > 1):
        path += f'\\{message.command[1]}'
    files = f'Current Folder : `{os.path.basename(path)}`\n\n'
    for i in os.listdir(path):
        if(os.path.isdir(i)):
            files += f'📁 `{i}`\n'
    for i in os.listdir(path):
        if(not os.path.isdir(i)):
            files += f'`{i}`\n'
    message.reply(files, True)

@app.on_message(filters.command(["upload", "up"]))
def upload_media(client, message):
    path = message.text[4:]
    message.reply_document(open(path, 'rb'), True)

@app.on_message(filters.command(["download", "dl"]))
def download_media_cmd(client, message):
    download_media(client, message)
      
@app.on_message(filters.command(['exec', 'e']))
def tes(client, message):
    if(len(message.command) < 2):
        message.reply('No commands to execute.', True)
        return
    print(message.command)
    output = subprocess.run(message.command[1:],shell=True, capture_output=True).stdout.decode()
    # print(output)
    if(len(output) > 4095):
        with open('output.txt', 'w') as f:
            f.write(output)
        # message.reply("Output is too long.", True)
        message.reply_document(open('output.txt', 'rb'), True)
    else:
        message.reply(output, True)
    print(message.text)

@app.on_message()
def hello(client, message):
    message.reply("Hi", True)
    # print(message)

app.run()  # Automatically start() and idle()
