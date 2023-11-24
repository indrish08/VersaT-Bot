import os
import subprocess
import time as t

from pyrogram import Client, emoji, filters

async def ping(_, message):
    print(message.text)
    start_time = t.time()
    reply = await message.reply('Pinging...',True)
    end_time = t.time()
    await reply.edit_text(f"Pong! \n{((end_time - start_time) * 1000):.2f} ms")

def start(client, message):
    print(message.text)
    message.reply_text("Welcome to VersaT bot! You can use /help to see available commands.", True)

def help(client, message):
    print(message.text)
    help_text = \
            "Here are the available commands:\n" + \
            "- /start - Start using the bot.\n" + \
            "- /help - Display this help message.\n" + \
            "- /ls - List directory.\n" + \
            "- /download - or /dl to download files.\n" + \
            "- /upload - or /up to upload files.\n" + \
            "- /exec - or /e to execute shell commands.\n" + \
            "- /ping - Check ping."
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

def forward(client, message):
    print(message.text)
    target_chat = 'tg_premium_today'
    if message.reply_to_message:
        str = message.reply_to_message.text
    else:
        str = message.text[message.text.find(' ')+1 : ]
    arr = str.split('\n')
    links = []
    for i in arr:
        if(i.startswith('http')):
            links.append(i)
    chat_ids = []
    msg_ids = []
    for i in links:
        index = i.rfind('/')
        msg_ids.append(int(i[index+1 : ]))
        chat_ids.append(i[i.rfind('/',0,index)+1 : index])
    for i in range(len(msg_ids)):
        client.forward_messages(target_chat, chat_ids[i], msg_ids[i], True)
    
def size_h(size, decimal_point=2):
    for x in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f'{size:.2f} {x}'
        size /= 1024.0
    return f"{size:.{decimal_point}f}{x}"