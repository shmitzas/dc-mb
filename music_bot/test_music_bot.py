import asyncio
import os
from posixpath import split
from typing import overload
import discord
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import yt_dlp as youtube_dl
from config import *

youtube_dl.utils.bug_reports_message = lambda: ''

test_token = 'ODgyMzE5OTQ5OTYyNTc1ODcz.YS5qfA.GB21iWctpEMqzht2jHTeLf88C30'
main_token = 'ODgxODg5ODcwMDIzMzYwNTYy.YSzZ8Q.VydXQ5_gbCDDHBPJmcNi05h1iRQ'

zinute = {
    'pagalba': '**Kaimo muzikanto komandos**\n```+g - Paleisti/pridėti dainą į eilę\n+pause - Sustabdo dainą\n+resume - Tęsia dainą\n+stop - Išjungia dainą, atsijungia iš kanalo```',
    'todo': '**Kuriama**\n```+skip - Pereiti prie sekančios dainos\n+bass - Reguliuoti bosą\n+vol - Reguliuoti garsą\nInformacija apie dainą (laikas, pavadinimas, kas paleido)\nDainų leidimas iš playlisto```',
    'bugs': '**Žinomos problemos**\n```1. Pridedant dainą dažniau nei 1 per 5sec, pridėta daina negros\n```',
    'prideta_daina': '>>> `{}` pridėta į albumą\n',
    'nezinoma_komanda': '>>> Dar tokio prijomo nemoku :face_with_raised_eyebrow:',
    'pabaiga': '>>> Koncertas baigtas! :pensive:',
    'netinkamas_url': '>>> Tokios dainos nežinau, surask kitą',
    'pradzia': '>>> Koncertas prasideda! :raised_hands:\nTik duok keletą sekundžių apšilt :grinning:',
    'ne_vc': '>>> Ateik pakalbėt, tada pagrosiu :grinning:',
    'tesiam': '>>> Tesiam koncertą! :sunglasses:',
    'pertrauka': '>>> Padarom pertraukėlę :beers:'
}

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

queue = []
loop = False

client = commands.Bot(command_prefix='-')

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.id = data.get('id')
        self.song_id = self.id + '.mp3'
        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


'''
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.id = data.get('id')
        self.song_id = self.id + '.mp3'
        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download = not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
'''


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('music'))


def is_connected(ctx):
    voice_client = ctx.message.guild.voice_client
    return voice_client and voice_client.is_connected()


@client.command()
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()


@client.command()
async def ping(ctx):
    await ctx.send(f'>>> \n**Pong!** Latency: {round(client.latency * 1000)}ms\n')


@commands.command()
async def join(ctx):  # join
    if not ctx.message.author.voice:
        await ctx.send(zinute['ne_vc'])
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send(zinute['pradzia'])


@client.command()
async def resume(ctx):  # resume
    server = ctx.message.guild
    voice_channel = server.voice_client
    await ctx.send(zinute['tesiam'])
    voice_channel.resume()


@client.command()
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.pause()
    await ctx.send(zinute['pertrauka'])


@client.command()
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.stop()
    await ctx.send(zinute['pabaiga'])
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()


@client.command()
async def skip(ctx):
    await ctx.send(zinute['nezinoma_komanda'])


@client.command()
async def vol(ctx):  # volume
    await ctx.send(zinute['nezinoma_komanda'])


@client.command()
async def bass(ctx):
    await ctx.send(zinute['nezinoma_komanda'])


@client.command()
async def pagalba(ctx):
    stringas = '>>> ' + zinute['pagalba'] + \
        '\n' + zinute['todo'] + '\n'+zinute['bugs']
    await ctx.send(stringas)


@client.command(name='g', help='+g - Paleisti/pridėti dainą į eilę')
async def p(ctx, url):  # play command
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        await join(ctx)
    server = ctx.message.guild
    voice_channel = server.voice_client
    if not voice_channel.is_playing() or not voice_channel.is_paused():
        song = url.split('=')
        if song[0] == 'https://www.youtube.com/watch?v' and '&' not in song[1]:
            queue.append(url)
            await ctx.send(zinute['prideta_daina'].format(url))
            append_log('Komanda: [-g] | url: ' + url + '\nStatus: OK')
        else:
            await ctx.send(zinute['netinkamas_url'])
            append_log('Komanda: [-g] | url: ' + url +
                       '\nStatus: netinkasmas URL')

        while queue:
            ''' ------------------[ Player ]------------------- '''
            while voice_channel.is_playing() or voice_channel.is_paused():
                await asyncio.sleep(2)
            player = await YTDLSource.from_url(queue[0])
            voice_channel.play(discord.FFmpegPCMAudio(
                player.song_id), after=lambda e: append_log('Player ERROR: %s' % e) if e else None)
            await asyncio.sleep(player.duration+1)
            del(queue[0])
            os.remove(player.song_id)

print('\n-----[ [TEST] - Kaimo muzikantas ] -----\n')
print(' -> Bot online\n')

client.run(test_token)
