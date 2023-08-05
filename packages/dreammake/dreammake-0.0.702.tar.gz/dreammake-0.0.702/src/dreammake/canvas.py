import pygame as pg
from pygame.locals import *


class Canvas:
    def __init__(self, size, caption):
        self.width, self.height = size
        self.caption = caption
        self.surface = pg.Surface(size)
        self.frame_clock = pg.time.Clock()
        self.frame_rate = 120
        self.dt = 1/self.frame_rate

        pg.display.set_caption(caption)

    def clear(self, color=(255, 255, 255)):
        self.surface.fill(color)

    def late_update(self):
        pg.display.update()
        self.dt = self.frame_clock.tick(self.frame_rate)
