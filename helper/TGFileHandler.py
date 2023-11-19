import os
import subprocess
import time as t
import urllib.parse
import urllib.request
import gdown


class TGFileHandler:
    async def progress(current, total, *args):
        print(current, total)
        type = args[0]
        msg = args[1]
        message = args[2]
        if len(args) > 3:
            file_name = args[3]
        else:
            file_name = message.document.file_name if message.document is not None else message.video.file_name
        val = current * 15 // total
        txt = f"**{type}loading...**\n[{val*'▣'}{(15-val)*'▢'}] {current*100/total:.2f}%\n" + \
            f"**File Name :** `{file_name}`\n" + \
            f"**Progress :** {current/1024/1024:.2f} of {total/1024/1024:.2f} MB"
        if msg.text != txt:
            await msg.edit_text(txt)
            msg.text = txt
            if current == total:
                return
            t.sleep(5)

    def upload_media(client, message, progress=progress):
        print(message.text)
        if (len(message.command) == 1):
            message.reply('Give link or file path to Upload.', True)
            return
        path = message.command[1]
        file_name = os.path.basename(path)
        msg = message.reply('Uploading...', True)
        file = open(path, 'rb')
        size = os.path.getsize(path)
        if (size > 2147483648):
            if os.path.exists('./downloads/cache'):
                os.mkdir('./downloads/cache')
            new_path = os.path.join(os.path.dirname(path), 'cache')
            # msg.edit_text("File size is too large. Please upload a file smaller than 2GB.")
            subprocess.run(
                f"7z -mx0 a -v2047M {os.path.join(new_path, file_name)} {path}".split(" "))
            for file in os.listdir(new_path):
                print(file)
                message.reply_document(open(os.path.join(new_path, file), 'rb'),
                                       True, caption=f'`{file}`', progress=progress, progress_args=['Up', msg, message, file], file_name=file)
        else:
            message.reply_document(file, True, caption=file_name, progress=progress, progress_args=[
                                   'Up', msg, message, file_name])
        msg.delete()

    def download_media(client, message, progress=progress):
        print(message.text)

        if len(message.command) > 1 and message.command[1].startswith('https://drive.google.com'):
            url = message.command[1]
            msg = message.reply('Downloading...', True)
            file_name = gdown.download(url, quiet=True, resume=True, fuzzy=True)
            if file_name:
                if os.path.exists(f'./downloads/{file_name}'):
                    os.remove(f'./downloads/{file_name}')
                os.rename(file_name, f'./downloads/{file_name}')
                msg.edit_text(f"Downloaded successfully to: \n`downloads\{file_name}`")
            else:
                msg.edit_text("Downloaded Failed!")
        elif len(message.command) > 1 and message.command[1].startswith('http'):
            msg = message.reply('Downloading...', True)
            os.system(f'wget {message.command[1]} -P ./downloads')
            msg.edit_text(f"Downloaded successfully to: \n`{file_path[file_path.rfind('downloads'):]}`")
            # data = urllib.parse.urlparse(message.command[1])
            # # print(data)
            # urllib.request.urlretrieve(message.command[1], filename=f'downloads/{os.path.basename(data.path)}')
        elif message.reply_to_message and message.reply_to_message.media:
            msg = message.reply('Downloading...', True)
            # print(message)
            # print(message.reply_to_message)
            # print('\n-------------------------------------------------------\n')
            # print(message.document)
            # print(message.video)
            file_path = client.download_media(message.reply_to_message, progress=progress, progress_args=['Down', msg, message.reply_to_message])
            msg.edit_text(f"Downloaded successfully to: \n`{file_path[file_path.rfind('downloads'):]}`")
        else:
            message.reply_text("Please tag a media message with the /download command.", True)
