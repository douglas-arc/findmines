

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