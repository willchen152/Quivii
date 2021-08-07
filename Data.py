import shelve

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

for team in db:
    print('Team: '+ team)
    for key in db[team]:
        print('\n' + key + ':')
        for item in db[team][key]:
            print(item, end = ', ')
    print()
