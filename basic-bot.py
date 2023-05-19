# This example requires the 'message_content' intent.
import os
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import yt_dlp as youtube_dl

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

print(TOKEN)

intents = discord.Intents.default()
intents.message_content = True

#bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix = '!',intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game(name = 'Ingresa !video y mira la magia!'))
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
async def play(ctx, url:str):
    cancionactiva = os.path.isfile("cancion.mp3")
    try:
        if cancionactiva:
            os.remove("cancion.mp3")
            print("La cancion se ha removido")
    except PermissionError:
        print("Reproduciendo canción")
        await ctx.send("Error: Cancion reproduciendose")
        return
    await ctx.send("Todo listo")
    voz = get(bot.voice_clients,guild=ctx.guild)
    ydl_op = {
        'format':'bestaudio/best',
        'postprocessor': [{
            'key':'FFmpegExtractAudio',
            'proferredcodec':'.webm',
            'proferredquality':'192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_op) as ydl:
        print("Descargar Cancion")
        ydl.download([url])

    for file in os.listdir("./"):
        nombre, extension = os.path.splitext(file)
        print(extension)
        if extension ==".webm":
            name = nombre
            print(f"Renombrando Archivo: {file}")
            os.rename(file,"cancion.webm")
            print(file)

    source = discord.FFmpegPCMAudio(file)
    voz.play(source, after=lambda e: print("ha terminado"))
    voz.source = discord.PCMVolumeTransformer(voz.source)
    voz.source.volume = 0.2

    nombre = name.rsplit("-",2)
    await ctx.send(f"Reproduciendo: {nombre[0]}")

bot.run('MTEwMzcwMTk4NDQ3OTAyMzE0NQ.GyBi2N.xBCKvYb7q9SiOrVMf65AeCXCv03Xw1YRUJe_0Y')