import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix = '.', intents=intents)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(f'{bot.user} is connected to: {guild.name}')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Ni Hao {member.name}! Welcome to 100h community.')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command()
async def poll(ctx, *, message):
    emb = discord.Embed(title="POLL", description=message)
    print("Nice")
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction('✔️')
    await msg.add_reaction('❌')

bot.run(TOKEN)
