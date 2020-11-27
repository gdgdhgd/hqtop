import discord
import random
from discord.ext import commands
import asyncio
from pymongo import MongoClient
from HQApi import HQApi
import asyncio
from datetime import datetime
import requests
import time
import colorsys
global checkbuycmd
checkbuycmd = "ON"
global checkstockcmd
checkstockcmd = "ON"
global dis
dis = 0
global buycmd
buycmd = "ON"

client = MongoClient('mongodb+srv://wavehq:Test237@modmail-3ntpq.mongodb.net/test?retryWrites=true&w=majority')
db = client.get_database("trivia")
database = db.user
lifebase = db.life
number_base = db.number
pending_base = db.pending
numbers_base = db.numbers
white = [702645536758693909,608461422694891530]#Discord ID For Owner
black = [702645536758693909,608461422694891530]#Discord ID2 For Owner
red = [702645536758693909,608461422694891530] #Stock Adder ID
def rand():
    ran = random.randint(3,12)
    x = "1234567890"
    y = "1234567890"
    uname = ""
    for i in range(ran):
      first = random.choice(("Aine", "Aliz", "Amy", "Anya", "Arya", "Ayn", "Bay", "Cia", "laire", "Clor", "Cora", "Coco", "Dawn", "Fleur", "Eva", "Etta", "Erin", "Robin", "Dan","Camil","Ringo","Cayli","Digna","Emma","Galen","Helma","Jance","Gretl","Hazel","Gwen","Helen","Ella","Edie",'Ivy'))
    second = random.choice(("Jill", "Joss", "Juno", "Kady", "Kai", "Kira", "Klara", "Lana", "Leda", "Liesl", "Lily", "Amaa", "Mae", "Lula", "Lucia", "Mia", "Myra", "Opal", "Paige", "Rain", "Quinn", "Rose", "Sia", "Taya", "Teva", "markus", "Judie", "Zuri", "Zoe", "Vera", "Una", "Reeve",'Ekta'))
    c = random.choice(("1", "2", "3"))
    if c == "1":uname = first + second
    elif c == "2":uname = first.title() + second.title()
    elif c == "3": uname = first + second.title()
    d = random.choice(x)
    e = random.choice(y)
    name = uname+d+e
    api = HQApi()
    check = api.check_username(name)
    if not check:
        return name
    else:
        return rand()

bot = commands.Bot(command_prefix='-')
bot.remove_command('help')

@bot.event
async def on_ready():
    print("started")
    ch = bot.get_channel(762131453684219934)#Your Channel ID Here
    await bot.change_presence(activity=discord.Game(name='with Trivia Lives| -help for info'))
    await ch.send("**__Bot Restarted with Upgrades!__** :smirk_cat:")

@bot.command()
async def dm(ctx):
    await ctx.author.send("What up chump?")
@commands.dm_only()
@bot.command()
async def lifes(ctx, refname, amount=1):
    logchannel = bot.get_channel(762131453684219934)
    user_in_list = True
    commander_id = ctx.message.author.id
    num_list = []
    all_data = list(number_base.find())
    for i in all_data:
        num_list.append(i['number'])
    stock = len(num_list)
    id_list = []
    all_data = list(database.find())
    for i in all_data:
        id_list.append(i['id'])
    if commander_id in id_list:
        spec_user_point = database.find_one({'id': commander_id})['points']
    else:
        user_in_list = False
    if amount > stock:
        async with ctx.typing():
            await ctx.send('<@{}> **Sorry we are out of this much stock. Current total stock: `{}`**'.format(commander_id, stock))
    elif amount > spec_user_point or user_in_list == False:
        async with ctx.typing():
            await ctx.send("<@{}> **You don't have enough point. Type `+point` to check**".format(commander_id))
    else:
      global checkbuycmd
      if checkbuycmd == "OFF":
        await ctx.send("**Oof seems that Life Making is currently unavailable!**")
        return
      else:
        pass

        number_list = list(number_base.find())
        gen = 0
        message_id = 0
        total = list(lifebase.find())
        for i in total:
            tot = i['life']
        new_tot = tot + amount
        updat = {'life': new_tot}
        lifebase.update_one({'life': tot}, {'$set': updat})
        spec_user_point = database.find_one({'id': commander_id})['points']
        new_amount = spec_user_point - amount
        update = {'points': new_amount}
        database.update_one({'id': commander_id}, {'$set': update})
        for i in range(0,amount):
            token = number_list[i]['token']
            login_api = HQApi(token=token)
            login_api.add_referral(refname)
            pend = {'berear': token}
            pending_base.insert_one(pend)
            number_base.delete_one({'token': token})
            gen += 1
            if gen == 1:
                await logchannel.send(content="<@{}> **Life generated `{}` of `{}` for {}**".format(commander_id, gen, amount, refname))
                old_message = await ctx.send('<@{}> **Life generated `{}` of `{}`**'.format(commander_id, gen, amount))
                message_id = old_message.id
            elif gen > 1:
                channel = ctx.channel
                message = await channel.fetch_message(message_id)
                await message.edit(content="<@{}> **Life generated `{}` of `{}`**".format(commander_id, gen, amount))
                await logchannel.send(content="<@{}> **Life generated `{}` of `{}` for {}**".format(commander_id, gen, amount, refname))

