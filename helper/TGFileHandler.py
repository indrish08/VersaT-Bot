from helper.DirectLinkDL import DirectLinkDL as DDL
from helper.GdriveHelper import GdriveHelper as GDL

import os
import subprocess
import time as t
import math


class TGFileHandler:
    async def progress(current, total, *args):
        # print(current, total, math.ceil(t.time()))
        start = args[2]
        now = t.time()
        diff = now - start
        if round(diff % 10.00) == 0 or current == total:
            type = args[0]
            msg = args[1]
            file_name = args[3]
            val = current * 15 // total
            txt = f"**{type}loading...**\n[{val*'▣'}{(15-val)*'▢'}] {current*100/total:.2f}%\n" + \
                f"**File Name :** `{file_name}`\n" + \
                f"**Progress :** {current/1024/1024:.2f} of {total/1024/1024:.2f} MB"
            await msg.edit_text(txt)

    def upload_media(client, message, progress=progress):
        print(message.text)
        if (len(message.command) == 1):
            message.reply('Give link or file path to Upload.', True)
            return
        if message.command[1].startswith('http'):
            path = DDL.download(message)
        else:
            path = message.text[message.text.find(' ')+1 : ]
        file_name = os.path.basename(path)
        file = open(path, 'rb')
        size = os.path.getsize(path)
        if (size > 2097152000):
            msg = message.reply('Splitting...', True)
            new_path = os.path.join(os.path.dirname(path), 'cache')
            if os.path.exists(new_path) is False:
                os.mkdir(new_path)
            os.system(f'rar -m0 a -v2097152000B \"{os.path.join(new_path, file_name)}\" \"{path}\"')
            files = sorted(os.listdir(new_path))
            for file in files:
                message.reply_document(open(os.path.join(new_path, file), 'rb'),
                                       True, caption=f'`{file}`', progress=progress, progress_args=['Up', msg, t.time(), file], file_name=file)
        else:
            msg = message.reply('Uploading...', True)
            message.reply_document(file, True, caption=f'`{file_name}`', progress=progress, progress_args=[
                                   'Up', msg, t.time(), file_name])
        msg.delete()

    def download_media(client, message, progress=progress):
        print(message.text)
        if len(message.command) > 1 and message.command[1].startswith('https://drive.google.com'):
            GDL.download(message)
        elif len(message.command) > 1 and message.command[1].startswith('http'):
            DDL.download(message)
        elif message.reply_to_message and message.reply_to_message.media:
            msg = message.reply('Downloading...', True)
            print(message)
            # print(message.reply_to_message)
            # print('\n-------------------------------------------------------\n')
            # print(message.document)
            # print(message.video)
            file_name = message.reply_to_message.document.file_name if message.reply_to_message.document is not None else message.reply_to_message.video.file_name
            file_path = client.download_media(message.reply_to_message, progress=progress, progress_args=['Down', msg, t.time(), file_name])
            msg.edit_text(f"Downloaded successfully to: \n`{file_path[file_path.rfind('downloads'):]}`")
        else:
            message.reply_text("Please tag a media message with the /download command.", True)
