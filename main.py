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
import traceback
from time import sleep

load_dotenv()
client = discord.Client()

EM_TRUE = "<:true:877164045248102471>"
EM_FALSE = "<:false:877164045176819782>"
TOKEN = os.getenv('TOKEN')
PREFIX = "+"
REPLIES_URI = 'utils/replies.json'
USER_API = "https://server.duinocoin.com/users/"
PRICE_API = "https://server.duinocoin.com/api.json"
{
    ":floppy_disk: Master Server": {
        "ip": "51.15.127.80",
        "port": 2812,
        "status": ":question: Unknown"
    },
    ":heartpulse: PulsePool": {
        "ip": "149.91.88.18",
        "port": 1224,
        "status": ":question: Unknown"
    },
    ":star: StarPool": {
        "ip": "51.158.182.90",
        "port": 6006,
        "status": ":question: Unknown"
    },
    ":snowflake: BeyondPool": {
        "ip": "beyondpool.io",
        "port": 6000,
        "status": ":question: Unknown"
    },
    ":broken_heart: SvkoPool": {
        "ip": "5.230.69.132",
        "port": 6000,
        "status": ":question: Unknown"
    }
}


with open(REPLIES_URI, "r") as replies_file:
    duino_stats_replies = json.load(replies_file)

duino_stats_pings = [
    "hey",
    "stop ignoring me",
    "plz respond :(",
    "hi",
    "!!!!",
    "task for you"
]

