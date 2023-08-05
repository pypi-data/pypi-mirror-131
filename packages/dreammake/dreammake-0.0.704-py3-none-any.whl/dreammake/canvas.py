import pygame as pg
from pygame.locals import *


class Canvas:
    """The Canvas object handles the basic functionality of an application window including events"""
    def __init__(self, size, caption):
        # Window properties
        self.width, self.height = size
        self.caption = caption
        self.surface = pg.display.set_mode(size)
        pg.display.set_caption(caption)

        # Time properties
        self.frame_clock = pg.time.Clock()
        self.frame_rate = 120
        self.dt = 1/self.frame_rate

    def get_events(self):
        return pg.event.get()

    def get_mouse_pos(self):
        return pg.mouse.get_pos()

    def get_mouse_rel(self):
        return pg.mouse.get_rel()

    def get_mouse_pressed(self):
        return pg.mouse.get_pos()

    def clear(self, color=(255, 255, 255)):
        self.surface.fill(color)

    def update(self):
        pg.display.update()
        self.dt = self.frame_clock.tick(self.frame_rate)
