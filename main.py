# Cybersaur main file. - infinitypupper

# Import like 4532534534543 modules
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
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='c>',intents=intents)

# One of the bits for Discord channel logging. Currently off for development purposes.
# logging.basicConfig(filename='test.log', format='%(filename)s: %(message)s',
#     level=logging.ERROR)


db["s3p"] = int(0) # current Stage 3 page

# where blacklist pages are stored
s1bEmbeds = []
s2bEmbeds = []
s3bEmbeds = []


xmasTime = int(1640390400) # define christmas day as unix

# Declare various lists for use.
badwords = ['nigger','niggers','nibber','nigga','nibba','faggot','faget',' fag ','fagging','fagot','mussie','mossie',' cum','ejaculate','jerk  of','lezzo','lezbo','lezzer','lezer','lezza','leza','masturbat','molest','porn', ' rape ','rimjob','rimming','blowjob','sextoy','skank','slut','sperm','sodom','tranny','tranni','trany','trani',' wank',' wog ','retard','f@g','re3tard','cunt','c u m',' c u m','hentai','ahegao','cocaine','crackhead','whore','spunk']
botadmins = ["314394344465498122"]
blacklist = [] # yeah idk what this is used for
rps_choices = ["scissors!", "rock!", "paper!"]
serverlist = [] # server names
slist = [] #server objects

# define time
starttime = time.time()
print(starttime)

#load from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# function to delete a card from the trelloban list
def clearUser(name):
  TRELLO_APP_KEY = os.getenv('TRELLO_APP_KEY')
  TOKEN = os.getenv('TOKEN')
  listID = "6093ccae8f0a0a4e409fa1ce"
  
  trello = TrelloApi(TRELLO_APP_KEY, TOKEN)

  cardList = trello.lists.get_card(listID)

  for x in cardList:
    splity = x["name"].split(":")[0] # i.e. the first split part of the card title
    if str(splity) == str(name):
      trello.cards.delete(x['id'])

# poorly named, but this is the command that continually logs 
async def checkQ():
  while True:
    await asyncio.sleep(1)
    fileq = open("test.log","r")
    for x in fileq:
      toSend = "```py\n"+x+"```"
      bot.loop.create_task((bot.get_channel(832614393279283211)).send(toSend))
    fileq.close()
    open('test.log', 'w').close()

# returns any friends the provided user has who are also blacklisted
async def checkFriends(username):
  RS = os.getenv('ROBLOSECURITY')
  roblox = Client(RS)

  TRELLO_APP_KEY = os.getenv('TRELLO_APP_KEY')
  TOKEN = os.getenv('TOKEN')
  trello = TrelloApi(TRELLO_APP_KEY, TOKEN)
  listIDBL = "6093ccae8f0a0a4e409fa1ce"

  user = await roblox.get_user_by_username(username)
  friendList = []
  trelloBL = []
  badList = []
  crossover = []
  for x in await user.get_friends():
    friendList.append(str(x.id))
  for x in trello.lists.get_card(listIDBL):
    if str(x["name"].split(":")[1]) in ["1","2","3"]:
      badList.append(str(x["name"].split(":")[0]))
  for x in friendList:
    if (x in badList):
      crossover.append(x)
  return crossover

# logging function for any kind of "admin" command
def adminLog(userPing,fullmessage,comtype,server,channel):
    embedVar = discord.Embed(title="Admin Command Ran", description="",color=0x03a1fc)
    embedVar.add_field(name="User", value=userPing, inline=False)
    embedVar.add_field(name="Command Type", value=comtype, inline=False)
    embedVar.add_field(name="Full Command", value=fullmessage, inline=False)
    embedVar.add_field(name="Server", value=server, inline=False)
    embedVar.add_field(name="Channel", value=channel, inline=False)
    embedVar.set_footer(text="Command log | Cybersaur")
    bot.loop.create_task(bot.get_channel(854711573490302976).send(embed=embedVar))

