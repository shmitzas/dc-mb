import asyncio
import os
from posixpath import split
import discord
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import yt_dlp as youtube_dl

from random import choice

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format':'bestaudio/best',
    'extractaudio':True,
    'audioformat':'mp3',
    'outtmpl': u'%(id)s.%(ext)s',
    'noplaylist':False,
    'nocheckcertificate':True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}
ffmpeg_options = {
    'options': '-vn'
}

client = commands.Bot(command_prefix='+')

# ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)

#         self.data = data

#         self.title = data.get('title')
#         self.url = data.get('url')

def is_connected(ctx):
    voice_client = ctx.message.guild.voice_client
    return voice_client and voice_client.is_connected()

@client.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command()
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')

@client.command()
async def j(ctx): #join
    channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command()
async def resume(ctx): #resume
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.resume()

@client.command()
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.pause()

@client.command()
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.stop()

@client.command()
async def skip(ctx):
    await ctx.send('Dar tokio prijomo nemoku :face_with_raised_eyebrow:')

@client.command()
async def vol(ctx): #volume
    await ctx.send('Dar tokio prijomo nemoku :face_with_raised_eyebrow:')
    
@client.command()
async def bass(ctx):
    await ctx.send('Dar tokio prijomo nemoku :face_with_raised_eyebrow:')

@client.command()
async def p(ctx, url): #play command
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        channel = ctx.message.author.voice.channel
        await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client

    song = url.split('=')
    if song[0] == 'https://www.youtube.com/watch?v':
        url_dict = {'url':url, 'song':song[1]}
        await ctx.send('`{}` pridėta į albumą'.format(url))
        
    elif song[0] == 'https://www.youtube.com/playlist?list':
        await ctx.send('Man geriau po vieną dainą paduok :smile:')
    else:
        await ctx.send('Tokios dainos nežinau, surask kitą')

    ''' ------------------[ Player ]------------------- '''
    if len(url_dict) != 0:
        with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
            ydl.download(url_dict['url'])
        while voice_channel.is_playing() or voice_channel.is_paused():
            await asyncio.sleep(2)
        for file in os.listdir("./"):
            song_name = url_dict['song']+'.mp3'
            if file.endswith(song_name):
                print(file)
                voice_channel.play(discord.FFmpegPCMAudio(song_name))
    

print("Bot online")
client.run('ODgxODg5ODcwMDIzMzYwNTYy.YSzZ8Q.VydXQ5_gbCDDHBPJmcNi05h1iRQ')