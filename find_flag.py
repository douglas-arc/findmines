import pyautogui as gui
from PIL import Image

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


unseen_tile = Image.open('Images/none.png')
tiles_unseen = list(gui.locateAllOnScreen(unseen_tile))

print(len(tiles_unseen))