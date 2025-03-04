import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = '!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith("!hello"):
        await message.channel.send("Hello I am akoo_bot 👋")

bot.run(DISCORD_TOKEN)