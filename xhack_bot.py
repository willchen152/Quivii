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
    db = shelve.open('tournament.dat')
    db['teams'] = []    

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
        'record': []
    }
    
        
    teams = db["teams"] #array of teamnames
    teams.append(teamname)
    db['teams'] = teams    
    
    await ctx.send("Added!")

    
    
    

@client.command()
async def nextround(ctx):
    db = shelve.open('tournament.dat')
    teams = db['teams']     
    round_num = []
    for team in teams:
        round_num.append(len(db[team]['record']))
    counter = 0
    mininum = min(round_num)
    for item in round_num:
        if item != mininum:
            counter += 1
    if counter > 0:
        await ctx.send(f'there are {counter} teams not done round.')
    else:
        
        data = []
        for team in range(len(teams)):
            team_name = teams[team]
            here_data = []
            here_data.append(db[team_name]['wins'][0]) 
            here_data.append(team_name)
            data.append(here_data)
        print(mininum + 1)
        print(data)
        print(sorted(data))
        schedule = logic.create_Chart(data, (mininum+1))
        print(schedule)
        await ctx.send("Done")
        db.close()    
  
    
@client.command()
async def removeteam(ctx, teamname):
    db = shelve.open('tournament.dat')
    
    del db[teamname]

    await ctx.send("Removed!")
    db = shelve.close()

async def inputd(prompt, ctx):
    await ctx.send(prompt) # Sending the initial message

    def check(m):
        return m.author == ctx.author

    # Waiting for the message
    message = await client.wait_for("message", check=check)
    return message

@client.command()
async def update(ctx):
    m = await inputd("Which teams would you like to update", ctx)
    teams = m.content
    teams = teams.split()
    print(teams)
    db = shelve.open('tournament.dat')
    # teamname W/L teamname2 W/L
    changeteam1 = db[teams[0]] #team name 1
    changeteam2 = db[teams[2]] #team name 2
    win1 = changeteam1['wins'][0]
    win2 = changeteam2['wins'][0]
    
    x = (win1 + int(teams[1]))
    y = (win2 + int(teams[3]))    
    changeteam1['wins'][0] = x
    changeteam2['wins'][0] = y
    
    recordchange = changeteam1['record']
    recordchange.append(teams[1])
    changeteam1['record'] = recordchange
    
    recordchange2 = changeteam2['record']
    recordchange2.append(teams[3])
    changeteam2['record'] = recordchange2 
    
    db[teams[0]] = changeteam1
    db[teams[2]] = changeteam2
    
    print(db[teams[0]])
    print(db[teams[2]])