cards = [
    "utils/card_1.png",
    "utils/card_2.png"
]


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

        image.save('utils/out.png')
        return True
    except Exception as e:
        return False


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
            name="with your duinos - " + PREFIX + "help"))


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
        icon_url=message.author.avatar_url)
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
        `{p}price` - Show current DUCO prices
        `{p}help` - Show this help message
        `{p}mcip` - Show DuinoCraft IP
        `{p}mc-survival` - Shows online people in the Survival mc server
        `{p}mc-skyblock` - Shows online people in the SkyBlock mc server
        `{p}profile` - Show info about your profile
        `{p}server` - Show mining nodes status
        `{p}invite` - Invite Duino Stats Mini to your server
        `{p}about` - Show info about the bot
        `{p}statistics` - Show network stats
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

    if message.guild.id == 677615191793467402:
        if random.randint(0, 500) == 77:
            rand_ping = random.choice(duino_stats_pings)
            await message.channel.send(
                "<@!691404890290913280> "
                + rand_ping
            )

    if message.author == client.user:
        return

    if mention in message.content:
        response = random.choice(duino_stats_replies)
        await message.channel.send(
            message.author.mention
            + ", "
            + response)

    if message.content.startswith(PREFIX):
        command = message.content.strip(PREFIX).split(" ")

        # adding the people printing
        # Planification
        """ 
        It needs 4 phases:
        - contact w the api (retrieve the json w requests)
        - test req status (test if it reached the API)
        - parse the json (inside players index)
        - show the info w an embed
        """

        if command[0] == "mc-survival":

            survival_url = "https://api.mcsrvstat.us/2/survival.duinocraft.com"

            # retrieve json
            request = requests.get(survival_url)

            # check status
            status = request.status_code
            if status == 200:
                print("Status: "+str(status))
            else:
                raise Exception("Request to API with status: " + status)
            # parse json
            data = request.text
            json_data = json.loads(data)
            online_people = json_data['players']
            online_amount = online_people["online"]

            if online_amount > 0:
                players = online_people["list"]

                # player counter
                counter = 1

                # print with embed

                embed = discord.Embed(
                    title="Online people in Survival Server.",
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
                embed.add_field(
                    name="Online players amount",
                    value=str(online_amount),
                    inline=False
                )
                for player in players:
                    embed.add_field(
                        name="Players List",
                        value=str("Player "
                                  + str(counter)
                                  + ": "
                                  +
                                  player),
                        inline=False
                    )
                    counter += 1
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Online people in Survival Server.",
                    color=discord.Color.gold(),
                    timestamp=datetime.utcnow()
                )
                embed.set_author(
                    name=message.author.display_name,
                    icon_url=message.author.avatar_url
                )
                embed.set_footer(
                    text=client.user.name,
                    icon_url=client.user.avatar_url)
                embed.add_field(
                    name="There are no players online",
                    value="Players: " + str(online_amount),
                    inline=False
                )
                await message.channel.send(embed=embed)

        if command[0] == "mc-skyblock":

            skyblock_url = "https://api.mcsrvstat.us/2/skyblock.duinocraft.com"

            # retrieve json
            request = requests.get(skyblock_url)

            # check status
            status = request.status_code
            if status == 200:
                print("Status: "+str(status))
            else:
                raise Exception("Request to API with status: " + status)
            # parse json
            data = request.text
            json_data = json.loads(data)
            online_people = json_data['players']
            online_amount = online_people["online"]

            if online_amount > 0:
                players = online_people["list"]

                # player counter
                counter = 1

                # print with embed

                embed = discord.Embed(
                    title="Online people in SkyBlock Server.",
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
                embed.add_field(
                    name="Online players amount",
                    value=str(online_amount),
                    inline=False
                )
                for player in players:
                    embed.add_field(
                        name="Players List",
                        value=str("Player "
                                  + str(counter)
                                  + ": "
                                  +
                                  player),
                        inline=False
                    )
                    counter += 1
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Online people in Survival Server.",
                    color=discord.Color.gold(),
                    timestamp=datetime.utcnow()
                )
                embed.set_author(
                    name=message.author.display_name,
                    icon_url=message.author.avatar_url
                )
                embed.set_footer(
                    text=client.user.name,
                    icon_url=client.user.avatar_url)
                embed.add_field(
                    name="There are no players online",
                    value="Players: " + str(online_amount),
                    inline=False
                )
                await message.channel.send(embed=embed)

        if command[0] == "say":
            if message.author.guild_permissions.administrator:
                command[0] = ""
                await message.delete()
                await message.channel.send(" ".join(command))
            else:
                await message.channel.send(
                    ":no_entry: You dont't have the permission to do that!")

        if (command[0] == "balance"
            or command[0] == "bal"
                or command[0] == "b"):
            try:
                _ = command[1]
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(USER_API
                                               + command[1]) as resp:
                            response = json.loads(await resp.text())

                    if not response["success"]:
                        await message.channel.send("This user doesn't exist")

                    else:
                        balance = float(
                            response["result"]["balance"]["balance"])
                        miners_a = response["result"]["miners"]
                        verified = response["result"]["balance"]["verified"]
                        created = response["result"]["balance"]["created"]

                        import traceback
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
                                title=str(command[1]+"'s Duino-Coin account"),
                                color=discord.Color.gold(),
                                timestamp=datetime.utcnow())
                            embed.set_author(
                                name=message.author.display_name,
                                icon_url=message.author.avatar_url)
                            embed.set_footer(
                                text=client.user.name,
                                icon_url=client.user.avatar_url)

                            embed.add_field(
                                name="<:duco:876588980630618152> Balance",
                                value=str(balance)
                                + " DUCO"
                                + " ($"
                                + str(round(balance_in_usd, 4))
                                + ")",
                                inline=False)

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

                            if generate_card(command[1], balance,
                                             message.author.display_name):
                                print("Adding image")
                                await message.channel.send(
                                    embed=embed,
                                    file=discord.File("utils/out.png"))
                            else:
                                await message.channel.send(embed=embed)

                        except Exception as e:
                            await message.channel.send(
                                "`ERROR` Can't fetch user data: "
                                + str(traceback.format_exc()))
                except Exception as e:
                    await message.channel.send(
                        "`ERROR` Can't fetch the balances: "
                        + str(e))
            except IndexError:
                await message.channel.send(
                    "Provide a username first (e.g. {}bal revox)"
                    .format(PREFIX))

        if command[0] == "price":
            async with aiohttp.ClientSession() as session:
                async with session.get(PRICE_API) as resp:
                    response_price = json.loads(
                        await resp.text())

            price_xmg = float(response_price["Duco price"])
            price_bch = float(response_price["Duco price BCH"])
            price_trx = float(response_price["Duco price TRX"])

            price_nano = float(response_price["Duco price NANO"])
            price_xrp = float(response_price["Duco price XRP"])
            price_dgb = float(response_price["Duco price DGB"])
            price_fjc = float(response_price["Duco price FJC"])

            price_justswap = float(response_price["Duco JustSwap price"])
            price_pancake = float(response_price["Duco PancakeSwap price"])
            price_nodes = float(response_price["Duco Node-S price"])

            embed = discord.Embed(
                description=("Please keep in mind that price "
                             + "on the chart is updated every 1 day"),
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
                value="$"+str(round(price_xmg, 6)),
                inline=True)
            embed.add_field(
                name="<:bitcoincash:876963784491671622> DUCO Exchange (BCH)",
                value="$"+str(round(price_bch, 6)),
                inline=True)
            embed.add_field(
                name="<:tron:876962726000349204> DUCO Exchange (TRX)",
                value="$"+str(round(price_trx, 6)),
                inline=True)
            embed.add_field(
                name="<:nano:876962697730752552> DUCO Exchange (NANO)",
                value="$"+str(round(price_nano, 6)),
                inline=True)
            embed.add_field(
                name="<:digibyte:876962596270510120> DUCO Exchange (DGB)",
                value="$"+str(round(price_dgb, 6)),
                inline=True)
            embed.add_field(
                name="<:ripple:876962797882327110> DUCO Exchange (XRP)",
                value="$"+str(round(price_xrp, 6)),
                inline=True)
            embed.add_field(
                name="<:fuji:876962642370134097> DUCO Exchange (FJC)",
                value="$"+str(round(price_fjc, 6)),
                inline=True)
            embed.add_field(
                name=":currency_exchange: Node-S Exchange",
                value="$"+str(round(price_nodes, 6)),
                inline=True)
            embed.add_field(
                name=":white_flower: JustSwap",
                value="$"+str(round(price_justswap, 6)),
                inline=True)
            embed.add_field(
                name=":pancakes: PancakeSwap",
                value="$"+str(round(price_pancake, 6)),
                inline=True)
            embed.add_field(
                name=":person_standing: otc-trading",
                value="[Duino-Coin Discord](https://discord.gg/duinocoin)",
                inline=True)
            embed.set_image(url="https://server.duinocoin.com/prices.png")

            await message.channel.send(embed=embed)

        if (command[0] == "stats"
                or command[0] == "statistics"):
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
                name="<:duco:876588980630618152> DUCO price",
                value=duco_price,
                inline=True)
            embed.add_field(
                name="More stats",
                value="[Duino-Coin Explorer](https://explorer.duinocoin.com/)",
                inline=True)

            await message.channel.send(embed=embed)

        if command[0] == "help":
            await message.channel.send(embed=help_embed)

        if command[0] == "p":
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

        if command[0] == "mcip":
            embed = discord.Embed(
                title="DuinoCraft",
                description=("Server version: **Minecraft 1.16-1.17.1**\n"
                             + "Survival: **survival.duinocraft.com** \n"
                             + "Skyblock: **skyblock.duinocraft.com** \n"
                             + "Earn Duino-Coin just by playing!"),
                color=discord.Color.gold(),
                timestamp=datetime.utcnow())
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.avatar_url)
            embed.set_footer(
                text=client.user.name,
                icon_url=client.user.avatar_url)

            await message.channel.send(embed=embed)

        if command[0] == "invite":
            embed = discord.Embed(
                title="Invite Duino Stats Mini",
                description=(
                    "[Click this text to add this bot to your server]"
                    + "(https://discord.com/api/oauth2/authorize?client_id="
                    + "876506340112076801&permissions=257701570624&scope=bot)"
                ),
                color=discord.Color.gold(),
                timestamp=datetime.utcnow())
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.avatar_url)
            embed.set_footer(
                text=client.user.name,
                icon_url=client.user.avatar_url)

            await message.channel.send(embed=embed)

        if command[0] == "about":
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

        if (command[0] == "server"
            or command[0] == "servers"
                or command[0] == "nodes"):
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
                title="Ping results",
                color=discord.Color.gold(),
                timestamp=datetime.utcnow())
            embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.avatar_url)
            embed.set_footer(
                text=client.user.name,
                icon_url=client.user.avatar_url)

            for node in NODES:
                from socket import socket
                s = socket()
                try:
                    s.settimeout(1)
                    s.connect((NODES[node]["ip"], NODES[node]["port"]))
                    ver = s.recv(3)
                    if float(ver):
                        NODES[node]["status"] = EM_TRUE + " Operational"
                    else:
                        NODES[node]["status"] = EM_TRUE + " Offline"
                except Exception:
                    NODES[node]["status"] = EM_FALSE + " Timeout"

                embed.add_field(
                    name=node,
                    value=NODES[node]["status"],
                    inline=True)

            await msg.edit(embed=embed)

client.run(TOKEN)
