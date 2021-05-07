import discord
from discord.ext import commands
import ffmpeg

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

    


























Bot.run("ODMzMDYyMjA3Mjg5MTYzNzc2.YHs3ow.r4xmlExKXHypzlKSwJkfUN3j4XM") 
