import discord
import asyncio
from discord.ext import commands

client = commands.Bot(command_prefix = '.')
global godId
godId = 0

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Junior"))
    print("we are ready!")

@client.command()
@commands.has_permissions(manage_messages=True)
async def newgod(ctx, *, id):
    global godId
    godId = int(id)
    await ctx.send('کاربر '+str(client.get_user(godId))+' بعنوان گاد تعیین شد و از الان به بات دسترسی داره')

@client.command()
@commands.has_permissions(manage_messages=True)
async def kill(ctx, member: discord.Member):
    #user = discord.Guild.get_member(user_id=int(member))
    await member.remove_roles(discord.utils.get(member.guild.roles, name="Alive"))
    await member.add_roles(discord.utils.get(member.guild.roles, name="Dead"))
    try:
        await member.edit(mute=True)
    except:
        pass
    await ctx.send('با '+member.display_name+' خداحافظی میکنیم')
    #await ctx.send(member.mention())

@client.command()
@commands.has_permissions(manage_messages=True)
async def night(ctx):
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('شب🌙'))
    for member in ctx.guild.members:
        await member.edit(voice_channel=None)
    await ctx.send('شب میشه 🌙 بخوابید')

@client.command()
@commands.has_permissions(manage_messages=True)
async def day(ctx):
    await client.change_presence(status=discord.Status.online, activity=discord.Game('روز☀️'))
    await ctx.send('☀️ قوقولی قوقو روز میشه')
    msg = "بیاید تو چنل "
    for member in ctx.guild.members:
        msg += member.mention + " "
        #await member.edit(voice_channel=discord.utils.get(ctx.guild.voice_channels, name='General'))
    await ctx.send(msg)

wait = 10
@client.command()
@commands.has_permissions(manage_messages=True)
async def vote(ctx):
    await ctx.send("آخر روزه و رأی گیری شروع میشه. برای رأی دادن، به مسیج حاوی اسم فرد ری اکشن بیلاخ نشون بدید")
    await asyncio.sleep(2)
    role = discord.utils.get(ctx.guild.roles, name="Alive")
    t = len(role.members)
    for member in ctx.guild.members:
        c = 0
        if role in member.roles:
            votes = await ctx.send(" 🔸 "+member.mention+" رأی گیری برای "+" 🔸")
            timer = await ctx.send(wait)
            for i in range(wait):
                await asyncio.sleep(1)
                await timer.edit(content=str(wait-i-1))
            vote_msg = await votes.channel.fetch_message(votes.id)
            reactionText = "رأی دهنده ها: "
            for r in vote_msg.reactions:
                users = await r.users().flatten()
                reactionText += ' - '.join([u.name for u in users])
                c = len(users)
            await ctx.send(reactionText)
            await timer.edit(content="کلا "+str(c)+" رأی "+str(int((c/t)*100))+"% ")


@client.command()
async def whoisgod(ctx):
    await ctx.send(str(client.get_user(godId)) if godId != 0 else "گاد هنوز تعیین نشده عزیزم")
    #await ctx.send("godId= "+str(godId))
    #await ctx.send("ctx.author.id= "+str(ctx.author.id))

def is_god(ctx):
    global godId
    return str(ctx.author.id) == str(godId)

@client.command()
@commands.check(is_god)
async def ping(ctx, *, com):
    await ctx.send('we have no ' + com + ' here dude')

@client.command() 
@commands.has_permissions(manage_messages=True)
async def kick(ctx, member: discord.member, * , reason): 
    await member.kick(reason=reason)

client.run('NzM2ODY3MDIwNDMxNDI1NTQ4.Xx1C4w.8ntM3Jh-Cbxx2vfPVZ9XT5_9CSg')