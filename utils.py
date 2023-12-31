import os
import subprocess
import time as t
from psutil import disk_usage, virtual_memory, swap_memory, cpu_percent, cpu_count, boot_time, net_io_counters
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
    msg.delete()

def system_info(client, message):
    total, used, free, disk_usage_percentage = disk_usage(os.getcwd())
    swap = swap_memory()
    memory = virtual_memory()
    uptime = t.time() - boot_time()
    text = (
        f"Total Disk Space: {size_h(total)}\n"
        f"Used : {size_h(used)} | Free : {size_h(free)}\n\n"
        f"Resourse Usage :\n"
        f"CPU : {cpu_percent(interval=0.5)}% | RAM : {memory.percent}% | Disk : {disk_usage_percentage}%\n\n"
        f"CPU Cores Count: \n"
        f"Physical : {cpu_count(logical=False)} | Total : {cpu_count()}\n\n"
        f"Total RAM : {size_h(memory.total)}\n"
        f"Used : {size_h(memory.used)} | Free : {size_h(memory.available)}\n"
        f"Swap Memory : {size_h(swap.total)} | Used : {swap.percent}%\n\n"
        f"Network :\n"
        f"Upload : {size_h(net_io_counters().bytes_sent)} | Download : {size_h(net_io_counters().bytes_recv)}\n\n"
        f"OS Uptime : {time_h(uptime)}"
    )
    message.reply(text,True)


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
    for x in ['B', 'KiB', 'MiB', 'GiB', 'TiB']:
        if size < 1024.0:
            return f'{size:.{decimal_point}f}{x}'
        size /= 1024.0
    return f"{size:.{decimal_point}f}{x}"

def time_h(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    if hour:
        return "%dh %02dm %02ds" % (hour, minutes, seconds)
    elif minutes:
        return "%02dm %02ds" % (minutes, seconds)
    else:
        return "%02ds" % (seconds)

async def sendMessage(app, ids, event):
    for id in ids:
        await app.send_message(id,f'Bot {event}ed!')