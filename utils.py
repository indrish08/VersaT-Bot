import os
import subprocess
from datetime import datetime
import time as t
from time import time, monotonic
from pyrogram import Client, emoji, filters

async def ping(_, message):
    print(message.text)
    start_time = time()
    reply = await message.reply('Pinging...',True)
    end_time = time()
    await reply.edit_text(f"Pong! \n{((end_time - start_time) * 1000):.2f} ms")

# old
# def ping(client, message):
#     print(message.text)
#     ping_time = (datetime.now() - message.date).total_seconds() * 1000 
#     message.reply(f"Pong! \n{ping_time:.2f} ms" , True)

def start(client, message):
    print(message.text)
    message.reply_text("Welcome to JackUser bot! You can use /help to see available commands.", True)

def help(client, message):
    print(message.text)
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
    message.reply(help_text, True)

def list_directory(client, message):
    print(message.text)
    path = os.getcwd()
    if(len(message.command) > 1):
        path += f'/{message.command[1]}'
    files = f'Current Folder : `{os.path.basename(path)}`\n\n'
    for i in os.listdir(path):
        if(os.path.isdir(i)):
            files += f'📁 `{i}`\n'
    for i in os.listdir(path):
        if(not os.path.isdir(i)):
            files += f'`{i}`\n'
    message.reply(files, True)
    # print(files)

def upload_media(client, message):
    print(message.text)
    path = message.command[1]
    message.reply_document(open(path, 'rb'), True, file_name = path[path.rfind('/')+1:])

async def download_media(client, message):
    print(message.text)
    while message.reply_to_message and message.reply_to_message.media:
        print(message)
        print('\n-------------------------------------------------------\n')
        message = message.reply_to_message
        print(message)
        print(message.reply_to_message)
        # print(message.document)
        # print(message.video)
        msg = await message.reply('Downloading...', True)
        async def progress(current, total):
            val = current * 50 // total
            txt = f"Downloading...\n[{val*':'}{(50-val)*'.'}] {current*100/total:.2f}%\nFile Name : {message.document.file_name}\nSize : {message.document.file_size/1024/1024:.2f} MB"
            if(msg.text != txt):
                await msg.edit_text(txt)
                msg.text = txt
                t.sleep(5)
        file_path = await client.download_media(message, progress=progress)
        await msg.edit_text(f"Downloaded successfully to: \n`{file_path[file_path.rfind('down'):]}`")
    # else:
        # await message.reply_text("Please tag a media message with the /download command.", True)
    await message.reply_text("Download Completed.", True)
      
def exec(client, message):
    print(message.text)
    if(len(message.command) < 2):
        message.reply('No commands to execute.', True)
        return
    # print(message.command)
    try:
        output = subprocess.run(message.command[1:],shell=False, capture_output=True).stdout.decode()
    except Exception as e:
        message.reply(f'{e} \'{message.command[1]}\'',True)
        return
    else:
        if len(output) == 0:
            message.reply("No Output", True)
        elif(len(output) > 4095):
            with open('output.txt', 'w') as f:
                f.write(output)
            # message.reply("Output is too long.", True)
            message.reply_document(open('output.txt', 'rb'), True)
        else:
            message.reply(output, True)
        