# MUST BE RUNNED IN DISCORD.PY VERSION 1.7.3
import discord 
from discord.ext import commands
from datetime import datetime
import socket

HEADER = 64
FORMAT = 'utf-8'
DIS_MSG = '!DIS'
# Put esp32 ip here 
HOST = '192.168.29.159'
PORT = 80

intents = discord.Intents.default()

bot = commands.Bot('!',intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (HOST,PORT)
    client.connect(addr)
    print(f'Connected to {addr}')

def send(mesg : tuple):
    msg = ' '.join(mesg)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_len = str(msg_length).encode(FORMAT)
    send_len += b' '*(HEADER-len(send_len))
    client.send(send_len)
    client.send(message)

@bot.event
async def on_message(message: discord.Message):
    if bot.user.mentioned_in(message):
        name = message.author.name
        if len(name) > 7:
            name = message.author.name[:7]
        msg = (str(message.author.id),name,datetime.now().strftime("%H:%M"))
        send(msg)

bot.run('TOKEN',bot=False)