import shelve

def print_shelve():
    for team in db:
        print('Team: '+ team)
        for key in db[team]:
            print('\n' + key + ':')
            for item in db[team][key]:
                print(item, end = ', ')
        print()

db = shelve.open('test.dat')
db['A']={
    'members': ['will', 'zhenhao', 'jason', 'xiang'],
    'wins': [0],
    'record': [0, 0, 0]
}
db['B']={
    'members': ['person1', 'person2', 'person 3'],
    'wins': [3],
    'record': [1, 1, 1]
}

#Add win/loss
print(db['A']['wins'][0])

db_copy = db['A']
db_copy['wins'][0] = db['A']['wins'][0]+1
db['A'] = db_copy

print(db['A']['wins'][0])

#Check round
print(len(db['A']['record']))
