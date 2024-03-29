# This example requires the 'message_content' intent.
import os
import discord
from discord.ext import commands
from discord.utils import get
from pytube import YouTube
from dotenv import load_dotenv
import yt_dlp as youtube_dl
import asyncio
#import youtube_dl

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

print(TOKEN)

intents = discord.Intents.default()
intents.message_content = True

#bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix = '!',intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game(name = 'Ingresa !command url-youtube-corta y mira la magia!'))
    print('Estoy Vivoooo')

@bot.command()
async def video(ctx):
    await ctx.send('https://bit.ly/2qt0bNM')

@bot.command(pass_context = True)
async def conectar(ctx):
    canal = ctx.message.author.voice.channel
    if not canal:
        await ctx.send('No estas Conectado a un canal de VOZ')
        return
    voz = get(bot.voice_clients,guild=ctx.guild)
    if voz and voz.is_connected():
        await voz.move_to(canal)
    else:
        voz = await canal.connect()

@bot.command(pass_context = True)
async def desconectar(ctx):
    canal = ctx.message.author.voice.channel
    voz = get(bot.voice_clients,guild=ctx.guild)
    await voz.disconnect()

@bot.command(pass_context = True)
async def play(ctx, url):
    voz = ctx.guild.voice_client
    if not voz:
        await ctx.send('No estoy conectado a un canal de voz')
        return

    try:
        video = YouTube(url)
        best_audio = video.streams.get_audio_only()

        audio_source = discord.FFmpegPCMAudio(
            best_audio.url,
            before_options="-reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 2"
        )

        voz.play(audio_source)
        voz.source = discord.PCMVolumeTransformer(voz.source, volume=0.06)
        await ctx.send('Reproduciendo música de YouTube')

        while voz.is_playing():
            await asyncio.sleep(1)

        #await voz.disconnect()
        await ctx.send('Reproducción finalizada - Next, baby!')

    except Exception as e:
        await ctx.send(f'Error al reproducir música: {str(e)}')

@bot.command(pass_context = True)
async def pause(ctx):
    voz = ctx.guild.voice_client
    if not voz:
        await ctx.send('No estoy conectado a un canal de voz')
        return

    if voz.is_playing():
        voz.pause()
    else:
        await ctx.send('En este momento no está sonando ninguna canción...')

@bot.command(pass_context = True)
async def resume(ctx):
    voz = ctx.guild.voice_client
    if not voz:
        await ctx.send('No estoy conectado a un canal de voz')
        return

    if voz.is_paused():
        voz.resume()
    else:
        await ctx.send('En este momento no hay ninguna canción pausada...')

@bot.command(pass_context = True)
async def stop(ctx):
    voz = ctx.guild.voice_client
    if not voz:
        await ctx.send('No estoy conectado a un canal de voz')
        return
    voz.stop()

bot.run('******')