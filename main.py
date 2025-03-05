import discord
from discord.ext import commands
import asyncio
import yt_dlp as youtube_dl
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_TOKEN = os.getenv('GEMINI_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix = "!", intents=intents)
client = genai.Client(api_key = GEMINI_TOKEN)

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
    
    elif message.content.lower() == "!are u alive":
        await message.channel.send("Yes I am alive and kicking")

# @bot.command()
# async def hello(ctx):
#     await ctx.send("Hello I am akoo_bot 👋")

#welcome message
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name = "general")
    if channel:
        await channel.send(f'Hola {member.mention}, Welcome to the server!')

# @bot.command()  
# async def join(ctx):
#     if not ctx.author.voice:
#         await ctx.send("Join a voice channel first!")
#         return
    
#     channel = ctx.author.voice.channel

#     if ctx.voice_client:
#         await ctx.send(f"I'm already connected to {ctx.voice_client.channel.name}.")
#         return
    
#     try:
#         await channel.connect()
#         await ctx.send(f"Joined {channel.name}!")
#     except Exception as e:
#         await ctx.send(f"An error occurred: {str(e)}")
#         print(f"Error connecting to channel: {e}")

# @bot.command()
# async def disconnect(ctx):
#     if ctx.voice_client:
#         await ctx.voice_client.disconnect()

@bot.tree.command(name="join", description="Join a voice channel")
async def join(interaction: discord.Interaction):
    if not interaction.user.voice:
        await interaction.response.send_message("Join a voice channel first!", ephemeral=True)
        return
    
    channel = interaction.user.voice.channel

    if interaction.guild.voice_client:
        await interaction.response.send_message(f"I'm already connected to {interaction.guild.voice_client.channel.name}.", ephemeral=True)
        return
    
    try:
        await channel.connect()
        await interaction.response.send_message(f"Joined {channel.name}!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)
        print(f"Error connecting to channel: {e}")

@bot.tree.command(name="disconnect", description="Disconnect from a voice channel")
async def disconnect(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("Disconnected from voice channel!", ephemeral=True)

#Reminder command
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

    await asyncio.sleep(n_time)
    await interaction.followup.send(f"⏰{interaction.user.mention} Reminder: {message}", ephemeral=True)

#Gemini generated responses
@bot.tree.command(name="ai", description="Ask gemini 2.0 flash")
async def ai(interaction: discord.Interaction, message: str):
    await interaction.response.defer()
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[message] 
        )

        response_text = getattr(response, "text", "No response received.")

        if len(response_text) > 2000:
            parts =[response_text[i:i+2000] for i in range(0, len(response_text), 2000)]
            for part in parts:
                await interaction.followup.send(part)
        else: 
            await interaction.followup.send(response_text)

    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)}") 

bot.run(DISCORD_TOKEN)