# checks if a phrase is in the slur list, and which one
def slurCheck(phrase):
  wordstatus = False
  msg = str((phrase)).lower()
  for x in badwords:
    if x in msg:
      wordstatus = x
  return wordstatus





# @bot.event
# async def on_command_error(ctx,error):
#   logging.error(error)


# @bot.event
# async def on_error(event, *args, **kwargs):
#     message = args[0] #Gets the message object
#     logging.error(traceback.format_exc()) #logs the error

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you type! | Prefix is 'c>'!"))
    channel = bot.get_channel(854711573490302976)
    embedVar2 = discord.Embed(title="Bot connected to discord",description=f'Bot successfully connected to Discord at {time.asctime()}.',color=0x03a1fc)
    embedVar2.set_footer(text="Hello world | Cybersaur")
    await channel.send(embed=embedVar2)

    for server in bot.guilds:
      serverlist.append(str(server))
      slist.append(server)
      #await server.me.edit(nick="Cybersaur")
      #await server.leave() #activate this to leave all servers
    #inv = await (bot.get_channel(747581697826095260)).create_invite()
    #await user.send(inv)
    await checkQ()


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

  if "amogus" in str(message.content).lower():
    await message.add_reaction("<:red:760064755649347604>")

  if "owo" in str(message.content).lower():
    toSend = random.choice([
      "(●'◡'●)",
    "ʕʘ‿ʘʔ",
    "༼ つ ◕_◕ ༽つ",
    "(ˉ﹃ˉ)",
    "(⊙_⊙;)",
    "(T_T)",
    "ᓚᘏᗢ",
    "( ´･･)ﾉ(._.`)",
    "(☞ﾟヮﾟ)☞",
    "ඞ"])
    await message.channel.send(toSend)

  if "honk" == str(message.content).lower():
    await message.channel.send("https://cdn.discordapp.com/attachments/642880448862879759/849436442152534016/5b2.png")

#   CODE RELATED TO DYNO LOGGING. WILL BE DISABLED FOR NOW.
#   if message.channel.type is not discord.ChannelType.private:
#     role = discord.utils.find(lambda r: r.name == 'NOU Agent', message.guild.roles)
#     if role in (message.author).roles:
#       dynoType = None
#       if str(message.content).startswith("?ban "):
#         dynoType = "Ban"
#       elif str(message.content).startswith("?unban "):
#         dynoType = "Unban"
#       elif str(message.content).startswith("?warn "):
#         dynoType = "Warn"
#       elif str(message.content).startswith("?kick "):
#         dynoType = "Kick"
#       elif str(message.content).startswith("?mute "):
#         dynoType = "Mute"
#       elif str(message.content).startswith("?unmute "):
#         dynoType = "Unmute"
#       elif str(message.content).startswith("?delwarn "):
#         dynoType = "Warn Deletion"

#       if dynoType != None:
#         embedVar = discord.Embed(title="Dyno Command Ran", description="",color=0x03a1fc)
#         embedVar.add_field(name="Username", value="<@"+str(message.author.id)+">", inline=False)
#         embedVar.add_field(name="Action Type", value=dynoType, inline=False)
#         embedVar.add_field(name="Full Message", value=str(message.content), inline=False)
#         embedVar.set_footer(text="NOU Dyno Command log | Cybersaur")
#         channel = bot.get_channel(796891566341226506)
#         await channel.send(embed=embedVar)

  if message.channel.type is discord.ChannelType.private:
    channel = bot.get_channel(854711573490302976)
    user = str(message.author.id)
    user = "<@"+user+">"

    embedVar = discord.Embed(title="New Cybersaur DM", description="",color=0x03a1fc)

    embedVar.add_field(name="Username:", value=(user), inline=False)
    embedVar.add_field(name="Message:",value = message.content,inline=False)
      
    await channel.send(embed=embedVar)

  elif slurCheck(message.content):
    botAdminSlur = False
    slurColour = 000000
    if str(message.author.id) in botadmins:
      botAdminSlur = True
      slurColour = 0xc20000
    phrase = slurCheck(message.content)
    channel = bot.get_channel(854711573490302976) #bot testing server
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
    if botAdminSlur:
        embedVar.set_footer(text="BotAdmin violation - the violating message was not deleted.")


    try:
      await message.author.send(response)
    except:
      await message.channel.send("Watch your language, "+"<@"+str(message.author.id)+">.")
    finally:
      await message.add_reaction("😡")
      if not botAdminSlur:
        await message.delete()
    return
  if str(message.content).lower() == "good bot":
    await message.channel.send(":D")
  if str(message.content).lower() == "woof":
    await message.channel.send("woof")

  if str(message.author.id) not in blacklist:
    await bot.process_commands(message)