@lifes.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.PrivateMessageOnly):
        embed=discord.Embed(title="Direct Messages Only!", description="Be aware! People may have entered this server to look for usernames in order to abuse. For the security of your account, please use that command in direct message only!", color=0xff0000)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/637847068773449738/740370322754240562/IMG-20200805-WA0004.jpg")
        embed.set_footer(text="Cheapest HQ Life")
        await ctx.send(embed=embed)
                
@bot.command()
async def stocks(ctx):
    commander_id = ctx.message.author.id
    global checkstockcmd
    if checkstockcmd == "OFF":
        embed=discord.Embed(title="***Backup Stock***", description="", color=0x00ff00)
        embed.add_field(name="** HQ Trivia **", value=f"**• Lives: Wait Few Hours...**", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/641267482778140715/740462311101169766/PicsArt_08-05-08.04.41.png")
        embed.set_footer(text="Cheapest HQ Life")
        await ctx.send(embed=embed)
        return
    num_list = []
    all_data = list(number_base.find())
    for i in all_data:
        num_list.append(i['number'])
    stock = len(num_list)
    async with ctx.typing():
        embed=discord.Embed(title="***Backup Stock***", description="", color=0x00ff00)
        embed.add_field(name="** HQ Trivia **", value=f"**• Lives: {stock}!**", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/641267482778140715/740462311101169766/PicsArt_08-05-08.04.41.png")
        embed.set_footer(text="Cheapest HQ Life")
        #await ctx.send('<@{}> **Total stock: {}**'.format(stock))
        await ctx.send(embed=embed)

@bot.command(pass_context=True, aliases=['s'])
async def backup(ctx, number:str):
    commander_id = ctx.message.author.id
    if commander_id in red:
        check_if_exist = number_base.find_one({"number": number})
        if check_if_exist == None:
            api = HQApi()
            verification = api.send_code("+" + number, "sms")
            async with ctx.typing():
                await ctx.send("<@{}> **Please type the OTP within 1 minute. Please don't type wrong**".format(commander_id))
            def check(m):
                return m.author == ctx.message.author and m.channel == ctx.message.channel
            response = await bot.wait_for('message',check= check, timeout=60)
            code = int(response.clean_content)
            sub_code_res = api.confirm_code(verification["verificationId"], code)
            if sub_code_res['auth'] is not None:
              print("Sorry, this number is already associated with {}".format(sub_code_res['auth']['username']))
              await ctx.send("Sorry, this number is already associated with {}".format(sub_code_res['auth']['username']))
            else:
              a = await ctx.send('**__Login Done! Adding Username__** :wink:')
            name = rand()
            print(name)
            channel = ctx.channel
            message = a
            while True:
                await asyncio.sleep(1)
                try:
                    token = api.register(verification["verificationId"], name)
                    break
                except Exception as e:
                    async with ctx.typing():
                        await message.edit(content="<@{}> **Following error occurred: ```{}```**".format(commander_id,e))
            a_token = token["accessToken"]
            print(a_token)
            number_dict = {'number': number,
                           'token': a_token}
            number_base.insert_one(number_dict)
            await ctx.send("<@{}> **Successfully created an account **__``{}``__** and been thrown in the stock**".format(commander_id,name))
        else:
            async with ctx.typing():
                await ctx.send('<@{}> **Sorry, this number already exist in the database**'.format(commander_id))

    else:
        async with ctx.typing():
            await ctx.send('<@{}> This command is not for you'.format(commander_id))

@backup.error
async def on_command_error(ctx, error):
    if isinstance(error, Exception):
        async with ctx.typing():
            await ctx.send('<@{}> Following error occurred: ```{}```'.format(ctx.message.author.id,error))

@bot.command(pass_context=True, aliases=['add'])
async def add_point(ctx, amount:int):
    addchannel = bot.get_channel(744731279034941461)
    commander_id = ctx.message.author.id
    user_id = ctx.message.mentions[0].id
    if commander_id in white:
        id_list = []
        all_data = list(database.find())
        for i in all_data:
            id_list.append(i['id'])
        if user_id in id_list:
            spec_user_point = database.find_one({'id': user_id})['points']
            new_amount = amount + spec_user_point
            update = {'points': new_amount}
            database.update_one({'id': user_id}, {'$set': update})
        else:
            user_info_dict = {'id': user_id,
                              'points': amount}
            database.insert_one(user_info_dict)
        async with ctx.typing():
            await ctx.send('<@{}> **{} points succefully added to <@{}>**'.format(commander_id, amount, user_id))
            await addchannel.send('<@{}> **{} points succefully added to <@{}>**'.format(commander_id, amount, user_id))
    else:
        async with ctx.typing():
            await ctx.send('<@{}> This command is not for you'.format(commander_id))



@bot.command(pass_context=True, aliases=['remove'])
async def remove_point(ctx, amount:int):
    commander_id = ctx.message.author.id
    user_id = ctx.message.mentions[0].id
    if commander_id in white:
        id_list = []
        all_data = list(database.find())
        for i in all_data:
            id_list.append(i['id'])
        if user_id in id_list:
            spec_user_point = database.find_one({'id': user_id})['points']
            new_amount = spec_user_point - amount
            if new_amount < 0:
                async with ctx.typing():
                    await ctx.send('<@{}> **User <@{}> do not have any existing points to remove**'.format(commander_id, user_id))
            else:
                update = {'points': new_amount}
                database.update_one({'id': user_id}, {'$set': update})
                async with ctx.typing():
                    await ctx.send('<@{}> **{} points successfully removed from <@{}>**'.format(commander_id, amount, user_id))
        else:
            async with ctx.typing():
                await ctx.send('<@{}> **User <@{}> do not have any existing points to remove**'.format(commander_id, user_id))
    else:
        async with ctx.typing():
            await ctx.send('<@{}> This command is not for you'.format(commander_id))


@bot.command(pass_context=True, aliases=['points'])
async def point(ctx):
    username = ctx.message.author.name
    commander_id = ctx.message.author.id
    id_list = []
    all_data = list(database.find())
    for i in all_data:
        id_list.append(i['id'])
    if commander_id in id_list:
        spec_user_point = database.find_one({'id': commander_id})['points']
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed=discord.Embed(title=f"{username}'s Data",color = discord.Color((r << 16) + (g << 8) + b))
        if spec_user_point < 1:
            embed=discord.Embed(title=f"{username}'s Data", description = f"**You have `0` Points**" ,color=0x00ff00)
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/641267482778140715/740443669336948935/PicsArt_08-05-08.03.23.png?width=406&height=406")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f"{username}'s Data", description = f"**You have {spec_user_point} Points**" ,color=0x00ff00)
            embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/2WbDycziznHfXPW3Or7s8KcgHp2601CAev1TDrHdiyg/https/media.discordapp.net/attachments/637847068773449738/740397412207820860/PicsArt_08-05-08.04.06.png")
            await ctx.send(embed=embed)

    else:
        embed=discord.Embed(title=f"{username}'s Data", description = f"**You have `0` Points**" ,color=0x00ff00)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/637847068773449738/740397412379656302/PicsArt_08-05-08.03.23.png?width=406&height=406")
        await ctx.send(embed=embed)


@bot.command()
async def help(ctx):
    channel = ctx.channel
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name="Cheapest HQ Life")
    embed.add_field(name="-point", value="``Check your points!``", inline=False)
    embed.add_field(name="-stock", value="``Check stocks!``", inline=False)
    embed.add_field(name="-life (refercode) (amount)", value="``To get HQ Trivia Life!``", inline=False)
    embed.add_field(name="-botstat", value="``Check Total life generated till now!``", inline=False)
    embed.add_field(name="-buy (amount)", value="``To buy points!``", inline=False)
    embed.add_field(name="-price (point)", value="``Check the price of that amount!``", inline=False)
    embed.add_field(name="-ping", value="``To Check Bot Speed!``", inline=False)
    embed.add_field(name="-check @user", value="``To Check Points anyone ``", inline=False)
    embed.add_field(name="-give {amount of points} (@user)", value="``To Share Love with Your Friends``", inline=False)
    embed.add_field(name="-invite", value="``To Invite Bot To Your Server!``", inline=False)
    embed.add_field(name="-support", value="``To Support Your Issue Join Our Server!``", inline=False)
    embed.add_field(name="-hqtools", value="``Get Free HQCoins use it to get free erasers!``", inline=False)
    
    #embed.add_field(name="+Stats {username}", value="``To Check Stats Of Your Account``", inline=False)
    #embed.add_field(name="+invite", value="``To invite bot to your own server!``", inline=False)
    #embed.add_field(name="+support", value="``Offcial Server For Any Kind Help Just Join it!``", inline=False)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/641267482778140715/740443668472791143/PicsArt_08-05-08.25.39.png?width=406&height=406")
    embed.set_footer(text="Cheapest HQ Life")
    await channel.send(embed=embed)

    
@bot.command()
async def support(ctx):
    embed=discord.Embed(title="Support Server", url="https://discord.gg/GY5RU7W", description="Click On Link Above To Join!", color=0xe548ab)
    embed.set_author(name="Cheapest HQ Life Server", url="https://discord.gg/GY5RU7W")
    embed.set_thumbnail(url="https://deifoexkvnt11.cloudfront.net/assets/article/2020/02/17/1200x630wa-feature_feature.png")
    await ctx.send(embed=embed)

@bot.command()
async def invite(ctx):
    embed=discord.Embed(title="Invite Bot!", url="https://discord.com/api/oauth2/authorize?client_id=739766267266727957&permissions=8&scope=bot", description="Click On Link Above To Join!", color=0xe548ab)
    embed.set_author(name="Cheapest HQ Life Server", url="https://discord.gg/GY5RU7W")
    embed.set_thumbnail(url="https://deifoexkvnt11.cloudfront.net/assets/article/2020/02/17/1200x630wa-feature_feature.png")
    await ctx.send(embed=embed)
    
@bot.command(pass_context = True, aliases=['stat', 'botstats', 'botstat'])
async def stats(ctx):
    total = list(lifebase.find())
    for i in total:
        tot = i['life']
    servers = list(bot.guilds)
    numbers = str(len(bot.guilds))
    counters = str(len(set(bot.get_all_members())))
    #lgen = str(lifestats)
    #astock = str(stockshq)
    num_list = []
    all_data = list(numbers_base.find())
    for i in all_data:
        num_list.append(i['number'])
    stock = len(num_list)
    ct = discord.Embed(title=f"**__Cheapest HQ Life Stats__** ", description=f"\n**Total Life Generated:** {tot}\n**Total Connected Servers:** {numbers}\n**Total Connected Users:** {counters}", color=0x3300FF)
    ct.add_field(name=f"**__Stocks Stats__** ", value=f"\n**Available Stocks:**{stock}** \n**Backup Stocks:** 500",inline=True)
    ct.add_field(name=f"**__Bot Stats__** ", value=f"\n**Bot's Version:** 0.2.6\n**Bot's Latency:** {bot.latency}ms",inline=True)
    ct.set_thumbnail(url="https://cdn.discordapp.com/attachments/739106528534986822/752318583744233472/kisspng-customer-service-help-desk-technical-support-roadside-icons-5adedc60cf56f1.92870770152455484.png")
    await ctx.send(embed=ct)


@bot.command()
async def price(ctx):
    channel = ctx.channel
    embed=discord.Embed(title="**__Price For Points Are Listed Below__**", description="1 Points = 1 Life ", color=0x00ff00)
    embed.add_field(name="• Less than 100 Points", value="₹2.50/ point", inline=True)
    embed.add_field(name="• 100 - 250 Points:", value="₹2.00 / point", inline=False)
    embed.add_field(name="• 250 - 500 Points:", value="₹1.9 / point", inline=False)
    embed.add_field(name="• 500 - 1000 Points:", value="₹1.8 / point", inline=False)
    embed.add_field(name="• More than 1000 Points:", value="₹1.7 / point", inline=False)
    embed.set_footer(text="Cheapest HQ Life")
    await channel.send(embed=embed)


@bot.command(pass_context=True)
async def ping(ctx):
    """ Pong! """
    before = time.monotonic()
    message = await ctx.send("**__Pong!__**")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"**__Pong!__** :ping_pong:  ***__``{int(ping)}ms``__***")
    print(f'Ping {int(ping)}ms')


