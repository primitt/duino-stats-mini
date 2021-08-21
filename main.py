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
import threading
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
NODES = {
    ":floppy_disk: Master Server *(51.15.127.80)*": {
        "ip": "51.15.127.80",
        "port": 2812,
        "status": ":question: Unknown"
    },
    ":heartpulse: PulsePool *(149.91.88.18)*": {
        "ip": "149.91.88.18",
        "port": 5999,
        "status": ":question: Unknown"
    },
    ":star: StarPool *(51.158.182.90)*": {
        "ip": "51.158.182.90",
        "port": 6000,
        "status": ":question: Unknown"
    },
    ":trophy: WinnerPool *(193.164.7.180)*": {
        "ip": "193.164.7.180",
        "port": 6000,
        "status": ":question: Unknown"
    },
    ":snowflake: BeyondPool *(beyondpool.io)*": {
        "ip": "beyondpool.io",
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
        + str(symbol)
    )


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

    #sleep(5)
    #while True:
    #    in_servers = str(len(client.guilds))
    #    await client.change_presence(
    #        activity=discord.Game(
    #            name="serving " + in_servers + " servers"))
    #    sleep(15)
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
        `{p}price` - Show current DUCO prices
        `{p}help` - Show this help message
        `{p}mcip` - Show DuinoCraft IP
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
                        miners = response["result"]["miners"]

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
                                name="<:duco:876588980630618152> Balance",
                                value=str(balance)
                                + " DUCO"
                                + " ($"
                                + str(round(balance_in_usd, 4))
                                + ")",
                                inline=False
                            )

                            total_hashrate = 0
                            if not miners:
                                miner_str = "No miners running on this account"
                            else:
                                miner_str = ""
                                i = 0
                                for miner in miners:
                                    total_hashrate += miner["hashrate"]

                                    if miner["identifier"] != "None":
                                        miner_str += (
                                            miner["identifier"]
                                            + " ("
                                            + miner["software"]
                                            + ")")
                                    else:
                                        miner_str += miner["software"]

                                    miner_str += (
                                        " **"
                                        + str(miner["accepted"])
                                        + "/"
                                        + str(miner["accepted"] +
                                              miner["rejected"])
                                        + "** "
                                        + str(prefix("H/s", miner["hashrate"]))
                                        + "\n"
                                    )

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
                                inline=False
                            )

                            await message.channel.send(embed=embed)

                        except Exception as e:
                            await message.channel.send(
                                "`ERROR` Can't fetch user data: "
                                + str(e)
                            )
                except Exception as e:
                    await message.channel.send(
                        "`ERROR` Can't fetch the balances: "
                        + str(e)
                    )
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

            price_justswap = float(response_price["Duco JustSwap price"])
            price_nodes = float(response_price["Duco Node-S price"])

            embed = discord.Embed(
                description=("Please keep in mind that price "
                             + "on the chart is updated every 1 day"),
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
                name="<:magi:876963168218394644> DUCO Exchange (XMG)",
                value="$"+str(round(price_xmg, 6)),
                inline=True
            )
            embed.add_field(
                name="<:bitcoincash:876963784491671622> DUCO Exchange (BCH)",
                value="$"+str(round(price_bch, 6)),
                inline=True
            )
            embed.add_field(
                name="<:tron:876962726000349204> DUCO Exchange (TRX)",
                value="$"+str(round(price_trx, 6)),
                inline=True
            )
            embed.add_field(
                name="<:nano:876962697730752552> DUCO Exchange (NANO)",
                value="$"+str(round(price_nano, 6)),
                inline=True
            )
            embed.add_field(
                name="<:digibyte:876962596270510120> DUCO Exchange (DGB)",
                value="$"+str(round(price_dgb, 6)),
                inline=True
            )
            embed.add_field(
                name="<:ripple:876962797882327110> DUCO Exchange (XRP)",
                value="$"+str(round(price_xrp, 6)),
                inline=True
            )
            embed.add_field(
                name=":currency_exchange: Node-S Exchange",
                value="$"+str(round(price_nodes, 6)),
                inline=True
            )
            embed.add_field(
                name=":white_flower: JustSwap",
                value="$"+str(round(price_justswap, 6)),
                inline=True
            )
            embed.add_field(
                name=":person_standing: otc-trading",
                value="[Duino-Coin Discord](https://discord.gg/duinocoin)",
                inline=True
            )
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
                round(response["Duco price"]*response["All-time mined DUCO"], 2)
            )

            embed = discord.Embed(
                title="Duino-Coin Statistics",
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
                name=":pick: Net hashrate",
                value=total_hashrate,
                inline=True
            )
            embed.add_field(
                name=":evergreen_tree: Net energy usage",
                value=net_wattage,
                inline=True
            )
            embed.add_field(
                name=":people_holding_hands: Registered users",
                value=users,
                inline=True
            )
            embed.add_field(
                name=":gear: Net difficulty",
                value=difficulty,
                inline=True
            )
            embed.add_field(
                name=":coin: All mined DUCO",
                value=circulation,
                inline=True
            )
            embed.add_field(
                name=":moneybag: DUCO market cap",
                value=market_cap,
                inline=True
            )
            embed.add_field(
                name="<:duco:876588980630618152> DUCO price",
                value=duco_price,
                inline=True
            )
            embed.add_field(
                name="More stats",
                value="[Duino-Coin Explorer](https://explorer.duinocoin.com/)",
                inline=True
            )

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
            embed.set_thumbnail(
                url=message.author.avatar_url
            )
            embed.add_field(
                name="User",
                value=message.author,
                inline=False
            )
            embed.add_field(
                name="ID",
                value=message.author.id,
                inline=False
            )
            embed.add_field(
                name="Admin",
                value=admin,
                inline=False
            )
            embed.add_field(
                name="Account creation date",
                value=str(created)[:-7],
                inline=False
            )

            await message.channel.send(embed=embed)

        if command[0] == "mcip":
            embed = discord.Embed(
                title="DuinoCraft",
                description=("Server version: **Minecraft 1.16-1.17.1**\n"
                             + "IP: **play.duinocraft.com**\n"
                             + "Earn Duino-Coin just by playing!"),
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

        if command[0] == "invite":
            embed = discord.Embed(
                title="Invite Duino Stats Mini",
                description=(
                    "[Click this text to add this bot to your server]"
                    + "(https://discord.com/api/oauth2/authorize?client_id="
                    + "876506340112076801&permissions=257701570624&scope=bot)"
                ),
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
                    + "(https://github.com/primitt/duino-stats-mini/)"
                ),
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

        if (command[0] == "server"
            or command[0] == "servers"
                or command[0] == "nodes"):
            embed = discord.Embed(
                title="Please wait",
                description=("Pinging **Duino-Coin** services..."),
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
            msg = await message.channel.send(embed=embed)

            embed = discord.Embed(
                title="Ping results",
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
                    inline=True
                )

            await msg.edit(embed=embed)

client.run(TOKEN)
