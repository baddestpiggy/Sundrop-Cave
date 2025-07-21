from random import randint

player = {}
game_map = []
fog = [] #copying the game map ig but instead using '?' for fog and ' ' for cleared fog

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}

mineral_dropcount = {'C': [1,5], 'S': [1,3], 'G': [1,2]}

pickaxe_price = [50, 150] # 50 is copper, 150 is gold

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
            
            if (plr_y + y < 0 or plr_x + x < 0) or (plr_y + y > len(fog) or plr_x+x > len(fog[0])): #checks if player is on the top or leftmost border or rightmost or bottommost border
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
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['name'] = ''
    player['backpackslots'] = 10
    player['pickaxelevel'] = 1
    player['ores'] = []


    clear_fog(fog, player)
    return game_map
    
# This function draws the entire map, covered by the fof
def draw_map(game_map:list, fog:list, player:dict):
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
            elif rowindex == plr_y and elementindex == plr_x:
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
            
            if (plr_y + y < 0 or plr_x + x < 0) or (plr_y + y > len(game_map) or plr_x + x > len(game_map)): #checks if player is on borders
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
    print("(B)ackpack upgrade to carry {} items for {} GP".format(backpackslots+2,backpackslots*2))
    print("(L)eave shop")
    print("-----------------------------------------------------------")
    print("GP: {}")
    print("-----------------------------------------------------------")
    return
# This function shows the information for the player
def show_information(player):
    print("----- Player Information -----")
    print("Name: {}")
    print("Portal position: {}")
    print("Pickaxe level: {} {}")
    print("------------------------------")
    print("GP: {}")
    print("Steps taken: {}")
    print("------------------------------")


    return

# This function saves the game
def save_game(game_map, fog, player):
    # save map
    # save fog
    # save player
    return
        
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    # load fog
    # load player
    return

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
#    print("(H)igh scores")
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

        return "",game_map
    elif menuchoice.lower() == "l":
        
        return
    elif menuchoice.lower() == "q":
        
        return 'Exit',[]

def town_menu_actions(game_map,fog,player:dict):
    
    while True:

        show_town_menu(player["day"])
        townchoice = input("Your choice? ")
        print("\n")
        if townchoice.lower() == "b": #TODO: next time make option to upgrade pickaxe
            while True:
                buy_stuff(player)
                buy_choice = input("Your choice? ")
                if buy_choice.lower() == "b":
                    if player["GP"] >= player["backpackslots"]:
                        player["backpackslots"] += 2
                        print("Congratulations! You can now carry {} items!".format(player["backpackslots"]))
                        continue
                elif buy_choice.lower() == 'q':
                    break
            
        elif townchoice.lower() == "i":
            show_information(player)
        elif townchoice.lower() == "m":
            draw_map(game_map,fog,player)

        elif townchoice.lower() == "e":
            return "Enter"
        elif townchoice.lower() == "v": #TODO: save game
            print('saving tha game')
        elif townchoice.lower() == "q":
            return "Exit"
    
def show_mining_menu(game_map,fog,player):
    turns = player['turns']
    backpackslots = player['backpackslots']
    numofores = len(player['ores'])
    steps = player['steps']
    print("DAY {}".format(str(player['day'])))
    draw_view(game_map,fog,player)
    print("Turns left: {}   Load: {}/{}   Steps: {}".format(turns,numofores,backpackslots,steps))
    print("(WASD) to move\n(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu")

def action_mining_menu(game_map,fog,player):
    while True:
        show_mining_menu(game_map,fog,player)
        mineaction = input("Action? ")
        print("\n")
        if movement.get(mineaction.lower()): #movement
            movementdirection = movement.get(mineaction.lower())
            dir_y = movementdirection[0]
            dir_x = movementdirection[1]
            plr_y = player['y']
            plr_x = player['x']
            player['turns'] -= 1
            if (plr_y + dir_y < 0 or plr_x + dir_x < 0) or (plr_y + dir_y > len(game_map) or plr_x + dir_x > len(game_map)): #checks if player is gna move onto a border    
                print("You cant move there brochacho")
            else: #valid movement
                
                futureposition = game_map[plr_y+dir_y][plr_x+dir_x]    
                if futureposition == "T":        
                    return "Town"
                
                elif mineral_dropcount.get(futureposition):        
                    oresdropped = randint(mineral_dropcount.get(futureposition)[0],mineral_dropcount.get(futureposition)[1])        
                    if len(player['ores']) + oresdropped > player['backpackslots']:                
                        oresdropped = player['backpackslots'] - len(player['ores'])
                                
                    for i in range(oresdropped):                    
                        player['ores'].append(oresdropped)
                
                    game_map[plr_y+dir_y][plr_x+dir_x] = " "
                
                    print("You mined {} pieces of {}.".format(str(oresdropped),mineral_names[futureposition]))                
                    if len(player['ores']) < player['backpackslots']:                    
                        print("You can carry {} more piece(s).".format(player['backpackslots'] - len(player['ores'])))                
                    else:                    
                        print("Your backpack is full.")
                player['x'] = plr_x+dir_x
                player['y'] = plr_y+dir_y

                clear_fog(fog,player)
            if player['turns'] == 0:
                print("You're exhausted.")
                print("You place your portal stone here and zap back to town.")
                return "Town"
        else: #others
            if mineaction.lower() == "m":
                draw_map(game_map,fog,player)
            elif mineaction.lower() == "i":
                show_information(player)
            elif mineaction.lower() == "p":
                print("-----------------------------------------------------")
                print("You place your portal stone here and zap back to town.")
    


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





while True:
    main_choice,game_map = main_menu(game_map,fog,player)
    
    if main_choice == "Exit":
        break
    else:
        while True:
            player['day'] += 1
            town_action = town_menu_actions(game_map,fog,player)
            if town_action == "Exit":
                break
            elif town_action == "Enter":
                print("---------------------------------------------------")
                print("{:^51}".format("DAY",str(player['day'])))
                print("---------------------------------------------------")
                mining_action = action_mining_menu(game_map,fog,player)
                if mining_action == "Town":
                    continue
        

        
