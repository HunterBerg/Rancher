  
import asyncio
import discord
import os
from dotenv import load_dotenv
import youtube_dl
from discord.ext import commands
import ffmpeg

load_dotenv()
BOT_TOKEN = os.getenv("TESTKEY")
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


    #------------------------------------------------------------------------------------------------------------
    #FFMPEG Setup
    























print(BOT_TOKEN)
# Bot.run("ODMzMDYyMjA3Mjg5MTYzNzc2.YHs3ow.-1IYYmpprBxJKSerZRXj_8ZDlgc") 