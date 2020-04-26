import pyautogui as gui
from PIL import Image
import random

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
    
    width = int(((max_w - min_w) + dist_betsq) / (dist_betsq - 1))
    height = int(((max_h - min_h) + dist_betsq) / (dist_betsq - 1))
    
    tiles = [Tile(i, t['position'], t['value']) for i,t in enumerate(field)]
    minefield = Minefield(width, height, tiles)
    new_size = (minefield.tiles[0].position[0] - 5, minefield.tiles[0].position[1] - 5, minefield.tiles[len(minefield.tiles) - 1].position[0] - minefield.tiles[0].position[0] + 40, minefield.tiles[len(minefield.tiles) - 1].position[1] - minefield.tiles[0].position[1] + 40)
    print(size, new_size)
    return minefield, new_size

    
def display_minefield(minefield):
    for tile in minefield.tiles:
        print(tile.value, end=' ')
        if (tile.index+1) % minefield.width == 0:
            print()
 
            
def play(minefield, size):
    field = []
    for tile in all_tiles:
        position = gui.locateAllOnScreen(all_tiles[tile], region=size)
        for p in position:
            field.append({'value': tile, 'position': p})
    
    field = sorted(field, key=lambda x: (x['position'][1], x['position'][0])) 
    minefield.tiles = [Tile(i, t['position'], t['value']) for i,t in enumerate(field)]

    click = (random.randrange(len(minefield.tiles)))  
    click_x, click_y = minefield.tiles[click].position[0]/2, minefield.tiles[click].position[1]/2
    gui.click(click_x + 5, click_y + 5)      


def main():
    #minefield = read_minefield()
    minefield, size = read_minefield()
    display_minefield(minefield)
    print(minefield.width, "x", minefield.height)
    
    # First click is chosen at random
    firstClick = (random.randrange(len(minefield.tiles)))  
    firstClick_x, firstClick_y = minefield.tiles[firstClick].position[0]/2, minefield.tiles[firstClick].position[1]/2
    gui.doubleClick(firstClick_x+5, firstClick_y+5)

    end = False

    play(minefield, size)

    # while end == False:
    # end = play(minefield, size)


main()

'''tile = Image.open('Images/unseen.png')
tiles = list(gui.locateAllOnScreen(tile))             # Returns tupples with left, top, width and height. Put them into list

firstClick = (random.randrange(len(tiles)))
firstClick_x, firstClick_y = tiles[firstClick][0]/2, tiles[firstClick][1]/2

# tiles = sorted(tiles, key=lambda y: (y[1], y[0]))   # No need to sort
# print(tiles)

# x, y = tiles[0][0]/2, tiles[0][1]/2
gui.doubleClick(firstClick_x+5, firstClick_y+5)

for i in range(10):
    tiles = list(gui.locateAllOnScreen(tile)) 
    nextClick = (random.randrange(len(tiles)))
    nextClick_x, nextClick_y = tiles[nextClick][0]/2, tiles[nextClick][1]/2
    gui.click(nextClick_x+5, nextClick_y+5)
    print(i)




# ==========================================================================================

# Screen size 1280 x 800
# print(pyautogui.size())

# print("A posicao do mouse eh: " + str(gui.position()))
# 
# facelocation = gui.locateOnScreen('face.png')
# print(facelocation)
# 
# facex, facey = gui.center(facelocation)
# 
# print(type(facey))
# print(facex, facey)
# pyautogui.doubleClick(facex/2, facey/2) 


# Beginner: w=340, h=380
# Custom 30x20: w=1000, h=720
'''


