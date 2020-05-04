import pyautogui as gui
from PIL import Image
import random
import time
import pdb

class Minefield:
    def __init__(self, width, height, tiles):
        self.width = width
        self.height = height
        self.tiles = tiles
        
class Tile:
    def __init__(self, index, position, value):
        self.index = index
        self.position = position
        self.value = value

all_tiles = {
        '_': Image.open('Images/unseen.png'),
        0: Image.open('Images/none.png'),
        1: Image.open('Images/1.png'),
        2: Image.open('Images/2.png'),
        3: Image.open('Images/3.png'),
        4: Image.open('Images/4.png'),
        5: Image.open('Images/5.png'),
        6: Image.open('Images/6.png'),
        'b': Image.open('Images/bomb.png'),
        'f': Image.open('Images/flag.png')
        }


def read_minefield(size = (760, 260, 1000, 720)):
    field = []
    for tile in all_tiles:
        position = gui.locateAllOnScreen(all_tiles[tile], region=size)              # 380x130 to 880x490
        for p in position:
            field.append({'value': tile, 'position': p})
            #print(p)
    
    field = sorted(field, key=lambda x: (x['position'][1], x['position'][0]))
    
    max_w, min_w = max([x['position'][0] for x in field]), min([x['position'][0] for x in field])
    max_h, min_h = max([x['position'][1] for x in field]), min([x['position'][1] for x in field])    
    dist_betsq = field[1]['position'][0] - field[0]['position'][0]                                  # Currently 32 pixels
    
    width = (max_w - min_w + dist_betsq) // dist_betsq
    height = (max_h - min_h + dist_betsq) // dist_betsq
    
    tiles = [Tile(i, t['position'], t['value']) for i,t in enumerate(field)]
    minefield = Minefield(width, height, tiles)
    new_size = (minefield.tiles[0].position[0] - 5, minefield.tiles[0].position[1] - 5, minefield.tiles[len(minefield.tiles) - 1].position[0] - minefield.tiles[0].position[0] + 40, minefield.tiles[len(minefield.tiles) - 1].position[1] - minefield.tiles[0].position[1] + 40)

    return minefield, new_size

  
def display_minefield(minefield):
    for tile in minefield.tiles:
        print(tile.value, end=' ')
        if (tile.index+1) % minefield.width == 0:
            print()
     

