from random import randint

player = {}
game_map = []
fog = [] #copying the game map ig but instead using '?' for fog and ' ' for cleared fog
highscores = []
MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}

mineral_dropcount = {'C': [1,5], 'S': [1,3], 'G': [1,2]}

pickaxe_price = [50, 150] # 50 is silver, 150 is gold

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

movement = {"w" : [-1,0], "a" : [0,-1], "s" : [1,0], "d" : [0,1]}

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    with open(filename, 'r') as map_file:
        global MAP_WIDTH
        global MAP_HEIGHT
    
        map_struct.clear()
    
        # TODO: Add your map loading code here (done)
        map_file = map_file.read()
        map_struct = map_file.split("\n")
        for i in range(len(map_struct)):
            map_struct[i] = list(map_struct[i])
        MAP_WIDTH = len(map_struct[0])
        MAP_HEIGHT = len(map_struct)

        return map_struct
    

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog:list, player: dict):
    plr_x = player.get("x")
    plr_y = player.get("y")
    if plr_x == None or plr_y == None:
        return
    #3x3 square around player coordinates is -1,-1
    #need check if clearing fog is outside of map range also
    for x in range(-1,2,1):
        for y in range(-1,2,1):
            
            if (plr_y + y < 0 or plr_x + x < 0) or (plr_y + y >= len(fog) or plr_x+x >= len(fog[0])): #checks if player is on the top or leftmost border or rightmost or bottommost border
                continue
        
            
            if fog[plr_y + y][plr_x + x] == '?':
                fog[plr_y + y][plr_x + x] = ' ' #clears the jawn

    return

def initialize_game(game_map:list, fog: list, player:dict):
    # initialize map
    game_map = load_map("level1.txt", game_map)

    # TODO: initialize fog (done)
    
    for x in range(MAP_HEIGHT):
        fog.append([])
        for y in range(MAP_WIDTH):
            fog[x].append("?")
    
    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player['x'] = 0
    player['y'] = 0
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['name'] = ''
    player['backpackslots'] = 10
    player['pickaxelevel'] = 1
    player['ores'] = []
    player['minerals'] = {"C" : 0, "S" : 0, "G" : 0}
    player['TotalGP'] = 0
    

    clear_fog(fog, player)
    return game_map

def getnumberofminerals(player):
    total = 0
    for _,i in player['minerals'].items():
        total += i
    return total
# This function draws the entire map, covered by the fof
def draw_map(game_map:list, fog:list, player:dict,InTown: bool):
    plr_x = player.get("x")
    plr_y = player.get("y")
    if plr_x == None or plr_y == None:
        return
    horizontalborder = "+"+"-"*len(game_map[0])+"+"
    print(horizontalborder)
    for rowindex in range(len(game_map)):
        row = game_map[rowindex]
        print("|",end = '')
        for elementindex in range(len(row)):
            element = row[elementindex]
            if fog[rowindex][elementindex] == "?":
                element = "?"
            elif (rowindex == plr_y and elementindex == plr_x):
                element = "P"
                if not InTown:
                    
                    element = "M"
            if InTown and rowindex == 0 and elementindex == 0:
                element = "M"
                
            
            print(element,end = '')
        print("|")
    print(horizontalborder)
    return

# This function draws the 3x3 viewport
def draw_view(game_map:list, fog:list, player:dict):
    plr_x = player.get("x")
    plr_y = player.get("y")
    if plr_x == None or plr_y == None:
        return
    #print border
    horizontalborder = "+"+"-"*3+"+"
    print(horizontalborder)
    
    for y in range(-1,2,1):
        print("|",end = '')
        for x in range(-1,2,1):
            
            if (plr_y + y < 0 or plr_x + x < 0) or (plr_y + y >= len(game_map) or plr_x + x >= len(game_map[0])): #checks if player is on borders
                print("#",end = '')
            else:
                if y == 0 and x == 0:
                    print("M",end = '')
                else:
                    print(game_map[plr_y+y][plr_x+x],end = '')
        print("|")
    print(horizontalborder)
    return

def buy_stuff(player:dict):
    backpackslots = player['backpackslots']
    print("----------------------- Shop Menu -------------------------")
    if not(player['pickaxelevel'] == len(minerals)-1):
        print("(P)ickaxe upgrade to Level {} to mine {} ore for {} GP".format(str(player['pickaxelevel']+1),minerals[player['pickaxelevel']],str(pickaxe_price[player['pickaxelevel']-1])))
    
    print("(B)ackpack upgrade to carry {} items for {} GP".format(backpackslots+2,backpackslots*2))
    print("(L)eave shop")
    print("-----------------------------------------------------------")
    print("GP: {}".format(player["GP"]))
    print("-----------------------------------------------------------")
    return
