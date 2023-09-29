import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents = intents) # this client will represent our 100h bot

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    
    print(f'{client.user} is connected to: {guild.name}')



client.run(TOKEN)