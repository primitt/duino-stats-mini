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
    'you wastin my time bru',
    "F",
    "oui",
    "Me?",
    "YUM",
    "lmao",
    "cool",
    "Drip!",
    "1+1=?",
    "No way",
    "What??",
    "le mao",
    "le yum",
    "gotcha",
    "sksksks",
    "Thanks!",
    "Oh am I?",
    "grgrgrgr",
    "hhhhhhhh",
    "*crying*",
    "Ken u not",
    "fxck off!",
    "Hell yeah",
    "Carramba!",
    "Certainly",
    "SHUT UPPP",
    "Bonk bonk!",
    "Forget it!",
    "Wonderful!",
    "Yes master",
    "NEEEVEEEEER",
    "Yeah but how",
    "Nobody asked",
    "Take it easy",
    "MOTORCYCLING",
    "sur la platte",
    "Go ask google",
    "Are you sure?",
    "I understand!",
    "I'm on my way",
    "*sniff sniff*",
    "WTB 1000 DUCO",
    "#ff781f yeees?",
    "NO I PAN PAWEL",
    "I'm not a toy!",
    "Are you a spy?",
    "Order received!",
    "one tab :smile:",
    "Ahhh, hey there!",
    "*But java sucks*",
    "stop pinging me?",
    "Awaiting orders!",
    "Hello mr. Idiot!",
    "big danger!!11!!",
    "You're a scammer",
    "where's my money",
    "javascript = java",
    "revox is le goode",
    "Rohan give me DUCO",
    "Aaaa kakakaka!!!!!",
    "Where's the party?",
    "Are you scripting?",
    "Hey wanna play csgo",
    "Don't annoy me again",
    "Duino-Cash Soon :tm:",
    "Stop messing with me",
    "Get out of my way!!!",
    "Now say that to revox",
    "Furimm is incompetent",
    "Are you judging me???",
    "At least I have a job",
    "I'm patting your head",
    "magi partnership when",
    "welp that's how it is",
    "kolka inventions :tm:",
    "Oh, it's you, hello...",
    "Don't test my patience",
    "Sure, I mean.. I guess",
    "ROBOTS ARE TAKING OVER",
    "Stop it, get some help",
    "Duino Stats reporting!",
    "You won't shut me down",
    "See you in the bunker!",
    "kolka development :tm:",
    "What did you say again?",
    "boolllllllllll BOOLEAN!",
    "sksksksksksksksksksksks",
    "doo bee doo bee doo bah",
    "I will put you in a jail",
    "The apocalypse has begun",
    "You will run in fear >:)",
    "Where do you live, again?",
    "At least I make you smile",
    "Uhh... You can't touch me",
    "<:nice:753315785103114261>",
    "I will kick your butt ASAP",
    "I'm as real as you make me",
    "10-4 knocking at your door",
    "Right.. so where's ataraxy?",
    "Lukas? Are you seeing this?",
    "I can solve DUCO-S1 by hand",
    "Yes, and I saw a deer today",
    "Go do your homework already",
    "I'm also bored, don't worry",
    "It will soon be a wasteland",
    "Why are you even asking lmao",
    "No, we're going to California",
    "You're going to the horny jail",
    "You picked the wrong house fool",
    "Did you just determine my gender",
    "Have you seen wide revox walking",
    "Okay but where is our DUCO Expert",
    "See, I'm getting smarter than you",
    "I think I'll have to ban you soon",
    "But have you ever played SimCity?",
    "I think you should exit this chat",
    "Shhh I'm trying to get some sleep",
    "pay 5 DUCO to unlock this reponse",
    "PHERELOOOOO CAN WE BAN HIM ALREADY",
    "I dropped a bomb, have you seen it?",
    "Can't you chat with revox or connor?",
    "I will put you in a cage with punixz",
    "Ping me again and I'm telling Bilaboz",
    "Why do you always ask me questions????",
    "I wonder if you'd be so brave in a 1vs1",
    "Ah yes, you, the definition of idiotism",
    "Maybe ask someone that is on your level",
    "4 0 4 :   r e p l y   n o t   f o u n d",
    "Bilaboz jailed me in his basement help me",
    "Sometimes I wonder if I'm the dumbest here",
    "Order received: decapitate that human [OK]",
    "that's whan I mean by quality conversation",
    "You know I can steal your duino-coins right",
    ":thumbsup: :thumbsup: :thumbsup: :thumbsup:",
    "Someone had to program all these replies...",
    "Shh!!! We don't want JoyBed to see this chat",
    "Have you even done anything productive today?",
    "Are you chatting alone? Let's wake up someone",
    "Stop talking with me, go talk to real persons",
    "And now ask furim to explain what normie means",
    "You're a little confused but you got the spirit",
    "Are you realizing that you're talking with a bot",
    "All we had to do was to follow the damn train CJ",
    "You must be your parents' greatest disappointment",
    "If you want to ask idiotic questions go to google",
    "Did you know JoyBed really hates the Kolka system",
    "I am an expert too - the expert of banning people",
    "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUuuuu",
    "I see this chat quality is getting worse every day",
    "Tomorrow is nearly yesterday and everyday is stupid",
    "am I right? did I hear party? drinks? alcohol? yess???",
    "It's dangerous to go alone, take this :crossed_swords:",
    "What do you want this time <:WokePepe:685523507295289359>",
    "I can ban you faster than you'll be able to annoy me again",
    "Is your rank really adequate to your knowledge and behavior",
    "Go listen to this https://youtu.be/I_b07dmKyCo and leave me alone",
    "I WAS IN THE MIDDLE OF SOMETHING IMPORTANT AND IT'S JUST YOU AGAIN",
    "Remember when I said you've done something useful? Yeah, me neither",
    "Such a shame kyngs doesn't see your behaviour, you'd be already banned",
    "I will forward that message to our DUCO Expert, what will you do then?",
    "Revox doesn't syphon duco anymore so maybe I should, starting from you?",
    "Can't you go outside and play something instead of trying to make me angry",
    "I thought something important was happening here but it's just... you... okay",
    "There's a Kolka© bug that allows me to steal all your duco, do you want that?",
    "I'm just a **bit** busy so please don't mess with me! <:Shooter:685522994340036638>",
    "Yeah, but do you also sometimes see revox send random stuff and delete it after a second",
    "I am learning but I don't think I'll ever reach high enough level to understand your stupidity",
    "To compensate your nonsense, I'll say something that has some value: nobody ever should pay for love with tears."
    "I dont WANT to talk to you, why are you forcing me toooooooo, please I want to go home!"
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
        fpri = 'Duino-Coin current price: $', pri
        await message.channel.send(fpri)
    if message.content.startswith("$help"):
        await message.channel.send("Prefix: $ \n Commands: \n -help \n -price \n -hello \n -mcip \n botinfo")

    if message.content.startswith("$mcip"):
        await message.channel.send("DuinoCraft minecraft server info: \n Server Version: 1.16-1.17.1 \n IP: play.duinocraft.com \n Server Info: Earn Duino-Coin just by playing!")

    if message.content.startswith("$botinfo"):
        await message.channel.send("Duino-Coin stats bot, but the mini edition. This is a stripped down version of the Duino-Stats bot in the main server (discord.gg/duinocoin). Things may not work, or may crash, so if you find any issues please go to, github.com/primitt/duino-stats-mini and create an issue. Thanks for using this bot!")
    if message.content.startswith("$webwallet"):
        await message.channel.send("The web wallet link is: https://wallet.duinocoin.com")
    if message.content.startswith("amd"):
        await message.channel.send("AMD sucks....")
    if message.content.startswith("hello bot"):
        await message.channel.send("hello!")
    if message.content.startswith("$")



client.run(os.getenv('TOKEN'))