# This function shows the information for the player
def show_information(player):
    print("----- Player Information -----")
    print("Name: {}".format(player["name"]))
    print("Portal position: ({},{})".format(player["x"],player["y"]))
    #print("Pickaxe level: {} {}")
    print("------------------------------")
    print("Load: {} / {}".format(getnumberofminerals(player),player['backpackslots']))
    print("------------------------------")
    print("GP: {}".format(player['GP']))
    print("Steps taken: {}".format(player['steps']))
    print("------------------------------")


    return

# This function saves the game
def save_game(game_map, fog, player):
    # save map as game_map.txt
    with open("game_map.txt","w") as mapsavefile:
        writtenstring = ''   
        for rowindex in range(len(game_map)):
            row = game_map[rowindex]
                     
            for elementindex in range(len(row)):
                element = row[elementindex]
                writtenstring += element
            if rowindex != len(game_map)-1:

                writtenstring += '\n'
        mapsavefile.write(writtenstring)
        print("Save Success!")
    
                           
            
    # save fog as fog.txt
    with open("fog.txt","w") as fogsavefile:
        
        writtenstring = ''
        for rowindex in range(len(fog)):
            row = fog[rowindex]
                        
            for elementindex in range(len(row)):
                element = row[elementindex]
                writtenstring += element
            if rowindex != len(fog)-1:

                writtenstring += '\n'
            
        fogsavefile.write(writtenstring)
    # save player as player.txt
    with open("player.txt","w") as playersavefile:
        writtenstring = ''
        for stat,value in player.items():
            writtenstring += '{} - {}\n'.format(stat, value)
        playersavefile.write(writtenstring)
    return
        
def typeconverter(value:str):
    if value.isdigit(): #integer
        return int(value)
    elif value[0] == '[' and value[-1] == "]": #list
        value = value.replace("[","")
        value = value.replace("]","")
        outputlist = value.split(', ')
        if len(outputlist) == 1 and outputlist[0] == '':
            return []


        return outputlist
    elif value[0] == '{' and value[-1] == '}': #dict
        
        outputdict = {}
        value = value.replace("{","")
        value = value.replace("}","")
        value = value.replace("'","")
        value = value.split(', ')
        
        for keyvaluepair in value:
            keyvaluepair = keyvaluepair.split(": ")
            outputdict[keyvaluepair[0]] = int(keyvaluepair[1])

        return outputdict
    else:
        return value
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    game_map = load_map('game_map.txt',game_map)
    
    # load fog
    with open('fog.txt','r') as fogsave:
        fog = fogsave.read().split('\n')
        for i in range(len(fog)):
            fog[i] = list(fog[i])
        
    # load player
    with open('player.txt','r') as playersave:
        playersave = playersave.read().split('\n')
        for row in playersave:
            row = row.split(' - ')
            if len(row) != 2:
                
                continue
            else:
                row[1] = typeconverter(row[1])
                player[str(row[0])] = row[1]
    
    return game_map, fog

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu(day):
    print("\nDAY {}".format(str(day)))
    # TODO: Show Day(done)
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")
       
def main_menu(game_map,fog,player):
    show_main_menu()
    menuchoice = input("Your choice? ")
    if menuchoice.lower() == "n":
        game_map = initialize_game(game_map,fog,player)

        name = input("Greetings, miner! What is your name? ")
        print("Pleased to meet you, {}. Welcome to Sundrop Town!".format(name))

        player['name'] = name

        return "",game_map,fog
    elif menuchoice.lower() == "l":
        game_map,fog = load_game(game_map,fog,player)
        return "", game_map,fog
    elif menuchoice.lower() == "q":
        
        return 'Exit','',''
    elif menuchoice.lower() == 'h':
        display_high_scores(highscores)
        return 'Continue',[],[]
    else:
        print("Invalid input. Please enter a valid choice.")
        return 'Continue',[],[]
