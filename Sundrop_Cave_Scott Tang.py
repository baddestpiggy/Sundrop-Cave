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
pickaxe_price = [50, 150] # 50 is copper, 150 is gold

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

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
            
            if plr_y + y < 0 or plr_x + x < 0: #checks if player is on the top or leftmost border
                continue
            if plr_y + y > len(fog) or plr_x+x > len(fog[0]): #checks if player is on rightmost or bottommost border
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
    player['day'] = 1
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['name'] = ''
    player['backpackslots'] = 10
    player['pickaxelevel'] = 1
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
    
    for x in range(-1,2,1):
        print("|",end = '')
        for y in range(-1,2,1):
            
            if (plr_y + y < 0 or plr_x + x < 0) or (plr_y + y > len(game_map) or plr_x + x > len(game_map)): #checks if player is on borders
                print("#",end = '')
            else:
                print(game_map[y][x],end = '')
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
    # TODO: Show Day
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
        elif townchoice.lower() == "v":
            print('saving tha game')
        elif townchoice.lower() == "q":
            return "Exit"
    
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
    print(game_map)
    if main_choice == "Exit":
        break
    else:
        town_action = town_menu_actions(game_map,fog,player)
        if town_action == "Exit":
            continue
        elif town_action == "Enter":
            print("Entering tha mine")
        
