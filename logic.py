import random
round = 1


data = [[2, "Sophie"], [-2, "Will"], [-2, "Khris"], [2, "Bob"], [1, "Sarah"]]

#firstcheck
members = 4
if len(data) != members:
    print("invalid - not corresponding with number of members")


pairlist = []
tournament = (sorted(data))
if len(tournament) % 2 == 1:
    pairlist.append(tournament[len(tournament) - 1])
    tournament.pop()
if round == 1:
    random.shuffle(tournament)
    
    for i in range(int(len(tournament)/2)):
        pair = []
        pair.append(tournament[i*2])
        pair.append(tournament[(i*2)+1])
        pairlist.append(pair)
    print(pairlist) 
    
if round != 1:
    for i in range(int(len(tournament)/2)):
        pair = []
        pair.append(tournament[i*2])
        pair.append(tournament[(i*2)+1])
        pairlist.append(pair)
    print(pairlist)
            
Pairs = open("Pairs", "w")
for k in range(len(pairlist)):
    Pairs.write(str(pairlist[k]))
    Pairs.write("\n")
