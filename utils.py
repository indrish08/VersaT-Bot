import os
import subprocess
from pyrogram import Client, emoji, filters

def start(client, message):
    message.reply_text("Welcome to JackUser bot! You can use /help to see available commands.")

def help(client, message):
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

def upload_media(client, message):
    path = message.text[4:]
    message.reply_document(open(path, 'rb'), True)

def download_media(client, message):
    if message.reply_to_message and message.reply_to_message.media:
        msg = message.reply('Downloading...')
        def progress(current, total):
            val = current * 50 // total
            txt = f"Downloading...\n[{val*':'}{(50-val)*'.'}] {current*100/total:.2f}%"
            if(msg.text != txt):
                msg.edit_text(txt)
                msg.text = txt
        file_path = client.download_media(message.reply_to_message, progress=progress)
        msg.edit_text(f"Downloaded successfully to: \n`{file_path[file_path.rfind('down'):]}`")
    else:
        message.reply_text("Please tag a media message with the /download command.")
      
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
