import discord
from discord.ext import commands
from datetime import datetime
import socket

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Constants for socket communication
        self.header_length = 64
        self.encoding_format = 'utf-8'
        self.server_host = ''
        self.server_port = 00
        # Socket for communication with external server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        server_address = (self.server_host, self.server_port)
        self.connect_to_server(server_address)
        print(f'Connected to {server_address}')

    def send_message_to_server(self, message_data: tuple):
        # Join and encode the message, then get the length
        encoded_message = ' '.join(message_data).encode(self.encoding_format)
        
        # Send the message length and the encoded message
        self.client_socket.send(str(len(encoded_message)).encode(self.encoding_format.ljust(self.header_length)))
        self.client_socket.send(encoded_message)

    async def on_message(self, message: discord.Message):
        if self.user.mentioned_in(message):
            # Extract relevant user information and send to server
            truncated_user_name = self.get_truncated_user_name(message.author.name)
            message_data = (str(message.author.id), truncated_user_name, self.get_current_time())
            self.send_message_to_server(message_data)

    def connect_to_server(self, address: tuple):
        # Connect to the external server
        self.client_socket.connect(address)

    def get_truncated_user_name(self, name: str) -> str:
        # Truncate user name if it's longer than 7 characters
        return name[:7]

    def get_current_time(self) -> str:
        # Get the current time in HH:MM format
        return datetime.now().strftime("%H:%M")

bot = MyBot(command_prefix='!', intents=discord.Intents.default())
bot.run('TOKEN', bot=False)

