from helper.DirectLinkDL import DirectLinkDL as DDL
from helper.GdriveHelper import GdriveHelper as GDL
from utils import size_h

import os
import shutil
import subprocess
import time as t
import math

class TGFileHandler:
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

    def upload_media(client, message):
        print(message.text)
        if (len(message.command) == 1):
            message.reply('Give link or file path to Upload.', True)
            return
        elif message.command[1].startswith('http'):
            path = DDL.download(message)
        else:
            path = message.text[message.text.find(' ')+1 : ]

        size = os.path.getsize(path)
        file_name = os.path.basename(path)

        if (size > 2097152000):
            msg = message.reply('Splitting...', True)
            new_path = os.path.join(path, '/')
            if os.path.exists(new_path) is False:
                os.mkdir(new_path)
            os.system(f'rar -m0 a -v2097152000B \"{os.path.join(new_path, file_name)}\" \"{path}\"')
            files = sorted(os.listdir(new_path))
            for file in files:
                message.reply_document(os.path.join(new_path, file), True, caption=f'`{file}`', progress=TGFileHandler.progress, 
                                       progress_args=['Up', msg, t.time(), file], file_name=file)
            shutil.rmtree(new_path)
        else:
            msg = message.reply('Uploading...', True)
            message.reply_document(path, True, caption=f'`{file_name}`', progress=TGFileHandler.progress, 
                                   progress_args=['Up', msg, t.time(), file_name], file_name=file_name)
        msg.delete()

    def download_media(client, message, progress=progress):
        print(message.text)
        global file_path
        msg = message.reply('Downloading...', True)
        if len(message.command) > 1 and message.command[1].startswith('https://drive.google.com/'):
            file_path = GDL.download(message)
        elif len(message.command) > 1 and message.command[1].startswith('http'):
            file_path = DDL.download(message, msg)
        elif message.reply_to_message and message.reply_to_message.media:
            reply_msg = message.reply_to_message
            file_name = reply_msg.document.file_name if reply_msg.document is not None else reply_msg.video.file_name
            file_path = client.download_media(message.reply_to_message, progress=progress, progress_args=['Down', msg, t.time(), file_name])
        else:
            message.reply_text("Please tag a media message with the /download command.", True)
        
        if file_path == 'Downloaded Failed!':
            msg.edit_text('Downloaded Failed!')
        else:
            msg.edit_text("Downloaded successfully to: \n`{}`".format(file_path.replace('\\', '/')))