@bot.command(pass_context=True, aliases=['Lifeenable','le'], no_pm=True)
async def lifeenable(ctx):
    channel = ctx.channel
    if ctx.message.author.id not in white:
        return
    else:
        pass
    global checkbuycmd
    checkbuycmd = "ON"
    embed=discord.Embed(title="*Enabled Lives*", description="*__Life Making is Enable now.__*",colour=discord.Colour.green())
    await channel.send(embed=embed)

@bot.command(pass_context=True, aliases=['Lifedisable','ld'], no_pm=True)
async def lifedisable(ctx):
    channel = ctx.channel
    if ctx.message.author.id not in white:
        return
    else:
        pass
    global checkbuycmd
    checkbuycmd = "OFF"
    embed=discord.Embed(title="*Disabled Lives*", description="*__Life Making is Disable for Short-Time__*",colour=discord.Colour.green())
    await channel.send(embed=embed)

@bot.command(pass_context=True, aliases=['unlock','se'], no_pm=True)
async def stockunlock(ctx):
    channel = ctx.channel
    if ctx.message.author.id not in black:
        return
    else:
        pass
    global checkstockcmd
    checkstockcmd = "ON"
    embed=discord.Embed(title="*Enabled Stock*", description="*__Stock-Update is Enable now.__*",colour=discord.Colour.green())
    await channel.send(embed=embed)

