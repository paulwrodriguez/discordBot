
import requests
import json
import discord
import threading
import asyncio

continue_meme_loop_flag = {}

async def handle(message):
  print (str(threading.get_ident()))
  count = 1
  try : 
    count_string = message.content.split(" ")[1]
    if count_string.isnumeric():
      count = int(count_string)
      if count > 10 :
        await message.channel.send('Nice try. I am not going to search for {0} memes. But since your desires do not go unnoticed, I will grant you 10 memes. Enjoy'.format(str(count)))
        await asyncio.sleep(8)
        count = 10
      elif count < 0:
        count = 1
    else :
      count = 1
  except:
    count = 1
  for i in range(0, count) :
    print (str(threading.get_ident()))
    await message.channel.send("loading meme...")
    await asyncio.sleep(1)
    await generate_meme(message)
  await message.channel.send("Done. Enjoyed?")

def get_meme() :
  response = requests.get("https://meme-api.herokuapp.com/gimme")
  json_data = json.loads(response.text);
  return json_data

async def generate_meme(message):
  meme = get_meme()
  embedVar = discord.Embed(
            title=meme["title"],  
            color=0x00ff00, 
            url =meme["postLink"],
            type="rich", 
  author=meme["author"], 
  provider=meme["postLink"], 
  footer=meme["postLink"])
  embedVar.set_image(url=meme["url"])
  await message.channel.send(embed=embedVar)

async def generate_meme_loop(message):
  global continue_meme_loop_flag
  continue_meme_loop_flag[message.channel.id] = True

  try : 
    count_string = message.content.split("$gen meme")[1]
    if count_string == '' :
      count = 1
    elif count_string.strip().isnumeric():
      count = int(count_string)
      if count > 30 :
        await message.channel.send('Settle down there big boy, how about we meet in the middle and settle for 30 minutes ehh?')
        await asyncio.sleep(8)
        count = 30
      elif count < 0:
        count = 1
    else :
      await asyncio.sleep(2)
      await message.channel.send('...')
      await asyncio.sleep(2)
      await message.channel.send('...')
      await asyncio.sleep(2)
      await message.channel.send('...')
      await asyncio.sleep(2)
      await message.channel.send('Who the hell told you how to count?? Please stand up and InTrOdUcE \'{0}\' to the class  '.format(str(count_string).strip()))
      await asyncio.sleep(8)
      await message.channel.send('😕')
      await asyncio.sleep(6)
      await message.channel.send('I\'ll just assume you mean 1')
      await asyncio.sleep(2)
      await message.channel.send('Loading...')
      await asyncio.sleep(2)
      count = 1
  except:
    count = 1

  while continue_meme_loop_flag[message.channel.id]: 
    await generate_meme(message)
    await asyncio.sleep(count * 60)
  del continue_meme_loop_flag[message.channel.id]

async def end_meme_loop(message):
  global continue_meme_loop_flag
  continue_meme_loop_flag[message.channel.id] = False