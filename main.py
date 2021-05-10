  
import asyncio
import discord
import os
import youtube_dl
from discord.ext import commands
import ffmpeg

BOT_TOKEN = os.environ['BOT_TOKEN']
#Basic Bot commands
#-------------------------------------------------------------------------------------------------------------------------------------


Bot = commands.Bot(command_prefix = '*')

 
@Bot.command() # *ping command
async def ping(ctx):
    await ctx.send(f'Pong! `{Bot.latency * 1000}` ms')

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


    #------------------------------------------------------------------------------------------------------------
    #FFMPEG Setup
    























Bot.run(BOT_TOKEN) 