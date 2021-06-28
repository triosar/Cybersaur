import requests
import os
from ro_py import users
from ro_py.users import User
import discord
from dotenv import load_dotenv
import keep_alive
import random
import time
from humanfriendly import format_timespan
from discord.ext import commands
from replit import db
import io
import contextlib
from discord.utils import get
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import logging
from trello import TrelloApi
import asyncio
from ro_py import Client
import traceback

serverlist = [] # server names
slist = [] #server objects
blacklist = [] # bot blacklist

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='c>',intents=intents)

badwords = ['nigger','niggers','nibber','nigga','nibba','faggot','faget',' fag ','fagging','fagot','mussie','mossie',' cum','ejaculate','jerk  of','lezzo','lezbo','lezzer','lezer','lezza','leza','masturbat','molest','porn', ' rape ','rimjob','rimming','blowjob','sextoy','skank','slut','sperm','sodom','tranny','tranni','trany','trani',' wank',' wog ','retard','f@g','re3tard','cunt','c u m',' c u m','hentai','ahegao','cocaine','crackhead','whore','spunk']

botAdminNames = ["🌌Creator🌌", "🔨Developer🔨", "🚀Staff Team🚀"]
botAdminRoles = [736246472814624789, 776437222177374220, 747588419265233046]
# creator, dev, staff

load_dotenv()
DISCTOKEN = os.getenv('DISCORD_TOKEN')
RS = os.getenv('ROBLOSECURITY')
TRELLO_APP_KEY = os.getenv('TRELLO_APP_KEY')

#define functions
async def botAdminCheck(user,guild):
  staffRole = discord.utils.find(lambda r: r.name == "🚀Staff Team🚀", guild.roles)
  devRole = discord.utils.find(lambda r: r.name == "🔨Developer🔨", guild.roles)
  creatorRole = discord.utils.find(lambda r: r.name == "🌌Creator🌌", guild.roles)

  if str(user.id) == "314394344465498122":
    return 4
  if creatorRole in user.roles:
    return 3
  if devRole in user.roles:
    return 2
  if staffRole in user.roles:
    return 1
  return False # i.e. not any level of admin


def clearUser(name):
  TRELLO_APP_KEY = os.getenv('TRELLO_APP_KEY')
  TOKEN = os.getenv('TOKEN')
  listID = "600ed147a982530da7b48b87"
  
  trello = TrelloApi(TRELLO_APP_KEY, TOKEN)

  cardList = trello.lists.get_card(listID)

  for x in cardList:
    splity = x["name"].split(":")[0] # i.e. the first split part of the card title
    if str(splity) == str(name):
      trello.cards.delete(x['id'])

def slurCheck(phrase):
  wordstatus = False
  msg = str((phrase)).lower()
  for x in badwords:
    if x in msg:
      wordstatus = x
  return wordstatus

def adminLog(userPing,fullmessage,comtype,server,channel):
    embedVar = discord.Embed(title="Admin Command Ran", description="",color=000000)
    embedVar.add_field(name="User", value=userPing, inline=False)
    embedVar.add_field(name="Command Type", value=comtype, inline=False)
    embedVar.add_field(name="Full Command", value=fullmessage, inline=False)
    embedVar.add_field(name="Server", value=server, inline=False)
    embedVar.add_field(name="Channel", value=channel, inline=False)
    embedVar.set_footer(text="Command log | Cybersaur")
    bot.loop.create_task(bot.get_channel(854711573490302976).send(embed=embedVar))


# bot function definitions
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you type! | Prefix is '>'!"))
    channel = bot.get_channel(854711573490302976)
    embedVar2 = discord.Embed(title="Bot connected to Discord",description=f'Bot successfully connected to Discord at {time.asctime()}.',color=000000)
    embedVar2.set_footer(text="Hello world | Cybersaur")
    await channel.send(embed=embedVar2)

    for server in bot.guilds:
      serverlist.append(str(server))
      slist.append(server)
      #await server.leave() #activate this to leave all servers

@bot.event
async def on_raw_reaction_add(payload):
  if str(payload.channel_id) != "859046592350781450":
    return
  
  if str(payload.emoji) != "🤖":
    return

  msgID = payload.message_id
  channelID = payload.channel_id
  channel = bot.get_channel(channelID)

  msg = await channel.fetch_message(msgID)

  embedVar = msg.embeds[0]
  embedVar.add_field(name="Approved moment", value="approved by the holy doge 🤖", inline=False)
  embedVar.color = 0x00a300
  embedVar.title = r"✅   // Mod Call \\"+r"\\   ✅"
  await channel.send(embed=embedVar)

