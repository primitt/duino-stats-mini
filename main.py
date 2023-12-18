# python3 -m pip install pillow
import socketserver
import http.server
from PIL import Image, ImageDraw, ImageFont
import os

# python3 -m pip install python-dotenv
from dotenv import load_dotenv

# python3 -m pip install discord-py
import discord

# python3 -m pip install requests
import requests

import random
import json
from datetime import datetime
import aiohttp
import asyncio
import re
import traceback
from time import sleep

from io import BytesIO
import base64

from time import time

intents = discord.Intents.default()
#intents.typing = True
#intents.presences = True
#intents.messages = True
#intents.message_content = True

load_dotenv()
client = discord.Client(intents=intents)

second_limit = 3
allowed_channels = [678301439835111455, 819146399764840448]
EM_TRUE = "<:true:709441577503817799>"
EM_FALSE = "<:nop:692067038453170283>"
EM_WARNING = "⚠"
TOKEN = os.getenv('TOKEN')
PREFIX = "+"
REPLIES_URI = 'utils/replies.json'
USER_API = "https://server.duinocoin.com/users/"
PRICE_API = "https://server.duinocoin.com/api.json"
NODE_API = "https://server.duinocoin.com/all_pools"

headers = {
    "Authorization": "Client-ID " + os.getenv('IMGUR_TOKEN'),
}

async def is_reply(message):
    if message.reference:
        ref = await message.channel.fetch_message(message.reference.message_id)
        if ref:
            if ref.author == client.user:
                return True
    return False

with open(REPLIES_URI, "r") as replies_file:
    duino_stats_replies = json.load(replies_file)

duino_stats_pings = [
    "hey",
    "stop ignoring me",
    "plz respond :(",
    "hi",
    "!!!!",
    "task for you",
    "hiya",
    "o.o",
    ":eyes:",
    ":watermelon"
]

cards = [
    "utils/card_1.png",
    "utils/card_2.png"
]

last_uses = {}


def generate_card(nick: str, duco: float, discord_nick: str):
    try:
        image = Image.open(random.choice(cards))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('utils/Lato-Black.ttf', size=26)
        font2 = ImageFont.truetype('utils/Lato-Regular.ttf', size=20)
        font3 = ImageFont.truetype('utils/Lato-Regular.ttf', size=18)
        color = "#0a0a0a"

        nick = str(nick)+"'s balance"
        draw.text((155, 84), str(nick), fill=color, font=font2)
        duco_str = str(round(duco, 3)) + " DUCO"
        draw.text((155, 106), duco_str, fill=color, font=font)
        duco_str = str(round(duco, 3)) + " DUCO"
        draw.text((155, 138), str(discord_nick), fill=color, font=font3)

        # image.save('utils/out.png')

        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue())
        now = datetime.now()
        data = {'image': img_str, 'title': f"{nick}'s balance {now}"}
        r = requests.post("https://api.imgur.com/3/image",
                          data=data, headers=headers).json()["data"]
        print(r)
        return r["link"]
    except Exception as e:
        print(e)
        return "https://upload.wikimedia.org/wikipedia/commons/c/ca/1x1.png"


def prefix(symbol: str, value: float, accuracy=2):
    """
    Input: symbol to add, value 
    Output rounded value with scientific prefix as string
    """
    if value >= 900000000:
        prefix = " G"
        value = value / 1000000000
    elif value >= 900000:
        prefix = " M"
        value = value / 1000000
    elif value >= 900:
        prefix = " k"
        value = value / 1000
    else:
        prefix = " "
    return (
        str(round(value, accuracy))
        + str(prefix)
        + str(symbol))


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))
    await client.change_presence(
        activity=discord.Game(
            name="with your duinos | " + PREFIX + "help"))

    #avatar_path = 'christmas.png'
    #avatar = open(avatar_path, 'rb').read()
    #await client.user.edit(avatar=avatar)


