import os;
import discord;
import asyncio
import yt_dlp
import logging
from dotenv import load_dotenv

def run_bot():
    load_dotenv()
    TOKEN=os.getenv("discord_token")
    logging.basicConfig(level=logging.DEBUG)
    intents = discord.Intents.default()
  
    intents.message_content = True
    client = discord.Client(intents = intents)
    
    voice_clients = {}
    yt_dlp_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dlp_options)
    
    ffmpeg_options  = {"options": "-vn"}
    
    
    @client.event
    async def on_ready():
        print(f"{client.user} is now jamming")
        
    @client.event
    async def on_message(message):
        if message.content.startswith("?play"):
            try:
                voice_client = await message.author.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            except Exception as e:
                print(e)
            
            try:
                url = message.content.split()[1]
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False));
                
                song = data['url']
                player = discord.FFmpegPCMAudio(song, **ffmpeg_options )
                voice_clients[message.guild.id].play(player)
            except Exception as e:
                print(e)
                
    client.run(TOKEN)    



