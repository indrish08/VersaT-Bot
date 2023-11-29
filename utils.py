import os
import subprocess
import time as t
from speedtest import Speedtest

async def ping(client, message):
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
            "- /start - Check bot alive status.\n" + \
            "- /help - Get available commands.\n" + \
            "- /ls - List directory.\n" + \
            "- /download - or /dl to download files.\n" + \
            "- /upload - or /up to upload files.\n" + \
            "- /exec - or /e to execute shell commands.\n" + \
            "- /speedtest - or /st to check internet speed.\n" + \
            "- /ping - Check ping."
    message.reply(help_text, True)

def list_directory(client, message):
    print(message.text)
    path = os.getcwd()
    if(len(message.command) > 1):
        path += f'/{message.command[1]}'
    files = f'Current Folder : `{os.path.basename(path)}`\n'
    list_dir = sorted(os.listdir(path))
    for i in list_dir:
        path_i = os.path.join(path,i)
        if(os.path.isdir(path_i)):
            files += f'\n📁 `{i}`'
    for i in list_dir:
        path_i = os.path.join(path,i)
        if(os.path.isdir(path_i) is False):
            size = size_h(os.path.getsize(path_i))
            files += f'\n`{i}` [{size}]'
    message.reply(files, True)

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

def speedtest(_, message):
    print(message.text)
    msg = message.reply('Speed Test Started...',True)
    st = Speedtest()
    st.get_best_server()
    st.download()
    st.upload()
    st.results.share()
    res = st.results.dict()
    text = \
        f'Internet Speed...\n' + \
        f'Download : {size_h(res["download"]/8)} / s\n' + \
        f'Upload : {size_h(res["upload"]/8)} / s'
    message.reply_photo(res['share'], True, text)
    message.reply_text(res)
    msg.delete()

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
            return f'{size:.{decimal_point}f}{x}'
        size /= 1024.0
    return f"{size:.{decimal_point}f}{x}"

async def sendStartMessage(app, ids):
    for id in ids:
        await app.send_message(id,'Bot Started!')