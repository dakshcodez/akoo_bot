import discord
from discord.ext import commands
import asyncio
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
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith("!hello"):
        await message.channel.send("Hello I am akoo_bot 👋")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name = "general")
    if channel:
        await channel.send(f'Hola {member.mention}, Welcome to the server!')

# slash commands for setting up reminders
@bot.tree.command(name="remind", description="Set a reminder")
async def remind(interaction: discord.Interaction, time: int, unit: str, message: str):
    if unit == 's':
        n_time = time
        await interaction.response.send_message(f"Reminder set for {time} seconds!", ephemeral=True)
    elif unit == 'm':
        n_time = time*60
        await interaction.response.send_message(f"Reminder set for {time} minutes!", ephemeral=True)
    elif unit == 'h':
        n_time = time*3600
        await interaction.response.send_message(f"Reminder set for {time} hours!", ephemeral=True)

   ## await interaction.response.send_message(f"Reminder set for {time} seconds!", ephemeral=True)
    await asyncio.sleep(n_time)
    await interaction.followup.send(f"⏰{interaction.user.mention} Reminder: {message}", ephemeral=True)

bot.run(DISCORD_TOKEN)