@client.event
async def on_message(message):
    global last_uses

    help_embed = discord.Embed(
        title="List of available commands",
        color=discord.Color.gold(),
        timestamp=datetime.utcnow())
    help_embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.avatar_url)
    help_embed.set_footer(
        text=client.user.name,
        icon_url=client.user.avatar_url)
    help_embed.set_thumbnail(
        url=client.user.avatar_url)
    help_embed.add_field(
        name="General",
        value="""\
        `{p}about - Show info about Duino Stats Mini`
        `{p}balance <DUCO username>` - Show user DUCO balance *[b, bal]*
        `{p}mbalance <XMG username>` - Show user XMG balance *[m, mbal]*
        `{p}price` - Show current DUCO prices
        `{p}help` - Show this help message
        ~~`{p}faucets` - Show Duino-Coin faucets~~
        `{p}profile` - Show info about your profile *[p]*
        `{p}nodes` - Show mining nodes status *[server, servers]*
        `{p}statistics` - Show network stats *[stats]*
        ~~`{p}invite` - Invite Duino Stats Mini to your server~~
        """.replace("{p}", PREFIX),
        inline=False
    )
    help_embed.add_field(
        name="Admin",
        value="""\
        `{p}say <tosay>` - Make the bot say something
        """.replace("{p}", PREFIX),
        inline=False)

    if message.author == client.user:
        return

    #if message.guild.id != 677615191793467402:
    #    try:
    #        link = await message.channel.create_invite(max_age=300)
    #    except:
    #        link = "No permissions"
    #    print(message.guild.name, message.author, message.content, link, sep=" | ")

    #if str(client.user.id) in message.content or await is_reply(message):
        #with message.channel.typing():
        #    response = random.choice(duino_stats_replies)
        #    await message.channel.send(
        #        message.author.mention
        #        + ", "
        #        + response)

    if str(message.author.mention) == "<@!617037497574359050>":
        if message.guild.id == 677615191793467402:
            if not message.channel.id in allowed_channels:
                await message.delete()

    if str(message.author.mention) == "<@!270904126974590976>":
        if message.guild.id == 677615191793467402:
            if not message.channel.id in allowed_channels:
                await message.delete()

    if message.content.startswith("$") or message.content.startswith("pls "):
        if message.guild.id == 677615191793467402:
            if not message.author.guild_permissions.administrator:
                if not message.channel.id in allowed_channels:
                    with message.channel.typing():
                        bot_msg = await message.channel.send(
                            message.author.mention
                            + ", use the <#678301439835111455> channel for bot commands!")
                    await asyncio.sleep(5)
                    await message.delete()
                    await bot_msg.delete()

    elif message.content.lower().startswith("how much"):
        if message.content.lower().startswith("how much duco is") and message.content.lower().endswith("usd"):
            with message.channel.typing():
                amount = re.findall(r'\d+', message.content)[0]
                async with aiohttp.ClientSession() as session:
                    async with session.get(PRICE_API) as resp:
                        response_price = json.loads(await resp.text())
                price = response_price["Duco price"]
                value = round(float(amount) / float(price), 4)
                await message.channel.send(f"{amount} USD is currently equal to {value} DUCO")
        elif "duco" in message.content.lower():
            with message.channel.typing():
                amount = re.findall(r'\d+', message.content)[0]
                async with aiohttp.ClientSession() as session:
                    async with session.get(PRICE_API) as resp:
                        response_price = json.loads(await resp.text())
                price = response_price["Duco price"]
                value = round(float(amount) * float(price), 4)
                await message.channel.send(f"{amount} DUCO is currently worth {value} USD")

    elif message.content.startswith(PREFIX) or "<@876506340112076801> " in message.content:
        cont = True
        command = message.content.strip(PREFIX).split(" ")
        #command = message.content.strip("<@876506340112076801> ").split(" ")

        try:
            secs = round(time() - last_uses[message.author.mention], 2)
            print(message.author.display_name,
                  last_uses[message.author.mention], secs)
        except Exception as e:
            secs = second_limit

        if secs < second_limit:
            with message.channel.typing():
                bot_msg = await message.channel.send(
                    message.author.mention
                    + f", you're using the bot commands too often, try again in {round(second_limit-secs, 1)}s!")
            return
        last_uses[message.author.mention] = time()

        if message.guild.id == 677615191793467402 and 1 == 2:
            if not message.author.guild_permissions.administrator:
                if not message.channel.id in allowed_channels:
                    cont = False
                    with message.channel.typing():
                        bot_msg = await message.channel.send(
                            message.author.mention
                            + ", use the <#678301439835111455> channel for bot commands!")
                    await asyncio.sleep(5)
                    await message.delete()
                    await bot_msg.delete()

        if cont:
            if command[0] == "say":
                with message.channel.typing():
                    if message.author.guild_permissions.administrator:
                        command[0] = ""
                        await message.delete()
                        await message.channel.send(" ".join(command))
                    else:
                        await message.channel.send(
                            ":no_entry: You dont't have the permission to do that!")

            elif (command[0] == "balance"
                  or command[0] == "bal"
                    or command[0] == "b"):
                with message.channel.typing():
                    try:
                        _ = command[1]
                        try:
                            async with aiohttp.ClientSession() as session:
                                async with session.get(USER_API
                                                       + command[1]) as resp:
                                    response = json.loads(await resp.text())

                            if not response["success"]:
                                await message.channel.send(response["message"])

                            else:
                                balance = float(
                                    response["result"]["balance"]["balance"])
                                miners_a = response["result"]["miners"]
                                verified = response["result"]["balance"]["verified"]
                                created = response["result"]["balance"]["created"]
                                stake_amount = response["result"]["balance"]["stake_amount"]

                                try:
                                    miners = {}
                                    for miner in miners_a:
                                        miner_wid = miner["wd"]

                                        if not miner_wid:
                                            miner_wid = random.randint(0, 2811)

                                        miner_h = miner["hashrate"]
                                        miner_r = miner["rejected"]
                                        miner_a = miner["accepted"]

                                        if not miner_wid in miners:
                                            miners[miner_wid] = miner
                                            miners[miner_wid]["threads"] = 1
                                            continue
                                        elif miner_wid in miners:
                                            miners[miner_wid]["hashrate"] += miner_h
                                            miners[miner_wid]["rejected"] += miner_r
                                            miners[miner_wid]["accepted"] += miner_a
                                            miners[miner_wid]["threads"] += 1
                                            continue
                                except Exception:
                                    print(traceback.format_exc())

                                try:
                                    async with aiohttp.ClientSession() as session:
                                        async with session.get(PRICE_API) as resp:
                                            response_price = json.loads(
                                                await resp.text())

                                    price = response_price["Duco price"]
                                    balance_in_usd = price * balance

                                    embed = discord.Embed(
                                        title=str(
                                            command[1]+"'s Duino-Coin account"),
                                        color=discord.Color.gold(),
                                        timestamp=datetime.utcnow())
                                    embed.set_author(
                                        name=message.author.display_name,
                                        icon_url=message.author.avatar_url)
                                    embed.set_footer(
                                        text=client.user.name,
                                        icon_url=client.user.avatar_url)

                                    embed.add_field(
                                        name="<:duco_logo:832307063395975218> Balance",
                                        value=str(balance)
                                        + " DUCO"
                                        + " ($"
                                        + str(round(balance_in_usd, 4))
                                        + ")",
                                        inline=True)

                                    embed.add_field(
                                        name=":handshake: Stake",
                                        value=str(f"{stake_amount} DUCO"),
                                        inline=True)

                                    embed.add_field(
                                        name=":question: Verified account",
                                        value=str(verified).capitalize(),
                                        inline=True)

                                    embed.add_field(
                                        name=":calendar: Created",
                                        value=str(created).capitalize(),
                                        inline=True)

                                    total_hashrate = 0
                                    if not miners:
                                        miner_str = "No miners running on this account"
                                    else:
                                        miner_str = ""
                                        i = 0
                                        for miner in miners:
                                            total_hashrate += miners[miner]["hashrate"]

                                            if miners[miner]["identifier"] != "None":
                                                miner_str += (
                                                    f"**{miners[miner]['identifier']}**"
                                                    + f" ({miners[miner]['software']})")
                                            else:
                                                miner_str += miners[miner]["software"]

                                            miner_str += (
                                                " - **"
                                                + str(int(miners[miner]["accepted"]))
                                                + "/"
                                                + str(int(miners[miner]["accepted"]) +
                                                      int(miners[miner]["rejected"]))
                                                + "** acc. shares, **"
                                                + str(prefix("H/s", int(miners[miner]["hashrate"])))
                                                + "**")

                                            if miners[miner]["threads"] > 1:
                                                miner_str += f" ({miners[miner]['threads']} threads)"

                                            miner_str += "\n"

                                            i += 1
                                            if i >= 10:
                                                miner_str += ("and "
                                                              + str(len(miners)-i)
                                                              + " more miners...")
                                                break

                                    embed.add_field(
                                        name=":pick: Miners ("
                                        + str(len(miners))
                                        + ") - "
                                        + str(prefix("H/s", total_hashrate))
                                        + " total",
                                        value=miner_str,
                                        inline=False)

                                    try:
                                        embed.set_image(
                                            url=generate_card(command[1], balance, message.author.display_name))
                                    except:
                                        pass

                                    await message.channel.send(embed=embed)

                                except Exception as e:
                                    print(traceback.format_exc())
                                    await message.channel.send(
                                        "`ERROR` Can't fetch user data")
                        except Exception as e:
                            await message.channel.send(
                                "`ERROR` Can't fetch user balance")
                    except IndexError:
                        await message.channel.send(
                            "Provide a username first (e.g. {}bal revox)"
                            .format(PREFIX))

            elif command[0] == "faucets":
                await message.channel.send("Command disabled")
                return
                embed = discord.Embed(
                    title="Duino-Coin faucets",
                    color=discord.Color.blue(),
                    timestamp=datetime.utcnow())
                embed.set_author(
                    name=message.author.display_name,
                    icon_url=message.author.avatar_url)
                embed.set_footer(
                    text=client.user.name,
                    icon_url=client.user.avatar_url)

                embed.add_field(
                    name="Techcrafter's faucet",
                    value="**0.2 DUCO daily**\n*https://techcrafter.de/faucet/*",
                    inline=False)
                embed.add_field(
                    name="Pastel's faucet",
                    value="**0.08-0.7 DUCO daily**\n*http://pastelindustries.usermd.net*",
                    inline=False)
                embed.add_field(
                    name="Lukas' dashboard faucet",
                    value="**~0.01 DUCO daily**\n*https://duco.sytes.net*",
                    inline=False)
                embed.add_field(
                    name="Amogus faucet",
                    value="**0.0001-8 DUCO every 15 minutes**\n*https://duco-faucet.pcgeek.pl*",
                    inline=False)
                embed.add_field(
                    name="duino-faucet.com",
                    value="**1-5 DUCO every hour**\n*https://duino-faucet.com*",
                    inline=False)

                await message.channel.send(embed=embed)

            elif (command[0] == "mbalance"
                  or command[0] == "mbal"
                    or command[0] == "m"):
                with message.channel.typing():
                    try:
                        _ = command[1]
                        try:
                            async with aiohttp.ClientSession() as session:
                                async with session.get("https://magi.duinocoin.com/balances/"
                                                       + command[1]) as resp:
                                    response = json.loads(await resp.text())

                            if not response["success"]:
                                await message.channel.send("This user doesn't exist")

                            else:
                                balance = float(
                                    response["result"]["balance"]["balance"])
                                staked_balance = response["result"]["balance"]["staked_balance"]
                                address = response["result"]["balance"]["address"]

                                try:
                                    price = response["result"]["price"]["max"]
                                    balance_in_usd = price * balance

                                    embed = discord.Embed(
                                        title=str(
                                            command[1]+"'s Coin Magi account"),
                                        color=discord.Color.blue(),
                                        timestamp=datetime.utcnow())
                                    embed.set_author(
                                        name=message.author.display_name,
                                        icon_url=message.author.avatar_url)
                                    embed.set_footer(
                                        text=client.user.name,
                                        icon_url=client.user.avatar_url)

                                    embed.add_field(
                                        name=":hash: Wallet address",
                                        value=address,
                                        inline=False)

                                    embed.add_field(
                                        name="<:magi:896454859778314250> Balance",
                                        value=str(balance)
                                        + " XMG"
                                        + " ($"
                                        + str(round(balance_in_usd, 4))
                                        + ")",
                                        inline=False)

                                    embed.add_field(
                                        name=":handshake: Staked balance",
                                        value=f"{staked_balance} XMG",
                                        inline=False)

                                    await message.channel.send(embed=embed)

                                except Exception as e:
                                    print(traceback.format_exc())
                                    await message.channel.send(
                                        "`ERROR` Can't fetch user data")
                        except Exception as e:
                            print(traceback.format_exc())
                            await message.channel.send(
                                "`ERROR` Can't fetch user balance")
                    except IndexError:
                        await message.channel.send(
                            "Provide a username first (e.g. {}bal revox)"
                            .format(PREFIX))

            elif command[0] == "price":
                with message.channel.typing():
                    async with aiohttp.ClientSession() as session:
                        async with session.get(PRICE_API) as resp:
                            response_price = json.loads(
                                await resp.text())

                    price_xmg = float(response_price["Duco price"])
                    price_bch = float(response_price["Duco price BCH"])
                    price_trx = float(response_price["Duco price TRX"])
                    price_nano = float(response_price["Duco price NANO"])

                    price_justswap = float(
                        response_price["Duco SunSwap price"])
                    price_pancake = float(
                        response_price["Duco PancakeSwap price"])
                    price_ubeswap = float(response_price["Duco UbeSwap price"])
                    price_sushi = float(response_price["Duco SushiSwap price"])

                    embed = discord.Embed(
                        #description=("Please keep in mind that price "
                        #             + "on the chart is updated every 1 day"),
                        color=discord.Color.gold(),
                        timestamp=datetime.utcnow())
                    embed.set_author(
                        name=message.author.display_name,
                        icon_url=message.author.avatar_url)
                    embed.set_footer(
                        text=client.user.name,
                        icon_url=client.user.avatar_url)
                    embed.add_field(
                        name="<:magi:876963168218394644> DUCO Exchange (XMG)",
                        value=f"${price_xmg:.6f}",
                        inline=True)
                    embed.add_field(
                        name="<:bitcoincash:876963784491671622> DUCO Exchange (BCH)",
                        value=f"${price_bch:.6f}",
                        inline=True)
                    embed.add_field(
                        name="<:tron:876962726000349204> DUCO Exchange (TRX)",
                        value=f"${price_trx:.6f}",
                        inline=True)
                    embed.add_field(
                        name="<:nano:876962697730752552> DUCO Exchange (NANO)",
                        value=f"${price_nano:.6f}",
                        inline=True)
                    embed.add_field(
                        name=":sunny: SunSwap",
                        value=f"${price_justswap:.6f}",
                        inline=True)
                    embed.add_field(
                        name=":pancakes: PancakeSwap",
                        value=f"${price_pancake:.6f}",
                        inline=True)
                    embed.add_field(
                        name=":sushi: SushiSwap",
                        value=f"${price_sushi:.6f}",
                        inline=True)
                    embed.add_field(
                        name=":cucumber: UbeSwap",
                        value=f"${price_ubeswap:.6f}",
                        inline=True)
                    embed.add_field(
                        name=":person_standing: otc-trading",
                        value="[Duino-Coin Discord](https://discord.gg/duinocoin)",
                        inline=True)
                    #embed.set_image(
                    #    url=f"https://server.duinocoin.com/prices.png?v={random.randint(0, 100)}")

                    await message.channel.send(embed=embed)

            elif (command[0] == "stats" or command[0] == "statistics"):
                with message.channel.typing():
                    async with aiohttp.ClientSession() as session:
                        async with session.get(PRICE_API) as resp:
                            response = json.loads(
                                await resp.text())

                    total_hashrate = response["Pool hashrate"]
                    users = str(response["Registered users"])
                    net_wattage = response["Net energy usage"]
                    difficulty = str(response["Current difficulty"])
                    circulation = str(round(response["All-time mined DUCO"]))
                    duco_price = "$" + str(response["Duco price"])
                    market_cap = "$" + str(
                        round(response["Duco price"] *
                              response["All-time mined DUCO"], 2))

                    embed = discord.Embed(
                        title="Duino-Coin Statistics",
                        color=discord.Color.gold(),
                        timestamp=datetime.utcnow())
                    embed.set_author(
                        name=message.author.display_name,
                        icon_url=message.author.avatar_url)
                    embed.set_footer(
                        text=client.user.name,
                        icon_url=client.user.avatar_url)
                    embed.add_field(
                        name=":pick: Net hashrate",
                        value=total_hashrate,
                        inline=True)
                    embed.add_field(
                        name=":evergreen_tree: Net energy usage",
                        value=net_wattage,
                        inline=True)
                    embed.add_field(
                        name=":people_holding_hands: Registered users",
                        value=users,
                        inline=True)
                    embed.add_field(
                        name=":gear: Net difficulty",
                        value=difficulty,
                        inline=True)
                    embed.add_field(
                        name=":coin: All mined DUCO",
                        value=circulation,
                        inline=True)
                    embed.add_field(
                        name=":moneybag: DUCO market cap",
                        value=market_cap,
                        inline=True)
                    embed.add_field(
                        name="<:duco_logo:832307063395975218> DUCO price",
                        value=duco_price,
                        inline=True)
                    embed.add_field(
                        name="More stats",
                        value="[Duino-Coin Explorer](https://explorer.duinocoin.com/)",
                        inline=True)

                    await message.channel.send(embed=embed)

            elif command[0] == "help":
                with message.channel.typing():
                    await message.channel.send(embed=help_embed)

            elif command[0] == "p" or command[0] == "profile":
                with message.channel.typing():
                    created = message.author.created_at
                    if message.author.guild_permissions.administrator:
                        admin = "Yes"
                    else:
                        admin = "No"

                    embed = discord.Embed(
                        title=message.author.display_name+"'s profile",
                        color=discord.Color.gold(),
                        timestamp=datetime.utcnow())
                    embed.set_author(
                        name=message.author.display_name,
                        icon_url=message.author.avatar_url)
                    embed.set_footer(
                        text=client.user.name,
                        icon_url=client.user.avatar_url)
                    embed.set_thumbnail(
                        url=message.author.avatar_url)
                    embed.add_field(
                        name="User",
                        value=message.author,
                        inline=False)
                    embed.add_field(
                        name="ID",
                        value=message.author.id,
                        inline=False)
                    embed.add_field(
                        name="Admin",
                        value=admin,
                        inline=False)
                    embed.add_field(
                        name="Account creation date",
                        value=str(created)[:-7],
                        inline=False)

                    await message.channel.send(embed=embed)

            elif command[0] == "invite":
                await message.channel.send("Command disabled")
                return
                with message.channel.typing():
                    embed = discord.Embed(
                        title="Invite Duino Stats Mini",
                        description=(
                            "[Click this text to add this bot to your server]"
                            + "(https://discord.com/api/oauth2/authorize?client_id="
                            + "876506340112076801&permissions=257701570624&scope=bot)"),
                        color=discord.Color.gold(),
                        timestamp=datetime.utcnow())
                    embed.set_author(
                        name=message.author.display_name,
                        icon_url=message.author.avatar_url)
                    embed.set_footer(
                        text=client.user.name,
                        icon_url=client.user.avatar_url)

                    await message.channel.send(embed=embed)

            elif command[0] == "about":
                with message.channel.typing():
                    in_servers = str(len(client.guilds))
                    embed = discord.Embed(
                        title="Duino Stats Mini",
                        description=(
                            "An official, public, stripped down version of"
                            + " [**Duino Stats**]"
                            + "(https://github.com/Bilaboz/duino-stats)"
                            + " found on the [**Official Duino-Coin Discord**]"
                            + "(https://discord.gg/duinocoin).\n\n"
                            + "Created by [**primitt**](https://github.com/primitt)"
                            + " and [**revox**](https://github.com/revoxhere)"
                            + " from the **Duino** team\n"
                            + "Hosted on a **Raspberry Pi 4**\n"
                            + "Serving **" + in_servers + " servers**\n"
                            + "This bot is open-source. You can improve it [here]"
                            + "(https://github.com/primitt/duino-stats-mini/)"),
                        color=discord.Color.gold(),
                        timestamp=datetime.utcnow())
                    embed.set_author(
                        name=message.author.display_name,
                        icon_url=message.author.avatar_url)
                    embed.set_footer(
                        text=client.user.name,
                        icon_url=client.user.avatar_url)

                    await message.channel.send(embed=embed)

            elif (command[0] == "server"
                  or command[0] == "servers"
                    or command[0] == "nodes"):
                with message.channel.typing():
                    embed = discord.Embed(
                        title="Please wait",
                        description=("Pinging **Duino-Coin** services..."),
                        color=discord.Color.gold(),
                        timestamp=datetime.utcnow())
                    embed.set_author(
                        name=message.author.display_name,
                        icon_url=message.author.avatar_url)
                    embed.set_footer(
                        text=client.user.name,
                        icon_url=client.user.avatar_url)
                    msg = await message.channel.send(embed=embed)

                    embed = discord.Embed(
                        title="Node check results",
                        color=discord.Color.gold(),
                        timestamp=datetime.utcnow())
                    embed.set_author(
                        name=message.author.display_name,
                        icon_url=message.author.avatar_url)
                    embed.set_footer(
                        text=client.user.name,
                        icon_url=client.user.avatar_url)

                    async with aiohttp.ClientSession() as session:
                        async with session.get(NODE_API) as resp:
                            response = json.loads(
                                await resp.text())["result"]

                    response = sorted(response, key = lambda i: i['connections'])

                    for node in response:
                        try:
                            time_el = int(
                                ''.join(filter(str.isdigit, node['lastsync'])))
                        except:
                            time_el = -1

                        if (node['lastsync'] == "unknown" 
                            or time_el == -1 
                            or time_el >= 3600):
                            continue
                        elif time_el >= 90:
                            node["name"] += f" {EM_FALSE} "
                        elif time_el >= 20:
                            node["name"] += f" {EM_WARNING} "
                        else:
                            node["name"] += f" {EM_TRUE} "


                        embed.add_field(
                            name=node["name"],
                            value=(f"Last synced: **{node['lastsync']}**\n"
                                   + f"CPU: **{node['cpu']}%** RAM: **{node['ram']}%**\n"
                                   + f"Clients: **{node['connections']}**"),
                            inline=True)

                    await msg.edit(embed=embed)

client.run(TOKEN)
