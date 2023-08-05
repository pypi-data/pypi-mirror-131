import pygame as pg
pg.init()

def init_pygame():
    pg.init()
    print("Congratulations you uploaded the dang game engine!")

init_pygame()

class Canvas:
    def __init__(self, size, caption):
        print("You have created a project canvas")