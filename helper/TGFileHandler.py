import helper.DirectLinkDL as DDL
import helper.GdriveHelper as GDL
import helper.RcloneHandler as RC
from config import split_size
from utils import size_h

import os
import shutil
import subprocess
import time as t
import math

async def progress(current, total, type, msg, start, file_name):
    now = t.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        val = current * 15 // total
        txt = \
            f"**{type}loading...**\n" + \
            f"**File Name :** `{file_name}`\n" + \
            f"[{val*'▣'}{(15-val)*'▢'}] {current*100/total:.2f}%\n" + \
            f"**Progress :** {size_h(current)} of {size_h(total)}"
        await msg.edit_text(txt)

def upload_media(path, message, reply_to = None):
    size = os.path.getsize(path)
    file_name = os.path.basename(path)
    reply_to = message.id if reply_to == None else reply_to

    if (size > split_size):
        msg = message.reply(f'Splitting...\n{file_name}', True)
        new_path = f'{path}_rar/'
        if os.path.exists(new_path) is False:
            os.mkdir(new_path)
        os.system(f'rar -m0 a -v{split_size}B \"{os.path.join(new_path, file_name)}\" \"{path}\"')
        msg.delete()
        files = sorted(os.listdir(new_path))
        for file in files:
            msg = message.reply('Uploading...', True)
            reply = message.reply_document(os.path.join(new_path, file), caption=f'`{file}`', progress=progress, 
                                    progress_args=['Up', msg, t.time(), file], file_name=file, reply_to_message_id=reply_to)
            reply_to = reply.id
            msg.delete()
        shutil.rmtree(new_path)
    else:
        msg = message.reply('Uploading...', True)
        # if file_name.endswith('.mkv', '.mp4', '.webm', '.m4v'):
        #     reply = message.reply_video(path, caption=f'`{file_name}`', supports_streaming=True, reply_to_message_id=reply_to, 
        #                                 progress=progress, progress_args=['Up', msg, t.time(), file_name])
        # else:
        reply = message.reply_document(path, caption=f'`{file_name}`', progress=progress, 
                                    progress_args=['Up', msg, t.time(), file_name], file_name=file_name, reply_to_message_id=reply_to)
        msg.delete()
    return reply

def upload_folder(path, message, reply_to = None):
    reply_to = message.id if reply_to == None else reply_to
    reply = message.reply(f"**{os.path.basename(path)}**", reply_to_message_id=reply_to)
    reply_f = reply
    cur_dir = sorted(os.listdir(path))
    for folder in cur_dir:
        folder = os.path.join(path,folder)
        if(os.path.isdir(folder)):
            upload_folder(folder, message, reply.id)
    for file in cur_dir:
        file = os.path.join(path,file)
        if(os.path.isfile(file)):
            reply = upload_media(file, message, reply.id)
            t.sleep(1)
    # message.reply(f"**{'*'*11}**", reply_to_message_id=reply_f.id)

def upload(client, message):
    print(message.text)
    if (len(message.command) == 1):
        message.reply('Give link or file path to Upload.', True)
        return
    if message.command[1].startswith('http'):
        path = download_media(client, message)
    else:
        path = message.text[message.text.find(' ')+1 : ]

    if os.path.isdir(path):
        upload_folder(path, message)
    else:
        upload_media(path, message)
    message.reply(f"**Upload Completed : {os.path.basename(path)}**")

def download_media(client, message, progress=progress):
    print(message.text)
    global file_path
    msg = message.reply('Downloading...', True)
    if len(message.command) == 1:
        if message.reply_to_message and message.reply_to_message.media:
            reply_msg = message.reply_to_message
            file_name = reply_msg.document.file_name if reply_msg.document is not None else reply_msg.video.file_name
            file_path = client.download_media(message.reply_to_message, progress=progress, progress_args=['Down', msg, t.time(), file_name])
        else:
            message.reply_text("Please tag a media message with the /download command.", True)
        return
    if message.command[1].startswith('https://alchemist.cyou/'):
        file_path = RC.download(message)
    elif message.command[1].startswith('https://drive.google.com/'):
        file_path = GDL.download(message.command[1])
    elif message.command[1].startswith('http'):
        file_path = DDL.download(message)
    
    msg.delete()
    if file_path is None:
        message.reply_text('Downloaded Failed!',True)
    else:
        message.reply_text("Downloaded successfully to: \n`{}`".format(file_path.replace('\\', '/')), True)
    return file_path


def TG_link_dl(client, message):
    print(message.text)
    if message.reply_to_message:
        str = message.reply_to_message.text
    else:
        str = message.text[message.text.find(' ')+1 : ]
    index = str.rfind('/')
    msg_id = (int(str[index+1 : ]))
    chat_id = (str[str.rfind('/',0,index)+1 : index])
    video = client.get_messages(chat_id,msg_id)
    file_name = video.document.file_name if video.document is not None else video.video.file_name
    msg = message.reply('Downloading...', True)
    file_path = client.download_media(video, progress=progress, progress_args=['Down', msg, t.time(), file_name])
    msg.delete()
    if file_path is None:
        message.reply_text('Downloaded Failed!',True)
    else:
        message.reply_text("Downloaded successfully to: \n`{}`".format(file_path.replace('\\', '/')), True)