def find_neighbors(tile, minefield):
    i, w, h = tile.index, minefield.width, minefield.height
    if (i // w == 0) and (i % w == 0):          return (i + 1, i + w, i + w + 1)        # 1
    elif (i // w == 0) and (i % w == w - 1):    return (i - 1, i + w, i + w - 1)        # 2
    elif (i // w == h - 1) and (i % w == 0):     return (i - w, i - w + 1, i + 1)        # 3
    elif (i // w == h - 1) and (i % w == w - 1): return (i - w - 1, i - w, i - 1)        # 4
    elif i // w == 0:                           return (i - 1, i + 1, i + w - 1, i + w, i + w + 1)   # 5
    elif i % w == 0:                            return (i - w, i - w + 1, i + 1, i + w, i + w + 1)      # 8
    elif i % w == w - 1:                        return (i - w - 1, i - w, i - 1, i + w - 1, i + w)      # 6
    elif i // w == h - 1:                       return (i - w - 1, i - w, i - w + 1, i - 1, i + 1)      # 7
    else:                                       return (i - w - 1, i - w, i - w + 1, i - 1, i + 1, i + w - 1, i + w, i + w + 1) # 9       


def find_patterns(m, t, h):           
    if t.index % m.width != 0 and t.index % m.width != m.width - 1:                                                                     # If tile is not on the left or right-most columns
        if m.tiles[t.index - 1].value == (int(t.value) - 1) and m.tiles[t.index + 1].value == (int(t.value) - 1) and len(h) == 3:       # If tile's value is one unit more than the value of its left and right neighbors AND has exactly 3 hidden neighbors
            if h[2] - h[0] == 2:                                                                                                        # If the 3 hidden neighbors are in the SAME ROW:
                return True
            else: return False
        else: return False
    else: return False
     
           
def play(minefield, size):
    field, hidden_index = [], []
    total_hidden = 0
    click_random = True
    for tile in all_tiles:
        position = gui.locateAllOnScreen(all_tiles[tile], region=size)
        for p in position:
            field.append({'value': tile, 'position': p})
    
    field = sorted(field, key=lambda x: (x['position'][1], x['position'][0])) 
    minefield.tiles = [Tile(i, t['position'], t['value']) for i,t in enumerate(field)]
    
    
    # APPLY RULES:
    for tile in minefield.tiles:
        # TERMINATION CONDITION: If a bomb is seen, bot LOSES!
        if tile.value == 'b': return True
    
        if tile.value == '_':                                               # Count the number of hidden tiles
            total_hidden += 1
            hidden_index.append(tile.index)
         
        neighbors = find_neighbors(tile, minefield)                         # Map the index of all neighbors
        
        if tile.value != '_' and tile.value != 'f' and tile.value != 0:     # If it is a number, count the number of hidden tiles around
            n_hidden, n_flag = 0, 0
            hidden_around = []
            for n in neighbors:
                if minefield.tiles[n].value == '_':
                    n_hidden += 1
                    hidden_around.append(n)                                 # List with the indexes of hidden tiles around
                elif minefield.tiles[n].value == 'f':
                    n_flag += 1                                             # Count number of flags around
        
            if tile.value == n_hidden + n_flag:                             # Place flags
                for h in hidden_around:
                    rClick_x, rClick_y = minefield.tiles[h].position[0]/2, minefield.tiles[h].position[1]/2
                    gui.rightClick(rClick_x + 5, rClick_y + 5)
                    minefield.tiles[h].value = 'f'
                    # hidden_around.remove(h)
                    click_random = False
                    
            elif tile.value == n_flag:                                      # Click on safe squares
                for h in hidden_around:                    
                    click_x, click_y = minefield.tiles[h].position[0]/2, minefield.tiles[h].position[1]/2
                    gui.click(click_x + 5, click_y + 5)
                    minefield.tiles[h].value = '0'
                    # hidden_around.remove(h)
                    click_random = False
                                
                            
            elif find_patterns(minefield, tile, hidden_around):
                pdb.set_trace()
            #if tile.index % minefield.width != 0 and tile.index % minefield.width != minefield.width - 1:       # If tile is not on the left or right-most columns
            #    if minefield.tiles[tile.index - 1].value == (int(tile.value) - 1) and minefield.tiles[tile.index + 1].value == (int(tile.value) - 1) and len(hidden_around) == 3:
            #        if hidden_around[2] - hidden_around[0] == 2:
                for h in range(0, 3, 2):         # Executes for 0 and 2
                    rClick_x, rClick_y = minefield.tiles[hidden_around[h]].position[0]/2, minefield.tiles[hidden_around[h]].position[1]/2
                    gui.rightClick(rClick_x + 5, rClick_y + 5)
                    minefield.tiles[hidden_around[h]].value = 'f'
                    #rClick_x, rClick_y = minefield.tiles[hidden_around[0]].position[0]/2, minefield.tiles[hidden_around[0]].position[1]/2
                    #gui.rightClick(rClick_x + 5, rClick_y + 5) 
                    #minefield.tiles[hidden_around[0]].value = 'f'
                        
                click_x, click_y = minefield.tiles[hidden_around[1]].position[0]/2, minefield.tiles[hidden_around[1]].position[1]/2
                gui.click(click_x + 5, click_y + 5)
                click_random = False      
                
    
    # TERMINATION CONDITION: If no hidden tiles are left, bot WINS!
    if total_hidden == 0: return True
                   
    if click_random == True:                                                # If no rule applies, click on a random square
        next_click = random.choice(hidden_index)
        click_x, click_y = minefield.tiles[next_click].position[0]/2, minefield.tiles[next_click].position[1]/2
        gui.click(click_x + 5, click_y + 5)
                            
    return False
    

def main():
    #minefield = read_minefield()
    minefield, size = read_minefield()
    display_minefield(minefield)
    print(minefield.width, "x", minefield.height)
    
    # First click is chosen at random
    # Starts w/ one of the four corners
    firstClick = random.choice([0, minefield.width - 1, len(minefield.tiles) - minefield.width, len(minefield.tiles) - 1])  
    firstClick_x, firstClick_y = minefield.tiles[firstClick].position[0]/2, minefield.tiles[firstClick].position[1]/2
    gui.doubleClick(firstClick_x+5, firstClick_y+5)
    end = False

    while end == False:
        end = play(minefield, size)
        time.sleep(0.005)


main()


