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

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name = "general")
    if channel:
        await channel.send(f'Hola {member.mention}, Welcome to the server!')

async def join(interaction: discord.Interaction, respond=True):
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        if interaction.guild.voice_client is None:
            await channel.connect()
            if respond:
                await interaction.response.send_message(f"Joined {channel.name}")
        else:
            if respond:
                await interaction.response.send_message("Already in a voice channel.")
    else:
        if respond:
            await interaction.response.send_message("You are not in a voice channel.")

async def leave(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("Left the voice channel.")
    else:
        await interaction.response.send_message("Not in a voice channel.")

@bot.tree.command(name="join", description="Joins the voice channel")
async def join_command(interaction: discord.Interaction):
    await join(interaction)

@bot.tree.command(name="leave", description="Leaves the voice channel")
async def leave_command(interaction: discord.Interaction):
    await leave(interaction)

# Music playback functions.
youtube_dl_opts = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # Bind to IPv4 since IPv6 addresses cause issues sometimes.
}

ffmpeg_opts = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(youtube_dl_opts)

async def play(interaction: discord.Interaction, url: str):
    """ Plays a song from a YouTube URL. """
    if interaction.guild.voice_client is None:
        await join(interaction, respond=False)  # Prevent duplicate responses.

    voice_client = interaction.guild.voice_client

    try:
        data = ytdl.extract_info(url, download=False)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")
        return

    if 'entries' in data:
        data = data['entries'][0]

    filename = data['url']

    voice_client.play(discord.FFmpegPCMAudio(filename, **ffmpeg_opts), after=lambda e: print(f'Player error: {e}') if e else None)
    await interaction.followup.send(f"Now playing: {data['title']}")

@bot.tree.command(name="play", description="Plays a song from YouTube")
async def play_command(interaction: discord.Interaction, url: str):
    await interaction.response.defer()  # Prevents multiple responses issue.
    await play(interaction, url)

@bot.tree.command(name="stop", description="Stops the currently playing song")
async def stop_command(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await interaction.response.send_message("Stopped playing.")
    else:
        await interaction.response.send_message("Nothing is playing.")

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