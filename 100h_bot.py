import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import datetime

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

current_time = datetime.datetime.now()
duration = 15
end_time = current_time + datetime.timedelta(seconds=duration)

channel_id = '1156706476761550918'

bot = commands.Bot(command_prefix='.', intents=intents)

poll_closed = False  # Variable to track poll state

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

@tasks.loop(seconds=1)  # Checks every second
async def check_poll_end():
    global poll_closed  # Access the global variable
    if datetime.datetime.now() >= end_time:
        # Poll has ended, announce results and close the poll
        await close_poll()
        check_poll_end.cancel()  # Stop the loop
        poll_closed = True  # Set the poll state to closed

@check_poll_end.before_loop
async def before_check_poll_end():
    await bot.wait_until_ready()  # Wait for bot to be ready

async def close_poll():
    # Calculate poll results here
    results = "The poll has ended, and here are the results..."
    
    # Send the poll results as a message
    channel = bot.get_channel(int(channel_id))  # Replace with your channel ID
    await channel.send(results)

@bot.command()
async def poll(ctx, *, message):
    global poll_closed  # Access the global variable
    if poll_closed:
        await ctx.send("The poll is closed. You cannot vote.")
        return

    emb = discord.Embed(title="POLL", description=message)
    print("Nice")
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction('✔️')
    await msg.add_reaction('❌')
    check_poll_end.start()  # Start the poll duration check

bot.run(TOKEN)