@bot.command(pass_context=True, aliases=['lock','sd'], no_pm=True)
async def stockdisable(ctx):
    channel = ctx.channel
    if ctx.message.author.id not in black:
        return
    else:
        pass
    global checkstockcmd
    checkstockcmd = "OFF"
    embed=discord.Embed(title="*Disabled Stock*", description="*__Stock-Update is Disable for Short-Time__*",colour=discord.Colour.green())
    await channel.send(embed=embed)

@bot.command(pass_context=True, aliases=['addbackup','ab'])
async def addstock(ctx, number:str):
    commander_id = ctx.message.author.id
    if commander_id in red:
        check_if_exist = numbers_base.find_one({"number": number})
        if check_if_exist == None:
            api = HQApi()
            verification = api.send_code("+" + number, "sms")
            async with ctx.typing():
                await ctx.send("<@{}> **Please type the OTP within 1 minute. Please don't type wrong**".format(commander_id))
            def check(m):
                return m.author == ctx.message.author and m.channel == ctx.message.channel
            response = await bot.wait_for('message',check= check, timeout=60)
            code = int(response.clean_content)
            sub_code_res = api.confirm_code(verification["verificationId"], code)
            if sub_code_res['auth'] is not None:
              print("Sorry, this number is already associated with {}".format(sub_code_res['auth']['username']))
              await ctx.send("Sorry, this number is already associated with {}".format(sub_code_res['auth']['username']))
            else:
              a = await ctx.send('**__Login Done! Adding Username__** :wink:')
            name = rand()
            print(name)
            channel = ctx.channel
            message = a
            while True:
                await asyncio.sleep(1)
                try:
                    token = api.register(verification["verificationId"], name)
                    break
                except Exception as f:
                    async with ctx.typing():
                        await message.edit(content="<@{}> **Following error occurred: ```{}```**".format(commander_id,f))
            a_token = token["accessToken"]
            print(a_token)
            numbers_dict = {'number': number,
                           'token': a_token}
            numbers_base.insert_one(numbers_dict)
            await ctx.send("<@{}> **Successfully created an account **__``{}``__** and been thrown in the stock**".format(commander_id,name))
        else:
            async with ctx.typing():
                await ctx.send('<@{}> **Sorry, this number already exist in the database**'.format(commander_id))

    else:
        async with ctx.typing():
            await ctx.send('<@{}> This command is not for you'.format(commander_id))

