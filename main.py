import os
import discord
import random
import ducoapi

client = discord.Client()

p_msg = [
    'Why you disturbing me!1!1!1!',
    'Go away',
    'UGGGGGGGG',
    'im trying to work here!',
    'you wastin my time bru'
  ]


@client.event
async def on_ready():
  print("We are logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  mention = f'<@!{client.user.id}>'
  
  
  
  if message.author == client.user:
    return

  if mention in message.content:
    res = random.choice(p_msg)
    await message.channel.send(res)
  if message.content.startswith('$hello'):
    await message.channel.send("Hello!")

  if message.content.startswith('$price'):
    pri = ducoapi.get_duco_price()
    fpri = "Duino-Coin current price: $", pri
    await message.channel.send(pri)
  if message.content.startswith("$help"):
    await message.channel.send("Prefix: $ \n Commands: \n -help \n -price \n -hello")

  


client.run(os.getenv('TOKEN'))