def town_menu_actions(game_map,fog,player:dict):
    
    while True:
        sell_ores(player)
        if player['GP'] >= 500:
            print("-------------------------------------------------------------")
            print("Woo-hoo! Well done, {}, you have {} GP!".format(player['name'],player["GP"]))
            print("You now have enough to retire and play video games every day.")
            print("And it only took you {} days and {} steps! You win!".format(player['day'],player['steps']))
            print("-------------------------------------------------------------")
            save_high_scores(player)
            return 'Exit'
        show_town_menu(player["day"])
        townchoice = input("Your choice? ")
        print("")
        if townchoice.lower() == "b": #TODO: next time make option to upgrade pickaxe
            while True:
                buy_stuff(player)
                buy_choice = input("Your choice? ")
                if buy_choice.lower() == "b":
                    if player["GP"] >= player["backpackslots"] *2:
                        
                        print("Congratulations! You can now carry {} items!".format(player["backpackslots"]+2))
                        player["GP"] -= player["backpackslots"] *2
                        player["backpackslots"] += 2
                        continue
                    else:
                        print("Sorry. You do not have enough GP to upgrade your backpack.")
                        continue
                elif buy_choice.lower() == 'p':
                    if not(player['pickaxelevel'] == len(minerals)-1):

                        if player["GP"] >= pickaxe_price[player['pickaxelevel']-1]:
                            print("Congratulations! You can now mine {}!".format(minerals[player['pickaxelevel']]))
                            player["GP"] -= pickaxe_price[player['pickaxelevel']-1]
                            player['pickaxelevel'] += 1
                            continue
                        else:
                            print("Sorry. You do not have enough GP to upgrade your pickaxe.")
                            continue
                elif buy_choice.lower() == 'l':
                    break
                else:
                    print("Invalid input. Please enter a valid choice.")
        elif townchoice.lower() == "i":
            show_information(player)
        elif townchoice.lower() == "m":
            draw_map(game_map,fog,player,True)

        elif townchoice.lower() == "e":
            return "Enter"
        elif townchoice.lower() == "v": #TODO: save game
            
            save_game(game_map,fog,player)
        elif townchoice.lower() == "q":
            return "Exit"
        else:
            print("Invalid input. Please enter a valid choice.")
            continue
def show_mining_menu(game_map,fog,player):
    turns = player['turns']
    backpackslots = player['backpackslots']
    numofminerals = getnumberofminerals(player)
    steps = player['steps']
    print("DAY {}".format(str(player['day'])))
    draw_view(game_map,fog,player)
    print("Turns left: {}   Load: {}/{}   Steps: {}".format(turns,numofminerals,backpackslots,steps))
    print("(WASD) to move\n(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu")

def action_mining_menu(game_map,fog,player):
    while True:
        show_mining_menu(game_map,fog,player)
        mineaction = input("Action? ")
        print("")
        if movement.get(mineaction.lower()): #movement
            if player['turns'] == 0:
                print("You're exhausted.")
                print("You place your portal stone here and zap back to town.")
                return "Town"
            
            movementdirection = movement.get(mineaction.lower())
            dir_y = movementdirection[0]
            dir_x = movementdirection[1]
            plr_y = player['y']
            plr_x = player['x']
            player['turns'] -= 1
            player['steps'] += 1
            if (plr_y + dir_y < 0 or plr_x + dir_x < 0) or (plr_y + dir_y >= len(game_map) or plr_x + dir_x >= len(game_map[0])): #checks if player is gna move onto a border    
                print("You cant move there brochacho")
            else: #valid movement
                
                futureposition = game_map[plr_y+dir_y][plr_x+dir_x]    
                if futureposition == "T":        
                    player['x'] = plr_x+dir_x
                    player['y'] = plr_y+dir_y
                    
                    return "Town"
                
                elif mineral_dropcount.get(futureposition):        
                    oresdropped = randint(mineral_dropcount.get(futureposition)[0],mineral_dropcount.get(futureposition)[1])        
                    numofminerals = getnumberofminerals(player)
                    mineralname = mineral_names[futureposition]
                    if numofminerals == player['backpackslots']:
                        print("Your backpack is full. You can't mine that.")
                        continue
                    if player['pickaxelevel'] < minerals.index(mineralname)+1: #if pickaxe level is too low
                        print("Your pickaxe level is too low. You can't mine that.")
                        continue

                    if numofminerals + oresdropped > player['backpackslots']:     #if randomly generated quantity of ore exceeds backpack size           
                        oresdropped = player['backpackslots'] - numofminerals
                               
                    player['minerals'][futureposition] += oresdropped
                
                    game_map[plr_y+dir_y][plr_x+dir_x] = " "
                
                    print("You mined {} pieces of {}.".format(str(oresdropped),mineral_names[futureposition]))                
                    
                    if numofminerals + oresdropped < player['backpackslots']:                    
                        print("You can carry {} more piece(s).".format(player['backpackslots'] - (numofminerals + oresdropped)))               
                    else:                    
                        print("Your backpack is full.")
                player['x'] = plr_x+dir_x
                player['y'] = plr_y+dir_y

                clear_fog(fog,player)
            
        else: #others
            if mineaction.lower() == "m":
                draw_map(game_map,fog,player,False)
            elif mineaction.lower() == "i":
                show_information(player)
            elif mineaction.lower() == "p":
                print("-----------------------------------------------------")
                print("You place your portal stone here and zap back to town.")
                return "Town"
            else:
                print("Invalid input. Please enter a valid choice.")
                continue
    
