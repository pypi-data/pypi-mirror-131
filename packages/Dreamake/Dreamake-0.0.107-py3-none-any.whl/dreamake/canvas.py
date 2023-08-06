import pygame as pg
from pygame.locals import *
from .gui import UIManager

pg.init()


class Canvas:
    """The Canvas object handles the basic functionality of an application window including events"""
    def __init__(self, size, caption):
        # Window properties
        self.width, self.height = size
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.caption = caption
        self.surface = pg.display.set_mode(size)
        pg.display.set_caption(caption)

        # Time properties
        self.frame_clock = pg.time.Clock()
        self.frame_rate = 120
        self.dt = 1/self.frame_rate

        # Event properties
        self.events = []
        self.mouse_pos = (0, 0)
        self.mouse_rel = (0, 0)
        self.mouse_pressed = []

        # UI properties
        self.ui_manager = UIManager(self.rect)

    def get_events(self):
        self.events = pg.event.get()
        return self.events

    def get_mouse_pos(self):
        self.mouse_pos = pg.mouse.get_pos()
        return self.mouse_pos

    def get_mouse_rel(self):
        self.mouse_rel = pg.mouse.get_rel()
        return self.mouse_rel

    def get_mouse_pressed(self):
        self.mouse_pressed = pg.mouse.get_pressed()
        return self.mouse_pressed

    def clear(self, color=(255, 255, 255)):
        self.surface.fill(color)

    def handle_ui(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.ui_manager.handle_events(self.events, self.mouse_pos)

    def update_ui(self):
        self.ui_manager.update(self.dt)

    def draw_ui(self, dest):
        self.ui_manager.draw(dest)

    def update(self):
        pg.display.update()
        self.dt = self.frame_clock.tick(self.frame_rate)
