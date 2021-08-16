import os
# python3 -m pip install python-dotenv
from dotenv import load_dotenv
# python3 -m pip install discord-py
import discord
import random
import json
# python3 -m pip install requests
import requests
from datetime import datetime
import aiohttp
import asyncio

load_dotenv()
client = discord.Client()

TOKEN = os.getenv('TOKEN')
PREFIX = "$"
REPLIES_URI = 'utils/replies.json'
BALANCES_API = "https://server.duinocoin.com:5000/balances/"
PRICE_API = "https://server.duinocoin.com/api.json"

with open(REPLIES_URI, "r") as replies_file:
    duino_stats_replies = json.load(replies_file)


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="with your duino-coin"
        )
   )

@client.event
async def on_message(message):
    mention = f'<@!{client.user.id}>'

    help_embed = discord.Embed(
        title="List of available commands",
        color=discord.Color.gold(),
        timestamp=datetime.utcnow()
    )
    help_embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.avatar_url
    )
    help_embed.set_footer(
        text=client.user.name,
        icon_url=client.user.avatar_url
    )
    help_embed.set_thumbnail(
        url=client.user.avatar_url
    )

    help_embed.add_field(
        name="General",
        value="""\
        `{p}balance <DUCO username>` - Get user balance
        `{p}help` - Show this help message
        """.replace("{p}", PREFIX),
        inline=False
    )
    help_embed.add_field(
        name="Admin",
        value="""\
        `{p}say <tosay>` - Make the bot say something
        """.replace("{p}", PREFIX),
        inline=False
    )

    
    if message.author == client.user:
        return

    if mention in message.content:
        response = random.choice(duino_stats_replies)
        await message.channel.send(
            message.author.mention
            + ", "
            + response
        )

    if message.content.startswith(PREFIX):
        command = message.content.strip(PREFIX).split(" ")

        if command[0] == "say":
            if message.author.guild_permissions.administrator:
                command[0] = ""
                await message.delete()
                await message.channel.send(" ".join(command))
            else:
                await message.channel.send(
                    ":no_entry: You dont't have the permission to do that!")

        if command[0] == "balance":
            if not command[1]:
                await message.channel.send("Provide a username first")
            else:
                try:
                    print("Getting balance api")
                    async with aiohttp.ClientSession() as session:
                        async with session.get(BALANCES_API
                                               + command[1]) as resp:
                            response = json.loads(await resp.text())
                    #response = {"result": {"balance": 69420.42069}, "success": True}

                    print("Got balance api")

                    if not response["success"]:
                        message.channel.send("This user doesn't exist")

                    else:
                        balance = float(response["result"]["balance"])

                        try:
                            print("Getting price api")
                            async with aiohttp.ClientSession() as session:
                                async with session.get(PRICE_API) as resp:
                                    response_price = json.loads(
                                        await resp.text())
                            #response_price = {"Duco price": 0.0065}
                            print("Got price api")

                            price = float(response_price["Duco price"])
                            balance_in_usd = balance * price

                            print("Sending embed")
                            embed = discord.Embed(
                                description="**"
                                + str(command[1])
                                + "**'s balance: **"
                                + str(balance)
                                + "** <:duco:876588980630618152>"
                                + " ($"
                                + str(round(balance_in_usd, 4))
                                + ")",
                                color=discord.Color.gold(),
                                timestamp=datetime.utcnow()
                            )
                            embed.set_author(
                                name=message.author.display_name,
                                icon_url=message.author.avatar_url
                            )
                            embed.set_footer(
                                text=client.user.name,
                                icon_url=client.user.avatar_url
                            )
                            await message.channel.send(embed=embed)

                        except Exception as e:
                            await message.channel.send(
                                "`ERROR` Can't fetch the price: "
                                + str(e)
                            )
                except Exception as e:
                    await message.channel.send(
                        "`ERROR` Can't fetch the balances: "
                        + str(e)
                    )

        if command[0] == "price":
            ducoapi.Getducoprice
            await message.channel.send("Duino-Coin current price: $", )

        if command[0] == "help":
            await message.channel.send(embed=help_embed)

        if command[0] == "mcip":
            await message.channel.send(
                """"
                DuinoCraft:
                Server Version: 1.16-1.17.1
                IP: play.duinocraft.com
                Earn Duino-Coin just by playing!
                """
            )



          

client.run(TOKEN)