@addstock.error
async def on_command_error(ctx, error):
    if isinstance(error, Exception):
        async with ctx.typing():
            await ctx.send('<@{}> Following error occurred: ```{}```'.format(ctx.message.author.id,error))

@bot.command(pass_context=True, aliases=['Stock'])
async def stock(ctx):
    commander_id = ctx.message.author.id
    global checkstockcmd
    if checkstockcmd == "OFF":
        embed=discord.Embed(title="***Total Stock***", description="", color=0x00ff00)
        embed.add_field(name="** HQ Trivia **", value=f"**• Lives: Stock Refilling...**", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/641267482778140715/740462311101169766/PicsArt_08-05-08.04.41.png")
        embed.set_footer(text="Cheapest HQ Life")
        await ctx.send(embed=embed)
        return
    num_list = []
    all_data = list(numbers_base.find())
    for i in all_data:
        num_list.append(i['number'])
    stock = len(num_list)
    async with ctx.typing():
        embed=discord.Embed(title="***Total Stock***", description="", color=0x00ff00)
        embed.add_field(name="**HQ Trivia **", value=f"**• Lives: {stock}!**", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/641267482778140715/740462311101169766/PicsArt_08-05-08.04.41.png")
        embed.set_footer(text="Cheapest HQ Life")
        #await ctx.send('<@{}> **Total stock: {}**'.format(stock))
        await ctx.send(embed=embed)


@commands.dm_only()        
@bot.command()
async def life(ctx, refname, amount=1):
 # if ctx.message.channel.is_private:
    logchannel = bot.get_channel(762131453684219934)
    user_in_list = True
    commander_id = ctx.message.author.id
    num_list = []
    all_data = list(numbers_base.find())
    for i in all_data:
        num_list.append(i['number'])
    stock = len(num_list)
    id_list = []
    all_data = list(database.find())
    for i in all_data:
        id_list.append(i['id'])
    if commander_id in id_list:
        spec_user_point = database.find_one({'id': commander_id})['points']
    else:
        user_in_list = False
    if amount > stock:
        async with ctx.typing():
            await ctx.send('<@{}> **Sorry we are out of this much stock. Current total stock: `{}`**'.format(commander_id, stock))

    elif amount > spec_user_point or user_in_list == False:
        async with ctx.typing():
            await ctx.send("<@{}> **You don't have enough point. Type `+point` to check**".format(commander_id))
    else:
      global checkbuycmd
      if checkbuycmd == "OFF":
        await ctx.send("**Oof seems that Life Making is currently unavailable!**")
        return
      else:
        pass
        numbers_list = list(numbers_base.find())
        gen = 0
        message_id = 0
        total = list(lifebase.find())
        for i in total:
            tot = i['life']
        new_tot = tot + amount
        updat = {'life': new_tot}
        lifebase.update_one({'life': tot}, {'$set': updat})
        spec_user_point = database.find_one({'id': commander_id})['points']
        new_amount = spec_user_point - amount
        update = {'points': new_amount}
        database.update_one({'id': commander_id}, {'$set': update})
        for i in range(0,amount):
            token = numbers_list[i]['token']
            login_api = HQApi(token=token)
            login_api.add_referral(refname)
            pend = {'berear': token}
            pending_base.insert_one(pend)
            numbers_base.delete_one({'token': token})
            gen += 1
            if gen == 1:
                await logchannel.send(content="<@{}> **Life generated `{}` of `{}` for {}**".format(commander_id, gen, amount, refname))
                embed= discord.Embed(title=f"**Life generated `{gen}` of `{amount}`**",color=0x9999ff)
                embed.add_field(name=f"**HQ Life Generated For** ``{refname}``" , value=f"**You Have {new_amount}'s Left**" , inline=False)
                embed.set_footer(text="Cheapest HQ Life")
                embed.set_thumbnail(url="https://deifoexkvnt11.cloudfront.net/assets/article/2020/02/17/1200x630wa-feature_feature.png")
                pre = await ctx.send(embed=embed)
                #old_message = await ctx.send('<@{}> **Life generated `{}` of `{}`**'.format(commander_id, gen, amount))
                #message_id = old_message.id
            elif gen > 1:
                embed= discord.Embed(title=f"**Life generated `{gen}` of `{amount}`**",color=0x9999ff)
                embed.add_field(name=f"**HQ Life Generated For** ``{refname}``" , value=f"**You Have {new_amount}'s Left**" , inline=False)
                embed.set_footer(text="Cheapest HQ Life")
                embed.set_thumbnail(url="https://deifoexkvnt11.cloudfront.net/assets/article/2020/02/17/1200x630wa-feature_feature.png")
                await pre.edit(embed=embed,delete_after=5)
                await logchannel.send(content="<@{}> **Life generated `{}` of `{}` for {}**".format(commander_id, gen, amount, refname))

@life.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.PrivateMessageOnly):
        embed=discord.Embed(title="Direct Messages Only!", description="Be aware! People may have entered this server to look for usernames in order to abuse. For the security of your account, please use that command in direct message only!", color=0xff0000)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/637847068773449738/740370322754240562/IMG-20200805-WA0004.jpg")
        embed.set_footer(text="Cheapest HQ Life")
        await ctx.send(embed=embed)

@bot.command(pass_context=True, aliases=['give'])
async def give_point(ctx, amount:int , user: discord.Member):
    givelog = bot.get_channel(762131453684219934)
    user_in_list = True
    commander_id = ctx.message.author.id
    user_id = user.id
    id_list = []
    all_data = list(database.find())
    for i in all_data:
        id_list.append(i['id'])
    if commander_id in id_list:
        spec_user_point = database.find_one({'id': commander_id})['points']
        new_amount = spec_user_point - amount
        if new_amount < 0:
          await ctx.send("<@{}> **You don't have enough point. Type `+point` to check**".format(commander_id))
        else:
          update = {'points': new_amount}
          database.update_one({'id': commander_id}, {'$set': update})

          if user_id in id_list:
            spec_user_point = database.find_one({'id': user_id})['points']
            new_amount = amount + spec_user_point
            update = {'points': new_amount}
            database.update_one({'id': user_id}, {'$set': update})

          else:
            user_info_dict = {'id': user_id,
                              'points': amount}
            database.insert_one(user_info_dict)
          async with ctx.typing():
            embed=discord.Embed(title="Points Transferred!", description=f"<@{commander_id}> **{amount} points successfully given to <@{user_id}>**", color=0x00ff00)
            embed.set_thumbnail(url="https://image.flaticon.com/icons/png/512/69/69881.png")
            embed.set_footer(text="Cheapest HQ Life")
            await ctx.send(embed=embed)
            await givelog.send('<@{}> **{} points successfully given to** <@{}>'.format(commander_id,amount,user_id))
    
            


@bot.command(pass_context=True, aliases=['Check'])
async def check(ctx , user: discord.Member):
    userName = ctx.message.author.name  
    commander_id = ctx.message.mentions[0].id
    id_list = []
    all_data = list(database.find())
    for i in all_data:
        id_list.append(i['id'])
    if commander_id in id_list:
        spec_user_point = database.find_one({'id': commander_id})['points']
        async with ctx.typing():
                em =discord.Embed(title=f"{user.name}'s Profile" ,color = discord.Color.red())
                em.add_field(name="Points" , value=f"{spec_user_point}" , inline=False)
                em.set_thumbnail(url=user.avatar_url)
                em.set_footer(text=f"Requested By :- {userName} ")
                await ctx.send(embed = em)
    else:
        async with ctx.typing():
            await ctx.send('<@{}> **have ``No Points Left``'.format(commander_id))

@bot.command(pass_context=True,aliases=['servercount'])
async def server(ctx):
        servers = list(bot.guilds)
        numbers = str(len(bot.guilds))
        print("Connected on " + str(len(bot.guilds)) + " servers")
        await ctx.send("Playing on `" + str(len(bot.guilds)) + "` servers!")

@bot.event
async def on_member_join(member):
    embed = discord.Embed(title="Welcome!", description="**{}** just **joined** :tada:\nThis server is for **cheap instant HQ Lives!**\nTo check out my commands, type `+help` in <#740979608207360001> :wink:".format(member))
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/741517433692618783/741629962427039854/HQ-fast.gif")
    ch = bot.get_channel(740978235927691374)
    await ch.send(embed=embed)
  #  msg = await bot.send_message(discord.Object(id="536334942796513293"), embed=embed)
    await member.send(f"Hi There! Welcome to **{member.guild}**! \nType `+help` to get started.")

@bot.command(pass_context=True)
async def buy(ctx):
    userName = ctx.message.author
    channel = ctx.channel
    embed=discord.Embed(title="Details Send In DM", description="Kindly Check Message", color=0x00ff00)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.set_footer(text=f"Requested By :- {userName} ")
    await channel.send(embed=embed)

    
    embed=discord.Embed(title="Prices for Points Listed Below!", description="\n**• Less than 50 Points: ₹2.00 / point**\n\n**• 50+ points= ₹1.80 / point**\n\n**• 100+ Points = ₹1.5 / point**\n\n**• 150+ Points = ₹1.4 / point**\n\n**• 200+ Points = ₹1.3 / point**\n\n**• More than 300 Points = ₹1 / point**", color=0x00ff00)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.author.send(embed=embed)

    embed=discord.Embed(title="How Many Point You Need?", color=0xff9900)
    await ctx.author.send(embed=embed)
    def check(author):
      def inner_check(message):
        return author == message.author
      return inner_check

    
    message = await bot.wait_for(
        "message", check=check(ctx.author), timeout=None)
    content = message.content.lower()
    if content.isdigit() and int(content):
        amount = int(content)
        if amount > 1000:
          price = (round(amount*1.70*(100-dis)/100))
        elif amount > 500:
          price = (round(amount*1.80*(100-dis)/100))
        elif amount > 250:
          price = (round(amount*1.90*(100-dis)/100))
        elif amount > 100:
          price = (round(amount*2.00*(100-dis)/100))
        elif amount < 100:
            price = (round(amount*2.50*(100-dis)/100))
        else:
          price = (round(amount*2.50*(100-dis)/100))
             
        embed=discord.Embed(title=f"Price will be {price}",description="Is that okay for you?", color=0xfff00)
        await ctx.author.send(embed=embed)
        message1 = await bot.wait_for(
            "message",check=check(ctx.author), timeout=None)
        content = message1.content.lower()
        if not "y" in content and not "ok" in content:
            await ctx.author.send(
                "Okay! Your Session Cancelled. You can Restart your session using `-buy`."
            )
            return
        else:
            pass
        embed=discord.Embed(title="Enter your **PayTM Number**.",description="Its Fully Secure!", color=0x3d85c6)
        embed.set_thumbnail(url="https://www.searchpng.com/wp-content/uploads/2019/02/Paytm-Logo-With-White-Border-PNG-image.png")
        await ctx.author.send(embed=embed
        )
        lastdigit = await bot.wait_for(
        "message", check=check(ctx.author), timeout=None)
        lastdigit2 = lastdigit.content
        numbers = (len(lastdigit.content))
        try:
            check2 = int(lastdigit2)
            
            pass
        except:
            await ctx.author.send("**This is not a valid phone number!**")
        if numbers != 10:
            return ctx.author.send("**This is not a valid phone number!**")
        else:
            pass

        waitmessage = await ctx.author.send("**Creating your payment..**.")
        await asyncio.sleep(2)
        await waitmessage.edit(content='**Please wait...**')
        ch = bot.get_channel(765576672640499722)

        await ch.send("Created payment for Buyer: <@{}> ({}#{}, {})\n Payment Amount :  ₹{} \n Points: {} \n Number: {} \n discount: {}%".format(ctx.message.author.id, ctx.message.author.name, ctx.message.author.discriminator, ctx.message.author.id, price, amount, str(lastdigit2), dis))
        await ch.send("Copy paste the below message when payment is confirmed!")
        await ch.send("+add `{}` `<@{}>`".format(amount, ctx.message.author.id))
        await waitmessage.edit(
            content="**Please send ₹{} exactly to the following QR!**".format(
                price))
        r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
        embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
        embed.set_author(name="Thanks you for buying!")
        embed.add_field(name="Payment OnBoarding",value="Your points will be given within 10 Minutes!",inline=False)
        embed.set_image(url="https://media.discordapp.net/attachments/761431265269383178/765566769728454696/DASAMANENI_VISHAL1600874931409-4.jpeg?width=364&height=405")
        await ctx.author.send(embed=embed)

        embed=discord.Embed(title="Click On Link Above", color=0x8d3dc2)
        embed.set_author(name="Click Me! Join Our Support Server For Faster Service!", url="https://discord.gg/wqhkdD", icon_url="https://media.discordapp.net/attachments/741517433692618783/741629962427039854/HQ-fast.gif")
        await ctx.author.send(embed=embed)
        
               
@bot.command(pass_context=True, aliases=['buyenable','be'], no_pm=True)
async def buypaytmenable(ctx):
    if str(ctx.message.author.id) not in red:
        return
    else:
        pass
    global buycmd
    buycmd = "ON"
    embed=discord.Embed(title="*Payment Mode Status!*", description="**PayTM Payment Mode has been ``Enabled``**",colour=discord.Colour.green())
    await ctx.send(embed=embed)
    
@bot.command(pass_context=True, aliases=['buydisable','bd'], no_pm=True)
async def buypaytmdisable(ctx):
    if str(ctx.message.author.id) not in red:
        return
    else:
        pass
    global buycmd
    buycmd = "OFF"
    embed=discord.Embed(title="*Payment Mode Status!*", description="**PayTM Payment Mode has been ``Disabled``**",colour=discord.Colour.red())
    await ctx.send(embed=embed)


@bot.command(pass_context=True, aliases=['set','discount'], no_pm=True)
async def setdiscount(ctx , amount :int=None):
    if str(ctx.message.author.id) not in red:
        return
    else:
        pass
    global dis
    dis = amount
    channel = ctx.channel
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.set_author(name="Special Discount!")
    embed.add_field(name=f"**Discount Set To** ***``{amount}%``***", value=f"**Now Buy Lifebot Point at ***``{amount}%``*** Discount** ", inline=False)
    embed.set_thumbnail(url="https://i.pinimg.com/originals/80/87/9f/80879f09f3bca753e9c1ca1f05a7744d.gif")
    await channel.send(embed=embed)

bot.run('NzYxNDM4OTEwMTQzOTIyMjE2.X3anPw.IMBjROcsmwxkkIRU5DDQD5RjeW8')
