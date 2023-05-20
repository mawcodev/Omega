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

queues = {}

def check_queue(ctx, id):
    if queues[id] != []:
        voz = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voz.play(source,  after=lambda x=None: check_queue(ctx, ctx.message.guild.id))
        #Nivelamos el volumen para que siempre suenen en la misma intensidad
        voz.source = discord.PCMVolumeTransformer(voz.source, volume=0.1)

intents = discord.Intents.default()
intents.message_content = True

#bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix = '!',intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game(name = 'Ingresa !command url-youtube-corta y mira la magia!'))
    print('Estoy Vivoooo')

#Para conectarse a un canal de voz
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
#Para desconectarse del canal de voz
@bot.command(pass_context = True)
async def desconectar(ctx):
    canal = ctx.message.author.voice.channel
    voz = get(bot.voice_clients,guild=ctx.guild)
    await voz.disconnect()
#Para reproducir una canción
@bot.command(pass_context = True)
async def play(ctx, url):
    voz = ctx.guild.voice_client
    if not voz:
        await ctx.send('No estoy conectado a un canal de voz')
        return

    try:
        video = YouTube(url)
        best_audio = video.streams.get_audio_only()

        source = discord.FFmpegPCMAudio(
            best_audio.url,
            before_options="-reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 2"
        )

        voz.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))
        voz.source = discord.PCMVolumeTransformer(voz.source, volume=0.1)
        await ctx.send('Reproduciendo música de YouTube')

        while voz.is_playing():
            await asyncio.sleep(5)

        #await voz.disconnect()
        await ctx.send('Reproducción finalizada - Next, baby!')

    except Exception as e:
        await ctx.send(f'Error al reproducir música: {str(e)}')
#Para pausar las canciones de la lista
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
#Para continuar con la reproducción
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
#Para parar la reproducción
@bot.command(pass_context = True)
async def stop(ctx):
    voz = ctx.guild.voice_client
    if not voz:
        await ctx.send('No estoy conectado a un canal de voz')
        return
    voz.stop()
#Para añadir a la cola de reproducción más canciones
@bot.command(pass_context = True)
async def queue(ctx,url):
    voz = ctx.guild.voice_client
    if not voz:
        await ctx.send('No estoy conectado a un canal de voz')
        return

    guild_id = ctx.message.guild.id
    video = YouTube(url)
    best_audio = video.streams.get_audio_only()

    source = discord.FFmpegPCMAudio(
        best_audio.url,
        before_options="-reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 2"
    )
    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id] = [source]
    await ctx.send("Añadida a la cola")

@bot.command(pass_context = True)
async def lista(ctx):
    voz = ctx.guild.voice_client
    if not voz:
        await ctx.send('No estoy conectado a un canal de voz')
        return
    print(queues)

    for item in queues:
        for i in item:
            await ctx.send(i)

bot.run(TOKEN)