@bot.event
async def on_message(message):

  if message.author == bot.user:
    return

  if str(message.author.id) == "819310933197324318":
    # ignore lithium
    return

  if (message.webhook_id):
    # ignore webhook posts
    return


  if message.channel.type is not discord.ChannelType.private:
    role = discord.utils.find(lambda r: r.name == '🚀Staff Team🚀', message.guild.roles)
    if role in (message.author).roles:
      dynoType = None
      if str(message.content).startswith("?ban "):
        dynoType = "Ban"
      elif str(message.content).startswith("?unban "):
        dynoType = "Unban"
      elif str(message.content).startswith("?warn "):
        dynoType = "Warn"
      elif str(message.content).startswith("?kick "):
        dynoType = "Kick"
      elif str(message.content).startswith("?mute "):
        dynoType = "Mute"
      elif str(message.content).startswith("?unmute "):
        dynoType = "Unmute"
      elif str(message.content).startswith("?delwarn "):
        dynoType = "Warn Deletion"

      if dynoType != None:
        embedVar = discord.Embed(title="Dyno Command Ran", description="",color=000000)
        embedVar.add_field(name="Username", value="<@"+str(message.author.id)+">", inline=False)
        embedVar.add_field(name="Action Type", value=dynoType, inline=False)
        embedVar.add_field(name="Full Message", value=str(message.content), inline=False)
        embedVar.set_footer(text="Staff Dyno Command log | Cybersaur")
        channel = bot.get_channel(854711573490302976)
        await channel.send(embed=embedVar)

  if message.channel.type is discord.ChannelType.private:
    channel = bot.get_channel(834397212481028136)
    user = str(message.author.id)
    user = "<@"+user+">"

    embedVar = discord.Embed(title="New Cybersaur DM", description="",color=0x00cc00)

    embedVar.add_field(name="Username:", value=(user), inline=False)
    embedVar.add_field(name="Message:",value = message.content,inline=False)
      
    await channel.send(embed=embedVar)

  elif slurCheck(message.content):
    botAdminSlur = False
    slurColour = 000000
    if await botAdminCheck(message.author,message.guild):
      botAdminSlur = True
      slurColour = 0xc20000
    phrase = slurCheck(message.content)
    channel = bot.get_channel(832614393279283211) #bot testing server
    pingperson = str(message.author.id)
    pingperson = "<@"+pingperson+">" 
    servername = str(message.guild.name)
    channelname = str(message.channel.name)
    total = str(message.content)

    embedVar = discord.Embed(title="Autofilter Triggered", description="",color=slurColour)

    embedVar.add_field(name="Username:", value=(pingperson), inline=False)
    embedVar.add_field(name="Server:",value = servername,inline=False)
    embedVar.add_field(name="Channel:",value = channelname,inline=False)
    embedVar.add_field(name="Trigger:",value = phrase,inline=False)
    embedVar.add_field(name="Entire Message:",value = total,inline=False)
    embedVar.set_footer(text="Autofilter | Cybersaur")
    if await botAdminCheck(message.author,message.guild):
        embedVar.set_footer(text="BotAdmin violation - the violating message was not deleted.")
    await bot.get_channel(854711573490302976).send(embed=embedVar)
      
    response = "Please don't use words like **"+phrase+"**!"
    try:
      await message.author.send(response)
    except:
      await message.channel.send("Watch your language, "+"<@"+str(message.author.id)+">.")
    finally:
      await message.add_reaction("😡")
      if not await botAdminCheck(message.author,message.guild):
        await message.delete()
    return

  if str(message.author.id) not in blacklist:
    await bot.process_commands(message)

@bot.command()
async def eval(ctx, *, code):
    if (ctx.message.author.id) != 314394344465498122:
      await ctx.send("Denied.")
      return
    str_obj = io.StringIO() #Retrieves a stream of data
    try:
        with contextlib.redirect_stdout(str_obj):
            exec(code)
    except Exception as e:
        return await ctx.send(f"```{e.__class__.__name__}: {e}```")
    await ctx.send(f'```{str_obj.getvalue()}```')
    adminLog("<@"+str(ctx.message.author.id)+">",str(ctx.message.content),"Code Execution",ctx.message.guild,ctx.message.channel)


@bot.command()
async def kick(ctx):
  if not await botAdminCheck(ctx.message.author,ctx.message.guild):
    await ctx.send("You are not authorised to run this command!")
    return
  await ctx.send("epic kick moment")

@bot.command()
async def ban(ctx):
  if not await botAdminCheck(ctx.message.author,ctx.message.guild):
    await ctx.send("You are not authorised to run this command!")
    return
  await ctx.send("epic ban moment")

@bot.command()
async def unban(ctx):
  if not await botAdminCheck(ctx.message.author,ctx.message.guild):
    await ctx.send("You are not authorised to run this command!")
    return
  await ctx.send("epic unban moment")

@bot.command()
async def trelloban(ctx):
  if await botAdminCheck(ctx.message.author,ctx.message.guild) < 2: 
    await ctx.send("You are not authorised to perform this command.")
    return
  await ctx.send("nice")
  
@bot.command()
async def adminlevels(ctx):
  response = "Triosar: 4\nCreator: 3\nDevs: 2\nStaff: 1\nNormies: 0"
  await ctx.send(response)