@bot.command()
async def say(ctx,*args):
  if str(ctx.message.author) != "puptaco#3335":
    return
  await ctx.send(' '.join(args))
  await ctx.message.delete()
  adminLog("<@"+str(ctx.message.author.id)+">",str(ctx.message.content),"Say",ctx.message.guild,ctx.message.channel)

@bot.command()
async def logout(ctx):
  if str(ctx.message.author.id) not in botadmins:
    await ctx.send("You are not authorised to shut down this bot.")
    return
  await ctx.send("ZZZZZZZ")
  await ctx.message.delete()
  adminLog("<@"+str(ctx.message.author.id)+">",str(ctx.message.content),"Logout",ctx.message.guild,ctx.message.channel)
  await bot.close()


@bot.command()
async def uptime(ctx):
  print("Fetching time...")
  channel = bot.get_channel(771426494500044851)
  currenttime = time.time()
  timedifference = currenttime - starttime
  humantimedifference = format_timespan(timedifference)
  response = "I've been awake for "+str(humantimedifference)+" !"
  await ctx.send(response)
  await ctx.message.delete()

@bot.command()
async def servers(ctx):
  counter = 1
  embedVar = discord.Embed(title="All Servers", description="Below are all servers this bot is in:")
  for line in serverlist:
    embedVar.add_field(name="Server #"+str(counter), value=(str(line)), inline=False)
    counter = counter + 1
  embedVar.set_footer(text="Server list | Cybersaur")
  await ctx.send(embed=embedVar)
  await ctx.message.delete()

@bot.command()
async def botbl(ctx):
  counter = 1
  embedVar = discord.Embed(title="All Blacklisted Users", description="Below are all users who are blacklisted from using this bot. To appeal, please DM <@314394344465498122>.")       
  for line in blacklist:
    embedVar.add_field(name="User #"+str(counter), value=("<@"+str(line)+">"), inline=False)
    counter = counter + 1
  await ctx.send(embed=embedVar)
  await ctx.message.delete()

@bot.command()
async def admins(ctx):
  counter = 1
  embedVar = discord.Embed(title="All Bot Admins", description="Below are all Bot Admins, who may run certain mod-only commands.")       
  for line in botadmins:
    embedVar.add_field(name="Admin #"+str(counter), value=("<@"+str(line)+">"), inline=False)
    counter = counter + 1
  embedVar.set_footer(text="Bot Admins list | Cybersaur")
  await ctx.send(embed=embedVar)
  await ctx.message.delete()


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
async def dm(ctx,*args):
  if (str(ctx.author.id) not in botadmins):
    return
  userID = args[0]
  messagec = ' '.join(args[1:])
  user = await bot.fetch_user(int(userID))
  await user.send(messagec)
  tosend = "**📧 Sent to "+"<@"+str(userID)+"> :** "+messagec+"\nSent by: <@"+str(ctx.message.author.id)+">"
  channel = bot.get_channel(835175591862206524)
  await channel.send(tosend)
  tosend2 = "**📧 Sent to "+"<@"+str(userID)+"> :** "+messagec+"\nSent by: <@"+str(ctx.message.author)+">"
  await ctx.send(tosend2)
  await ctx.message.delete()

