import discord
from discord.ext import commands
import shelve
import logic
import os
from keep_alive import keep_alive

my_secret = os.environ['token']

my_secret = os.environ['token']

client = commands.Bot(command_prefix = '!', help_command=None)

@client.event
async def on_ready():
    print('Bot is ready')
    channel = client.get_channel(873356724722081832)
    await channel.send("Bot is online")

@client.command()
async def addteam(ctx, teamname, members):
    db = shelve.open('tournament.dat')
    
    members = members.split(',')

    db[teamname] = {
        'members': members,
        'wins': [0],
        'record': []    
    }
    
    await ctx.send("Added!")

@client.command()
async def nextround(ctx):
    db = shelve.open('tournament.dat')
    round_num = []
    for teams in db:
        
        # get slice object to slice Python
        text = 'record'      
        print(db[teams])
        #print("record: ", len(db[teams]['record']))
        x = (len(db[teams][text]))
        round_num.append(x)
    counter = 0
    mininum = min(round_num)
    print("round num: ", round_num)
    for item in round_num:
        if item != mininum:
            counter += 1
    if counter > 0:
        await ctx.send(f'there are {counter} teams not done round.')
    else:
        embed = discord.Embed(title="Matches", description=" ", color=0x87ff7b, inline = False)
        
        data = []
        for teams in db:
            here_data = []
            here_data.append(db[teams]['wins'][0]) 
            here_data.append(teams)
            data.append(here_data)
        print(mininum + 1)
        print(data)
        print(sorted(data))
        schedule = logic.create_Chart(data, (mininum+1))
        print(schedule)
        if len(round_num) % 2 == 1:
            embed.add_field(name = 'Pass:', value = str(schedule[0][1]), inline = False)
            text = (schedule[0][1])
            byeteam = db[text]
            wincount = byeteam['wins'][0]
            wincount += 1
            byeteam['wins'][0] = wincount
            record = byeteam['record']
            record.append(1)
            byeteam['record'] = record
            db[text] = byeteam
            schedule.pop(0)
        print(schedule)
        for i in range(len(schedule)):
            embed.add_field(name = f'Match {i+1}:', value = str(schedule[i][0][1]) + " vs " + str(schedule[i][1][1]), inline = False)
        await ctx.send(embed = embed)
        db.close()    
  
@client.command()
async def removeteam(ctx, teamname):
    db = shelve.open('tournament.dat')
    
    del db[teamname]

    await ctx.send("Removed!")
    db = shelve.close()


@client.command()
async def update(ctx, team1, result1, team2, result2):
    teams = [team1, result1, team2, result2]
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
    recordchange.append(int(teams[1]))
    changeteam1['record'] = recordchange
    
    recordchange2 = changeteam2['record']
    recordchange2.append(int(teams[3]))
    changeteam2['record'] = recordchange2 
    
    db[teams[0]] = changeteam1
    db[teams[2]] = changeteam2
    
    print(db[teams[0]])
    print(db[teams[2]])

    await ctx.send('Updated')
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
    embed = discord.Embed(title="Team List", description="The teams comprise of:", color=0x87ff7b, inline = True)
    db = shelve.open('tournament.dat')
    for teams in db:
        embed.add_field(name = 'Team:', value = teams, inline = False)
        for key in db[teams]:
            embed.add_field(name = key, value = db[teams][key], inline = True)
    await ctx.send(embed=embed)

keep_alive()

my_secret = os.environ['token']
client.run(my_secret)
