import random

def create_Chart(DATA, Round):
    round = Round
    data = DATA
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
        #print(pairlist) 
    
    # [-2, -2, -2, -2, -2, 2, 3, 4]
    # randomize -2, -2, -2, -2,
    # [-2, 2] [3, 4]
    if round != 1:
        for i in range(int(len(tournament)/2)):
            pair = []
            pair.append(tournament[i*2])
            pair.append(tournament[(i*2)+1])
            pairlist.append(pair)
        #print(pairlist)
    
    return pairlist
    #Pairs = open("Pairs", "w")
    #for k in range(len(pairlist)):
        #Pairs.write(str(pairlist[k]))
        #Pairs.write("\n")
    #Pairs.close()