@bot.command()
async def bark(ctx):
  await ctx.send("bark")
  
@bot.command()
async def trelloban(ctx):
  if str(ctx.author.id) not in botadmins:
    await ctx.send("You are not authorised to perform this command.")
    return
  TRELLO_APP_KEY = os.getenv('TRELLO_APP_KEY')
  TOKEN = os.getenv('TOKEN')
  listID = "600ed147a982530da7b48b87"             #the id for your list 
  cardPos = "bottom"

  trello = TrelloApi(TRELLO_APP_KEY, TOKEN)
  await ctx.send("Warning: this command should only be used for T3B-ed members, or exploiter alts.")
  await ctx.send("What is the ROBLOX username of the T3B-ed user?")
  msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
  username = str(msg.content)

  RS = os.getenv('ROBLOSECURITY')
  await ctx.send("Fetching Roblox instance...")
  try:
    roblox = Client(RS)
  except:
    await ctx.send("Something broke trying to connect to Roblox!")
  try:
    robloxUser = await roblox.get_user_by_username(username)
  except:
    await ctx.send("Error getting user - maybe you gave an invalid user... 🤔")
    return
  userID = robloxUser.id

  userID = str(userID)

  cardName = username + ":"+userID

  await ctx.send("Sending request to Trello to add card.")
  reason = "Not specified."
  description = "__Discord-issued Trello Ban__\nIssuer: "+str(ctx.message.author.display_name)+"\nReason: "+reason
  newCard = trello.cards.new(cardName, idList=listID, desc=description, pos=cardPos)
  await ctx.send("Card created!\nCard details have been logged to the console.")
  print(newCard)    #above returns json details of the card just created
  await ctx.message.delete()
  adminLog("<@"+str(ctx.message.author.id)+">",str(ctx.message.content),"Trelloban",ctx.message.guild,ctx.message.channel)

@bot.command()
async def untrelloban(ctx):
  if str(ctx.author.id) not in botadmins:
    await ctx.send("You are not authorised to perform this command.")
    return
  TRELLO_APP_KEY = os.getenv('TRELLO_APP_KEY')
  TOKEN = os.getenv('TOKEN')
  listID = "600ed147a982530da7b48b87"             #the id for your list 
  cardPos = "bottom"
  trello = TrelloApi(TRELLO_APP_KEY, TOKEN)

  await ctx.send("What is the username of the user being untrellobanned?")
  msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
  username = str(msg.content)
  await ctx.send("Looking for cards with that name...")
  cardList = trello.lists.get_card(listID)
  for x in cardList:
    splity = x["name"].split(":")[0]
    if splity == username:
      print(x['id'])
      toSend = "Card containing the name '"+username+"' has been found, with the ID of: "+x['id']
      await ctx.send(toSend)
      await ctx.send("Deleting card...")
      trello.cards.delete(x['id'])
      await ctx.send("Card deleted!")
  await ctx.message.delete()
  adminLog("<@"+str(ctx.message.author.id)+">",str(ctx.message.content),"Untrelloban",ctx.message.guild,ctx.message.channel)


@bot.command()
async def about(ctx):
  embedVar = discord.Embed(title="<:triodoge:784565546036232192>", description="",color=0x03a1fc)
  embedVar.add_field(name="About", value="test", inline=False)
  embedVar.set_footer(text="About | Cybersaur")
  await ctx.send(embed=embedVar)

