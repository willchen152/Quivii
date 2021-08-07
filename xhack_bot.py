
import discord
from discord.ext import commands
import shelve
import logic
import pprint

client = commands.Bot(command_prefix = '!', help_command=None)

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

@client.command()
async def addmember(ctx, teamname, member):
    db = shelve.open('tournament.dat')
    
    db_copy = db[teamname]
    db_copy_members = db_copy['members']
    db_copy_members.append(member)
    db_copy['members'] = db_copy_members
    db[teamname] = db_copy

    await ctx.send("Added!")

@client.command()
async def removemember(ctx, teamname, member):
    db = shelve.open('tournament.dat')
    
    db_copy = db[teamname]
    db_copy_members = db_copy['members']
    db_copy_members.remove(member)
    db_copy['members'] = db_copy_members
    db[teamname] = db_copy

    await ctx.send("Removed!")



@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency*1000)}ms')

@client.command()
async def clear(ctx):
    db = shelve.open('tournament.dat')
    db.clear()
    await ctx.send('Cleared!')

@client.command()
async def help(ctx):
    embed=discord.Embed(title="Help Commands", color=0x87ff7b)
    embed.add_field(name = '!addteam', value = 'Adds a team where the first parameter is the team name and the second parameter are team members divided by a comma', inline = False)
    embed.add_field(name = '!removeteam', value = 'Removes a team where the first parameter is the team name')
    embed.add_field(name = '!addmember', value = ' adds a member to the team name where the first parameter is the team name and the second parameter is the member name', inline = False)
    embed.add_field(name = '!removemember', value = 'removes a member from the team name where the first parameter is the team name and the second parameter is the member name', inline = False)
    embed.add_field(name = '!clear', value = ' clears the shelve file, you may have to restart the program to access the new shelve file', inline = False)
    embed.add_field(name = '!nextround', value = 'creates a schedule for the nextround based on teams', inline = False)
    embed.add_field(name = '!update', value = 'updates a match where the 4 parameters seperated by a space are -> team1 name, 1/0, team2 name, 1/0', inline = False)
    embed.add_field(name = '!ping', value = 'checks the ping of the bot', inline = False)

    await ctx.send(embed = embed)

@client.command()
async def data(ctx):
    embed = discord.Embed(title="Team List", description="The teams comprise of:", color=0x87ff7b, inline = False)
    db = shelve.open('tournament.dat')
    for teams in db:
        embed.add_field(name = 'Team:', value = teams, inline = False)
        for key in db[teams]:
            embed.add_field(name = key, value = db[teams][key], inline = False)
    await ctx.send(embed=embed)

client.run