def sell_ores(player):
    totalmineralssold = 0
    for mineral,numofminerals in player['minerals'].items():
        totalmineralssold += numofminerals
        if numofminerals == 0:
            continue
        mineral_name = mineral_names[mineral]
        mineral_price = prices[mineral_name]
        minprice = mineral_price[0]
        maxprice = mineral_price[1]
        mineral_cost = 0
        for i in range(numofminerals):
            mineral_cost += randint(minprice,maxprice)
        
        print("You sell {} {} ore for {} GP.".format(str(numofminerals),mineral_name,str(mineral_cost)))    
        player["GP"] += mineral_cost
        player['TotalGP'] += mineral_cost
    if totalmineralssold != 0:
        player['minerals'] = {"C" : 0, "S" : 0, "G" : 0}
        print("You now have {} GP!".format(str(player["GP"])))
    
    return


#format of highscores for each line will be 'name, days, steps, Total GP'
def read_high_scores(highscorelist):
    with open('high_scores.txt','r') as highscorefile:
        highscorefile = highscorefile.read().split("\n") #splits individual high scores by newline
        
        if highscorefile == ['']:
            
            return []
        for i in highscorefile:
            
            i = i.split(', ')
            
            if len(i) == 4:
                
                highscorelist.append(i)
                
        return highscorelist

def display_high_scores(highscores):
    
    if len(highscores) == 0:
        print("There are no high scores yet.")
        return
    print("{:<20}{:<10}{:<10}{:<10}".format('   Name', 'Days', 'Steps', 'Total GP'))
    count = 1
    for score in highscores:
        print("{:<20}{:<10}{:<10}{:<10}".format(str(count)+'. '+score[0].replace("'",''), score[1], score[2], score[3]))
        count += 1
    return
def save_high_scores(player): #assuming that high scores are sorted beforehand
    replacedindex = -1
    
    for scoreindex in range(len(highscores)):
        score = highscores[scoreindex]
        if player['day'] < int(score[1]): #comparing days
            replacedindex = scoreindex
            break
        elif player['day'] == int(score[1]):
            if player['steps'] < int(score[2]):
                replacedindex = scoreindex
                break
            elif player['steps'] == int(score[2]):
                if player['TotalGP'] > int(score[3]):
                    replacedindex = scoreindex
                    break
    if replacedindex >= 0:

        if len(highscores) < 5:
            highscores.insert(replacedindex,[player['name'],player['day'],player['steps'],player["TotalGP"]])
        else:
            highscores[replacedindex] = [player['name'],player['day'],player['steps'],player["TotalGP"]]
    if len(highscores) == 0:
        highscores.append([player['name'],player['day'],player['steps'],player["TotalGP"]])
    with open("high_scores.txt",'w') as highscorefile:
        writetext = ''
        for score in highscores:
            score = str(score)
            score = score.replace('[','')
            score = score.replace(']','')
            score = score.replace("'",'')
            score = score.replace('"','')
            writetext += score+'\n'
        highscorefile.write(writetext)
#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!



highscores = read_high_scores(highscores)

while True:
    main_choice,game_map,fog = main_menu(game_map,fog,player)
    
    if main_choice == "Exit":
        break
    elif main_choice == "Continue":
        continue
    else:
        while True:
            player['day'] += 1
            town_action = town_menu_actions(game_map,fog,player)
            if town_action == "Exit":
                break
            
            elif town_action == "Enter":
                print("---------------------------------------------------")
                print("{:^51}".format("DAY "+str(player['day'])))
                print("---------------------------------------------------")
                mining_action = action_mining_menu(game_map,fog,player)
                if mining_action == "Town":
                    player['turns'] = TURNS_PER_DAY
                    continue
        

        
