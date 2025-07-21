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
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    
    map_file = open(filename, 'r')
    
    global MAP_WIDTH
    global MAP_HEIGHT
    
    map_struct.clear()
    
    # TODO: Add your map loading code here (done)
    map_file = map_file.read()
    map_struct = map_file.split("\n")

    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog:list, player: dict):
    plr_x = player.get("x")
    plr_y = player.get("y")
    #3x3 square around player coordinates is -1,-1
    #need check if clearing fog is outside of map range also
    for x in range(-1,1,1):
        for y in range(-1,1,1):
            if plr_y + y < 0 or plr_x + x < 0: #checks if player is on the top or leftmost border
                continue
            if plr_y + y > len(fog) or plr_x+x > len(fog[0]): #checks if player is on rightmost or bottommost border
                continue
            
            if fog[plr_y + y][plr_x + x] == '?':
                fog[plr_y + y][plr_x + x] = ' ' #clears the jawn

    return

def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)

    # TODO: initialize fog
    
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

    player['backpackslots'] = 10

    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    return

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    return

# This function shows the information for the player
def show_information(player):
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
    print("DAY {}".format(str(day)))
    # TODO: Show Day
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")
            

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

    show_main_menu()
    menuchoice = input("Your choice? ")
    if menuchoice.lower() == "n":
        #day = 1
        #backpackslots = 10

        player = {}
        initialize_game()

        name = input("Greetings, miner! What is your name? ")
        print("Pleased to meet you, {}. Welcome to Sundrop Town!\n".format(name))
        print(show_town_menu(day))
        townchoice = input("Your choice? ")
        if townchoice.lower() == "b":
    
        elif townchoice.lower() == "i":

        elif townchoice.lower() == "m":

        elif townchoice.lower() == "e":

        elif townchoice.lower() == "v":
            
        elif townchoice.lower() == "q":
            continue
    elif menuchoice.lower() == "l":
        
    elif menuchoice.lower() == "q":
        break