@bot.command()
async def blsearch(ctx,*args):
  toClear = []
  if str(ctx.message.channel.id) != "832652981659893820":
    await ctx.send("This command can only be used in <#832652981659893820>.")
    return
  name = ' '.join(args)
  name = str(name)
  RS = os.getenv('ROBLOSECURITY')
  try:
    roblox = Client(RS)
  except:
    await ctx.send("Something broke trying to connect to Roblox!")
  a = await ctx.send("Fetching Roblox user from username... <a:loading:841014732529598495>")
  try:
    user = await roblox.get_user_by_username(name)
  except:
    await ctx.send("Error getting user - maybe you gave an invalid user... 🤔")
    return
  b = await ctx.send("Found!")
  userId = str(user.id)
  robloxName = str(user.name)


  TRELLO_APP_KEY = os.getenv('TRELLO_APP_KEY')
  TOKEN = os.getenv('TOKEN')
  trello = TrelloApi(TRELLO_APP_KEY, TOKEN)
  listIDBans = "600ed147a982530da7b48b87"
  listIDBL = "6093ccae8f0a0a4e409fa1ce"

  c = await ctx.send("Fetching Trello lists... <a:loading:841014732529598495>")
  cardListBans = trello.lists.get_card(listIDBans)
  cardListBL = trello.lists.get_card(listIDBL)
  d = await ctx.send("Fetched!")
  
  e = await ctx.send("Checking Trelloban list... <a:loading:841014732529598495>")
  trelloBan = False


  for x in cardListBans:
    cardName = x["name"]
    if userId == cardName.split(":")[1]:
      trelloBan = True
  f = await ctx.send("Done!")
  g = await ctx.send("Checking blacklist... <a:loading:841014732529598495>")

  BLBan = False
  for x in cardListBL:
    cardName = x["name"]
    if userId == cardName.split(":")[0]:
      BLBan = True
      try:
        stage = (x["name"].split(":"))[1]
        reason = (x["name"].split(":"))[2]
        stage = str(stage)
      except:
        print("no")
  h = await ctx.send("Done!")
  
  embedVar = discord.Embed(title=robloxName,color=0x03a1fc)
  embedVar.add_field(name="Trellobanned?", value=(str(trelloBan)), inline=False)
  if BLBan == True:
    if (str(stage) == "1") or (str(stage) == "2") or (str(stage) == "3"):
      embedVar.add_field(name="Blacklisted?", value=(str(BLBan)), inline=False)
      embedVar.add_field(name="Blacklist Stage?", value=(str(stage)), inline=False)
      embedVar.add_field(name="Blacklist Reason?", value=(str(reason)), inline=False)
    else:
      embedVar.add_field(name="Blacklisted?", value=("False"), inline=False)
  else:
    embedVar.add_field(name="Blacklisted?", value=("False"), inline=False)
  try:
    badFriends = await checkFriends(name)
    print(badFriends)
    badFriendsStr = ""
    for x in badFriends:
      badUser = await roblox.get_user(int(x))
      badName = badUser.name
      badFriendsStr = badFriendsStr+badName+" "
    badFriendsStr = "```"+badFriendsStr+"```"
    embedVar.add_field(name="Blacklisted Friends", value=(str(badFriendsStr)), inline=False)
  except:
    print("error getting bad friends")
  embedVar.set_footer(text="Requested by "+str(ctx.message.author.display_name))
  await ctx.send(embed=embedVar)

  for msg in [a,b,c,d,e,f,g,h]:
    await msg.delete()
  await ctx.message.delete()
  
@bot.command()
async def poll(ctx,*args):
  embed = discord.Embed(title=' '.join(args),description=f'Sent by: {ctx.message.author}',color=0x03a1fc)  ## Added embed instead of message.
  embed.set_footer(text="Poll | Cybersaur")
  msg = await ctx.send(embed=embed)
  await msg.add_reaction("✅")
  await msg.add_reaction("❌") 

@bot.command()
async def floppa(ctx,*args):
  await ctx.send(random.choice([
    "https://tenor.com/btvbY.gif",
    "https://tenor.com/btFVt.gif",
    "https://tenor.com/bthES.gif",
    "https://tenor.com/bDsKF.gif",
    "https://tenor.com/bC7yO.gif"
  ]))

