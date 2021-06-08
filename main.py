import discord
import asyncio
import os
from dotenv import load_dotenv
import youtube_dl
import math
from discord.utils import get
from discord.ext import commands


queue = []
queue_looping = False

load_dotenv()
token = os.getenv("TOKEN")

 

Bot = commands.Bot(
	command_prefix=commands.when_mentioned_or("*"),
	description='Relatively simple music bot example'
)


#------------------------------------------------------------------------------------------------------------
#youtube_dl 

# Suppress noise about console usage from errors



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


class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def join(self, ctx, *, channel: discord.VoiceChannel):
		"""Joins a voice channel"""

		if ctx.voice_client is not None:
			return await ctx.voice_client.move_to(channel)
		else:
			channel=ctx.message.author.voice.channel()
			self.queue={}
		await channel.connect()

	



	# @commands.command()
	# async def play(self, ctx, *, url):

	# 	try:

	# 		async with ctx.typing():
	# 			player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
	# 			ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

	# 		await ctx.send(f':mag_right: **Searching for** ``' + url + '``\n<:youtube:763374159567781890> **Now Playing:** ``{}'.format(player.title) + "``")

	# 	except:

	# 		await ctx.send("Somenthing went wrong - please try again later!")

	@commands.command()
	async def play(self, ctx, *, url):

		global queue
		global queue_looping

		try:
			queue.append(url)
			user = ctx.message.author.mention
			await ctx.send(f'``{url}`` was added to the queue by {user}!')
		except:
			await ctx.send(f"Couldnt add {url} to the queue!")

		if queue_looping:
			return

		queue_looping = True
		for url in queue:

			try:

				async with ctx.typing():
					player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
					ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

				await ctx.send(f'<:youtube:763374159567781890> **Now Playing:** ``{url}``')

			except:

				await ctx.send("Somenthing went wrong - please try again later!")
			
		else:

			await ctx.send("Queue is now done!")

			queue_looping = False

	@commands.command()
	async def pause(self, ctx):
		voice = get(self.bot.voice_clients, guild=ctx.guild)

		voice.pause()

		user = ctx.message.author.mention
		await ctx.send(f"Bot was paused by {user}")

	@commands.command()
	async def resume(self, ctx):
		voice = get(self.bot.voice_clients, guild=ctx.guild)

		voice.resume()

		user = ctx.message.author.mention
		await ctx.send(f"Bot was resumed by {user}")

	@commands.command()
	async def add_queue(self, ctx, url):

		global queue

		try:
			queue.append(url)
			user = ctx.message.author.mention
			await ctx.send(f'``{url}`` was added to the queue by {user}!')
		except:
			await ctx.send(f"Couldnt add {url} to the queue!")
	@commands.command()
	async def clear_queue(self, ctx):

		global queue

		queue.clear()
		user = ctx.message.author.mention
		await ctx.send(f"The queue was cleared by {user}")
	
	@commands.command()
	async def view_queue(self, ctx):

		if len(queue) < 1:
			await ctx.send("The queue is empty - nothing to see here!")
		else:
			await ctx.send(f'Your queue is now {queue}')


	@commands.command()
	async def stop(self, ctx):
		"""Stops and disconnects the bot from voice"""
		if ctx.message.author.id == 355099018113843200:

			await ctx.voice_client.disconnect()

		else:
			await ctx.send("this is not a command you can use")



	@play.before_invoke
	async def ensure_voice(self, ctx):
		if ctx.voice_client is None:
			if ctx.author.voice:
				await ctx.author.voice.channel.connect()
			else:
				await ctx.send("You are not connected to a voice channel.")
				raise commands.CommandError("Author not connected to a voice channel.")
		elif ctx.voice_client.is_playing():
			ctx.voice_client.stop()

#####################

@Bot.command() # *ping command
async def ping(ctx):
	await ctx.send(f'Pong! `{math.floor(Bot.latency * 1000)}` ms')

@Bot.command() #speak command (*speak)
async def speak(ctx, *, text):
	if ctx.message.author.id == 355099018113843200:
		message = ctx.message 
		await message.delete()

		await ctx.send(text)
	else:
		await ctx.send("this is not a command you can use")

@Bot.command()
async def lick(ctx): #tounge command (*lick)
	await ctx.send("https://tenor.com/view/licktung-pokemon-wiggle-tongue-tongue-out-bleh-gif-17629715")

@Bot.event #bot status
async def on_ready():
	await Bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Music"))
	print('Rancher is Online')


Bot.add_cog(Music(Bot))
Bot.run(token)