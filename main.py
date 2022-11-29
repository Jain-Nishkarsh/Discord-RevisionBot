import discord
import os
import pytz
import time
import datetime as dt
from discord.ext import tasks,commands
import ImportImages
import random
from keep_alive import keep_alive

tz = pytz.timezone('Asia/Calcutta')
Bot_Token = os.environ['TOKEN']
client = commands.Bot(command_prefix='!')
quesGoing = False
currQuesAns = None
currSwTime = 0

QuesDirectoryList = []
RevThingDirectoryList = []
valid_Ans = ['A','B','C','D','a','b','c','d']

RevTime = ['9:0','12:0','14:0','16:0','18:0','20:0','22:0','24:0']

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  ImportImages_Now.start()
  Send_RevThing.start()

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content == 'Hello':
    await message.channel.send('Hello user!')

  global quesGoing
  if quesGoing:
    if message.content in valid_Ans:
      quesGoing=False
      global currQuesAns
      if currQuesAns == (message.content).upper():
        global currSwTime
        ebd = discord.Embed(title='You are CORRECT!',
                           description='You got it in '+str(dt.timedelta(seconds=currSwTime)),
                           color = discord.Color.green())
        await message.channel.send(embed = ebd)
      else:
        ebd = discord.Embed(title='You got it WRONG!',
                           description='Your attempt took '+str(dt.timedelta(seconds=currSwTime))+
                            '\n The correct ans is '+currQuesAns,
                           color = discord.Color.red())
        await message.channel.send(embed=ebd)
    else:
      await message.channel.send('Invalid Response!')
      
  await client.process_commands(message)    
    
    
@tasks.loop(hours=24)
async def ImportImages_Now():
  ImportImages.As_Function()  
  QuesNameList = os.listdir('Questions')
  for i in QuesNameList:
    QuesDirectoryList.append('Questions/{0}'.format(i))
    
  RevThingNameList = os.listdir('RevisionThings')
  for i in RevThingNameList:
    RevThingDirectoryList.append('RevisionThings/{0}'.format(i))
                                                            

@tasks.loop(seconds=60)
async def Send_RevThing():
  channel = client.get_channel(946391592841936931)
  if (str(dt.datetime.now(tz).hour)+':'+str(dt.datetime.now(tz).minute)) in RevTime:
    print('Sending')
    await channel.send('Revision Time @everyone',file = discord.File(random.choice(RevThingDirectoryList)))

@client.command(name='SayHi')
async def SayHi(ctx):
  await ctx.send(file=discord.File('ObiWanHelloThere.png'))

@client.command()
async def Revise(ctx):
  print('---prompted---')
  await ctx.send(file = discord.File(random.choice(RevThingDirectoryList)))

@client.command(name='Question')
async def RandQuestion(ctx):
  print('---prompted---')
  Ques = {}
  QuesNameList = os.listdir('Questions')
  for i in QuesNameList:
    ans = (i.split('--')[1]).split('.')[0]
    Ques[i] = ans
  x = random.choice(QuesDirectoryList)
  global currQuesAns
  currQuesAns = Ques[x.split('/')[1]]
  global quesGoing
  quesGoing = True
  await ctx.send('Here you go!',file = discord.File(x))
  await Stopwatch(ctx)

async def Stopwatch(ctx):
  global currSwTime
  currSwTime = 1
  embed_ = discord.Embed(title=str(dt.timedelta(seconds=currSwTime)),color=discord.Color.blurple())
  msg = await ctx.send(embed=embed_)
  while quesGoing:
    time.sleep(1)
    currSwTime += 1
    embed_new = discord.Embed(title=str(dt.timedelta(seconds=currSwTime)),color=discord.Color.blurple())
    await msg.edit(embed=embed_new)

@client.command(name='StopStopwatch')
async def StopStopwatch(ctx):
  global quesGoing
  quesGoing = False

@client.command(name='UpdateDrive')
async def UpdateDrive(ctx):
  print('---prompted---')
  ImportImages_Now.start()
  await ctx.send('Drive Updated!')

keep_alive()
client.run(Bot_Token)