@bot.command()
async def granks(ctx,*args):
  if str(ctx.message.author.id) not in botadmins:
    await ctx.send("You are not authorised to run this command.")
    return
  idGroup = ' '.join(args)
  idGroup = int(idGroup)
  await ctx.send("Fetching group ranks.\nThis will take a few seconds - assume the command broke if it took longer, and try again in a couple of seconds.")
  RS = os.getenv('ROBLOSECURITY')
  roblox = Client(RS)
  await asyncio.sleep(2)
  name = "pee"
  try:
    await asyncio.sleep(2)
    groupObj = await roblox.get_group(idGroup)
    name = groupObj.name
    await asyncio.sleep(2)
    roles = await groupObj.get_roles()

  except Exception as e:
    e = "Error: "+"`"+str(e)+"`"
    await ctx.send(str(e))
    try:
      await ctx.send("Failed. Retrying... (1/3)")
      await asyncio.sleep(2)
      groupObj = await roblox.get_group(idGroup)
      name = groupObj.name
      await asyncio.sleep(2)
      roles = await groupObj.get_roles()

    except Exception as e:
      e = "Error: "+"`"+str(e)+"`"
      await ctx.send(str(e))
      try:
        await ctx.send("Failed. Retrying... (2/3)")
        await asyncio.sleep(2)
        groupObj = await roblox.get_group(idGroup)
        name = groupObj.name
        await asyncio.sleep(2)
        roles = await groupObj.get_roles()
      
      except Exception as e:
        e = "Error: "+"`"+str(e)+"`"
        await ctx.send(str(e))
        try:
          await ctx.send("Failed. Retrying... (3/3)")
          await asyncio.sleep(2)
          groupObj = await roblox.get_group(idGroup)
          name = groupObj.name
          await asyncio.sleep(2)
          roles = await groupObj.get_roles()

        except Exception as e:
          e = "Error: "+"`"+str(e)+"`"
          await ctx.send(str(e))
          await ctx.send("Couldn't get group ranks.")
          return
  print(groupObj.name)
  embedVar = discord.Embed(title=name,color=0x03a1fc)
  for x in roles:
    name = (x.name)
    val = (x.rank)
    embedVar.add_field(name=x.name, value=(x.rank), inline=False)
  embedVar.set_footer(text="Group Ranks | Cybersaur")    
  await ctx.send(embed=embedVar)

@bot.command()
async def dontwoof(ctx):
  await ctx.send("https://cdn.discordapp.com/attachments/657008895776129028/771842764894896138/Woof.mov")
  await ctx.message.delete()

@bot.command()
async def bloxsearch(ctx,*args):
  if str(ctx.message.author.id) not in botadmins:
    await ctx.send("You are not authorised to run this command.")
    return

  baseURL = "https://api.blox.link/v1/user/"
  discID = args[0] # the discord id provided
  discID = str(discID)
  reqURL = baseURL + discID

  r = requests.get(reqURL)
  r = r.json() # make it accessible as a dict

  if r["status"] == "error": # if the request failed
    errorText = r["error"]
    await ctx.send("This command failed.\nError reason is:")
    toSend = "`"+errorText+"`"
    await ctx.send(toSend)
  else:
    link = "https://www.roblox.com/users/"+r["primaryAccount"]+"/profile"

    embedVar = discord.Embed(title="Bloxlink Lookup", description="",color=0x03a1fc)
    
    embedVar.add_field(name="Discord User", value="<@"+str(discID)+">", inline=False)
    RS = os.getenv('ROBLOSECURITY')
    roblox = Client(RS)
    user = await roblox.get_user(int(r["primaryAccount"]))
    currentName = user.name
    embedVar.add_field(name="Username", value=currentName, inline=False)
    embedVar.add_field(name="Profile Link", value=link, inline=False)
    await ctx.send(embed=embedVar)

keep_alive.keep_alive()
bot.run(TOKEN)