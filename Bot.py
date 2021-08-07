import discord
from discord.ext import commands
import shelve

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Bot is ready')

@client.command()
async def test(ctx, name):
    await ctx.send(name)
    db = shelve.open('tournament.dat')
    db['person'] = name
    print(db['person'])
client.run('ODczMzU3MzAyMzk5MzkzODIy.YQ3PXw.teLyegmNl9Niq3nvXuO8xH4Zk44')