#Hunter Berg
#Mrs.Bender
#Computer Science 30
#Discord Music Bot

import discord
import asyncio
import os
from dotenv import load_dotenv
import youtube_dl
import math
from discord.utils import get
from discord.ext import commands
from stay_alive import keep_alive #keeps bot running 24/7




load_dotenv()
token = os.environ['TOKEN'] #this makes it so if i share my code my bot token doesnt get leaked
 

Bot = commands.Bot(
	command_prefix=commands.when_mentioned_or("*"), #the prefix is what is infront of all commands (ex *play)
	description='The Rancher - The Music Bot '
)


#------------------------------------------------------------------------------------------------------------
#youtube_dl - youtube-dl is an open-source download manager for video and audio from YouTube and over 1000 other video hosting websites 

# Suppress noise about console usage from errors

#ffmpeg is what encodes and formats the audio

# Suppress noise about console usage from errors
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


class Music(commands.Cog): #class

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def join(self, ctx, *, channel: discord.VoiceChannel): #makes bot join vc 
		"""Makes the bot join the voice channel"""
		
		if ctx.voice_client is not None: #if the bot isnt in a vc it will join 
			return await ctx.voice_client.move_to(channel)
		else:
			channel=ctx.message.author.voice.channel() #join the vc 
			self.queue={}
		await channel.connect()

	@commands.command()
	async def play(self, ctx, *, url): #joins the vc automatically if not in one and searchs the song using youtube_dl then plays it. 
		"""Makes the bot join the voice channel and play the song you request using youtube_dl"""
		try: #it will try to play the song 
			async with ctx.typing():
				player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
				ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

			await ctx.send(f'Now playing: {player.title}')

		except: #if it cant play the song 
			await ctx.send("Something went wrong.")

	@commands.command()
	async def pause(self, ctx): #pauses the song playing in vc (if there is one)
		"""Pauses the music playing in the voice channel"""
		voice = get(self.bot.voice_clients, guild=ctx.guild)

		voice.pause()

		user = ctx.message.author.mention
		await ctx.send(f"Bot was paused by {user}")

	@commands.command()
	async def resume(self, ctx): #resumes the music if it was paused
		"""Continues to play the music in a voice channel if it was paused"""
		voice = get(self.bot.voice_clients, guild=ctx.guild)

		voice.resume()

		user = ctx.message.author.mention
		await ctx.send(f"Bot was resumed by {user}")

	@commands.command()
	async def stop(self, ctx): #stops playing the music in vc (if there is any playing)
		"""Stops playing the music playing in the voice channel"""
		await ctx.voice_client.disconnect()

	@play.before_invoke
	async def ensure_voice(self, ctx):
		if ctx.voice_client is None:
			if ctx.author.voice:
				await ctx.author.voice.channel.connect()
			else:
				await ctx.send("You are not connected to a voice channel.") #checks if the user requesting the command is in a vc
				raise commands.CommandError("Author not connected to a voice channel.")
		elif ctx.voice_client.is_playing():
			ctx.voice_client.stop()

#####################

@Bot.command() # *ping command
async def ping(ctx): #shows latency of bot in ms 
	"""Shows the ping of the bot ton the Discord servers in ms"""
	await ctx.send(f'Pong! `{math.floor(Bot.latency * 1000)}` ms')

@Bot.command() #speak command (*speak)
async def speak(ctx, *, text):
	"""A command only Hunter can use. It allows him to speak through the bot."""
	if ctx.message.author.id == 355099018113843200:
		message = ctx.message 
		await message.delete()

		await ctx.send(text)
	else:
		await ctx.send("this is not a command you can use")

@Bot.command()
async def lick(ctx): #tounge command (*lick)
	"""Sends a gif in chat :)"""
	await ctx.send("https://tenor.com/view/licktung-pokemon-wiggle-tongue-tongue-out-bleh-gif-17629715")

@Bot.event #bot status
async def on_ready():
	await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Music"))
	print('Rancher is Online') #prints this in the consle when the bot is running 

keep_alive() #keeps bot running 24/7

Bot.add_cog(Music(Bot)) 
Bot.run(token)