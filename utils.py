import os
import subprocess
from datetime import datetime
import time as t
from time import time, monotonic
from pyrogram import Client, emoji, filters
import urllib.parse 
import urllib.request

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
    message.reply_text("Welcome to VersaT bot! You can use /help to see available commands.", True)

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
    file_name = path[path.rfind('/')+1:]
    msg = message.reply('Uploading...', True)
    async def progress(current, total):
        # print(current,total)
        val = current * 30 // total
        txt = f'''Uploading...\n[{val*'='}{(30-val)*'.'}] {current*100/total:.2f}%
        File Name : {file_name}
        Progress : {current/1024/1024:.2f} of {total/1024/1024:.2f} MB'''
        if(msg.text != txt):
            await msg.edit_text(txt)
            msg.text = txt
        t.sleep(8)
    file = open(path, 'rb')
    size = (os.path.getsize(path))
    if(size > 2147483648):
        msg.edit_text("File size is too large. Please upload a file smaller than 2GB.")
        subprocess.run(f"7z -mx0 a -v2047M {path[:path.rfind('/')]}/cache/{file_name} {path}".split(" "))
        for f in os.listdir(f"{path[:path.rfind('/')]}/cache"):
            # print(f)
            message.reply_document(open(f"{path[:path.rfind('/')]}/cache/{f}", 'rb'), True, progress=progress, file_name = f)
    else:
        message.reply_document(file, True, progress=progress, file_name = file_name)
    msg.delete()

async def download_media(client, message):
    print(message.text)
    async def progress(current, total):
        print(current,total)
        val = current * 30 // total
        txt = f'''Downloading...\n[{val*'█'}{(30-val)*'▒'}] {current*100/total:.2f}%
        File Name : {message.document.file_name if message.document is not None else message.video.file_name}
        Progress : {current/1024/1024:.2f} of {total/1024/1024:.2f} MB'''
        if(msg.text != txt):
            await msg.edit_text(txt)
            msg.text = txt
        t.sleep(5)
    msg = await message.reply('Downloading...', True)
    while message.reply_to_message and message.reply_to_message.media:
        print(message)
        print(message.reply_to_message)
        print('\n-------------------------------------------------------\n')
        message = message.reply_to_message
        print(message)
        # print(message.document)
        # print(message.video)
        file_path = await client.download_media(message, progress=progress)
        await msg.edit_text(f"Downloaded successfully to: \n`{file_path[file_path.rfind('down'):]}`")
    # else:
        # await message.reply_text("Please tag a media message with the /download command.", True)
    if(message.command[1].startswith('http')):
        data = urllib.parse.urlparse(message.command[1])
        # print(data)
        urllib.request.urlretrieve(message.command[1], filename=f'downloads/{os.path.basename(data.path)}')
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
    
def size_h(size):
    for x in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f'{size:.2f} {x}'
        size /= 1024.0