import discord
from discord.ext import commands
import youtube_dl
from discord.voice_client import VoiceClient





    
    
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


Bot = commands.Bot(command_prefix = '*') #prefix for the bot

 
@Bot.command() # *ping command
async def ping(ctx):
    await ctx.send(f'Pong! `{Bot.latency * 1000}` ms')

@Bot.command() #speak command (*speak)
async def speak(ctx, *, text):
     if ctx.message.author.id == 355099018113843200:
          message = ctx.message 
          await message.delete()

          await ctx.send(message)
     else:
          await ctx.send("this is not a command you can use")

@Bot.command()
async def lick(ctx): #tounge command (*lick)
     await ctx.send("https://tenor.com/view/licktung-pokemon-wiggle-tongue-tongue-out-bleh-gif-17629715")
    

@Bot.event #bot status
async def on_ready():
     await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Music"))
     print('Rancher is Online')


@Bot.command()
async def play(ctx,url):
     if not ctx.message.author.voice:
          await ctx.send("You are not in a voice channel")
          return

          else: #error fix ASAP
               channel = ctx.message.author.voice.channel

    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('**Now playing:** {}'.format(player.title))

@client.command(name='stop', help='This command stops the music and makes the bot leave the voice channel')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()
          


    
    




























Bot.run("ODMzMDYyMjA3Mjg5MTYzNzc2.YHs3ow.r4xmlExKXHypzlKSwJkfUN3j4XM") 