@bot.command()
async def bansearch(ctx):
  if not await botAdminCheck(ctx.message.author,ctx.message.guild):
    await ctx.send("You are not authorised to run this command.")
    return
  await ctx.send("ban search moment")

@bot.command()
async def mockup(ctx):
  if await botAdminCheck(ctx.message.author,ctx.message.guild) < 4: 
    await ctx.send("You are not authorised to perform this command.")
    return

  embedVar = discord.Embed(color=0xEC7200)
  embedVar.add_field(name=r"// Mod Call \\"+r"\\", value="A Mod Call has been sent from Pinewood Builders Tycoon\n--------------------------------------------------\n**REPORTER:** 249Grimawesome\n**SUSPECT:** 249Grimawesome\n**REPORT REASON:** Filter Abuse\n--------------------------------------------------\n**GAME LINK:** https://www.roblox.com/games/5436115608/\n--------------------------------------------------", inline=False)
  embedVar.set_thumbnail(url="https://images-ext-2.discordapp.net/external/ZVEJrowG97UBjZ0HuEL_nvXRxKg9VsyJBvW8tRjp-Ec/%3Fwidth%3D676%26height%3D676/https/media.discordapp.net/attachments/747579977532440746/780243500771180565/asfasdda1_0052.jpg?width=674&height=674")


  x = await ctx.send(embed=embedVar)
  await x.add_reaction("✅")
  await x.add_reaction("❌")

  embedVar = discord.Embed(color=0xa30800)
  embedVar.add_field(name=r"❌   // Mod Call \\"+r"\\   ❌", value="A Mod Call has been sent from Pinewood Builders Tycoon\n--------------------------------------------------\n**REPORTER:** 249Grimawesome\n**SUSPECT:** 249Grimawesome\n**REPORT REASON:** Filter Abuse\n--------------------------------------------------\n**GAME LINK:** https://www.roblox.com/games/5436115608/\n--------------------------------------------------", inline=False)
  embedVar.set_thumbnail(url="https://images-ext-2.discordapp.net/external/ZVEJrowG97UBjZ0HuEL_nvXRxKg9VsyJBvW8tRjp-Ec/%3Fwidth%3D676%26height%3D676/https/media.discordapp.net/attachments/747579977532440746/780243500771180565/asfasdda1_0052.jpg?width=674&height=674")
  embedVar.add_field(name="Denial Reason",value="`Triosar` - Grim is very poopy.", inline=False)


  x = await ctx.send(embed=embedVar)
  await x.add_reaction("✅")
  await x.add_reaction("❌")

  embedVar = discord.Embed(color=0x00a300)
  embedVar.add_field(name=r"✅   // Mod Call \\"+r"\\   ✅", value="A Mod Call has been sent from Pinewood Builders Tycoon\n--------------------------------------------------\n**REPORTER:** 249Grimawesome\n**SUSPECT:** 249Grimawesome\n**REPORT REASON:** Filter Abuse\n--------------------------------------------------\n**GAME LINK:** https://www.roblox.com/games/5436115608/\n--------------------------------------------------", inline=False)
  embedVar.set_thumbnail(url="https://images-ext-2.discordapp.net/external/ZVEJrowG97UBjZ0HuEL_nvXRxKg9VsyJBvW8tRjp-Ec/%3Fwidth%3D676%26height%3D676/https/media.discordapp.net/attachments/747579977532440746/780243500771180565/asfasdda1_0052.jpg?width=674&height=674")
  embedVar.add_field(name="Action Taken",value="`Triosar` - Grim has been fed to Gacha Reis :D", inline=False)


  x = await ctx.send(embed=embedVar)
  await x.add_reaction("✅")
  await x.add_reaction("❌")

@bot.command()
async def mockup2(ctx):
  if await botAdminCheck(ctx.message.author,ctx.message.guild) < 4: 
    await ctx.send("You are not authorised to perform this command.")
    return
  embedVar = discord.Embed(title = r"// Mod Call \\"+r"\\",color=0xEC7200)
  embedVar.add_field(name="** **", value="A Mod Call has been sent from Pinewood Builders Tycoon\n--------------------------------------------------\n**REPORTER:** 249Grimawesome\n**SUSPECT:** 249Grimawesome\n**REPORT REASON:** Filter Abuse\n--------------------------------------------------\n**GAME LINK:** https://www.roblox.com/games/5436115608/\n--------------------------------------------------", inline=False)
  embedVar.set_thumbnail(url="https://images-ext-2.discordapp.net/external/ZVEJrowG97UBjZ0HuEL_nvXRxKg9VsyJBvW8tRjp-Ec/%3Fwidth%3D676%26height%3D676/https/media.discordapp.net/attachments/747579977532440746/780243500771180565/asfasdda1_0052.jpg?width=674&height=674")

  x = await ctx.send(embed=embedVar)

keep_alive.keep_alive()
bot.run(DISCTOKEN)