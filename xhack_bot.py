
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
async def create(ctx):
    m = await inputd("What is the tournament name?", ctx)

    if m.content != None:
        await ctx.send("good")
        tourn_name = str(m.content)
        db = shelve.open('tournament.dat')
        db['tourn_name'] = tourn_name
        print(db['tourn_name'])  
        
        m = await inputd("How many teams?", ctx)
    
        if m.content != None:
            await ctx.send("good")
            num_teams = int(m.content)     
            teamchart = []
            
            for team in range(num_teams):
                m = await inputd("What is team" + str(team + 1) + "'s name", ctx)
                if m.content != None:
                    await ctx.send(":)")
                    team_stats = []
                    team_stats.append(0)
                    team_stats.append(m.content)
                    teamchart.append(team_stats)
                    
                    m = await inputd("How many members are in the team?", ctx)
                    num_member = int(m.content)
                    
                    for mem in range(num_member):
                        m = await inputd("What is member" + str(mem + 1) + "'s name", ctx)
                        if m.content != None:
                            await ctx.send("Nice")
                            team_mem = m.content
                    continue
            db["teamchart"] = teamchart
            logic.creat_Chart(teamchart, 1)
            await ctx.send(str(teamchart))
        
    else:
        await ctx.send("bad")    
      

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