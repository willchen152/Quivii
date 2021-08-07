
import discord
from discord.ext import commands
import shelve
import logic

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Bot is ready')
    channel = client.get_channel(873356724722081832)
    await channel.send("Bot is online")

@client.command()
async def test(ctx):
    m = await inputd("What is your name?", ctx)
    name = m.content
    await ctx.send("Nice to meet you. The command for creating a tournament is -> " + '`!create`')
    db = shelve.open('tournament.dat')
    db['person'] = name
    print(db['person'])
      
@client.command()
async def addteam(ctx, teamname, members):
    db = shelve.open('tournament.dat')
    
    members = members.split(',')

    db[teamname] = {
        'members': members,
        'wins': [0],
        'record': [0]
    }
    await ctx.send("Added!")
    db = shelve.close()

@client.command()
async def removeteam(ctx, teamname):
    db = shelve.open('tournament.dat')
    
    del db[teamname]

    await ctx.send("Removed!")
    db = shelve.close()

#await channel.send(file=discord.File('my_image.png'))

async def inputd(prompt, ctx):
    await ctx.send(prompt) # Sending the initial message

    def check(m):
        return m.author == ctx.author

    # Waiting for the message
    message = await client.wait_for("message", check=check)
    return message



async def members(ctx, *, member):    
    await ctx.send(member)
    memberlist = []
    await ctx.send("These are the members: " + member)
client.run('ODczMzU3MzAyMzk5MzkzODIy.YQ3PXw.teLyegmNl9Niq3nvXuO8xH4Zk44')    
