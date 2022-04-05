import asyncio
import os
from posixpath import split
from typing import overload
import discord
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import yt_dlp as youtube_dl
import config as cfg

from random import choice

youtube_dl.utils.bug_reports_message = lambda: ''

main_token = 'ODgxODg5ODcwMDIzMzYwNTYy.YSzZ8Q.VydXQ5_gbCDDHBPJmcNi05h1iRQ'

test_token = 'ODgyMzE5OTQ5OTYyNTc1ODcz.YS5qfA.GB21iWctpEMqzht2jHTeLf88C30'


ytdl_format_options = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': u'%(id)s.%(ext)s',
    'noplaylist': True,
    'nocheckcertificate': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}
ffmpeg_options = {
    'options': '-vn'
}

playlist = []

client = commands.Bot(command_prefix='-')


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
async def j(ctx):  # join
    channel = ctx.message.author.voice.channel
    await channel.connect()


@commands.command()
async def join(ctx):  # join
    if not ctx.message.author.voice:
        await ctx.send('>>> Ateik pakalbėt, tada pagrosiu :grinning:')
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        msg = '>>> Koncertas prasideda! :raised_hands:\nTik duok keletą sekundžių apšilt :grinning:'
        await ctx.send(msg)


@client.command()
async def resume(ctx):  # resume
    server = ctx.message.guild
    voice_channel = server.voice_client
    await ctx.send('>>> Tesiam koncertą! :sunglasses:')
    voice_channel.resume()


@client.command()
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.pause()
    await ctx.send('>>> Padarom pertraukėlę :beers:')


@client.command()
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.stop()
    await ctx.send('>>> Koncertas baigtas! :pensive: ')
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()


@client.command()
async def skip(ctx):
    await ctx.send('>>> Dar tokio prijomo nemoku :face_with_raised_eyebrow:')


@client.command()
async def vol(ctx):  # volume
    await ctx.send('>>> Dar tokio prijomo nemoku :face_with_raised_eyebrow:')


@client.command()
async def bass(ctx):
    await ctx.send('>>> Dar tokio prijomo nemoku :face_with_raised_eyebrow:')


@client.command()
async def pagalba(ctx):
    help = '>>> fix **Kaimo muzikanto komandos**\n```diff\n+p arba +g - Paleisti/pridėti dainą į eilę\n+pause - Sustabdo dainą\n+resume - Tęsia dainą\n+stop - Išjungia dainą, atsijungia iš kanalo```'
    todo = '**Kuriama**\n```css\n+skip - Pereiti prie sekančios dainos\n+bass - Reguliuoti bosą\n+vol - Reguliuoti garsą\nInformacija apie dainą (laikas, pavadinimas, kas paleido)\nDainų leidimas iš playlisto```'
    stringas = help + '\n' + todo
    await ctx.send(stringas)


@client.command(name='g')
async def p(ctx, url):  # play command
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await join(ctx)
        await asyncio.sleep(2)
        await p(ctx, url)
    else:
        server = ctx.message.guild
        voice_channel = server.voice_client
        if '&' in url:
            tmp_url = url.split('&')
            url = tmp_url[0]
        
        song = url.split('=')
        if song[0] == 'https://www.youtube.com/watch?v' and '&' not in song[1]:
            url_dict = {'url': url, 'song': song[1]}

            await ctx.send('`{}` pridėta į albumą'.format(url))

        elif song[0] == 'https://www.youtube.com/playlist?list':
            await ctx.send('>>> Man geriau po vieną dainą paduok :smile:')
        else:
            await ctx.send('>>> Tokios dainos nežinau, surask kitą')

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

cln = discord.Client()

@tasks.loop(seconds=2)
async def status():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("music"))

print('\n-----[ Kaimo muzikantas ] -----\n')
print(' -> Bot online\n')

client.run(test_token)
