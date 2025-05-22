import pygame
import time
import math

class Pixel:
    '''Abstracts away the nitty-gritty of maintaining a perfect pixel system.'''
    def __init__(self, x: int, y:int):
        self.rect = pygame.Rect(x*10, y*10, 10, 10)
        self.x = x
        self.y = y
        self.set_color()
    
    def set_color(self):
        '''Updates color to reflect Adafruit display paradigm.'''
        if self.y < 16:
            self.color = (255, 255, 0)
        else:
            self.color = (0, 255, 255)

    def move(self, x: int, y: int):
        ''''''
        self.x += x
        self.y += y
        if self.y > 64:
            self.y = self.y - 64
        self.rect = pygame.Rect(self.x*10, self.y*10, 10, 10)
    
    def draw(self, screen: pygame.display):
        self.set_color()
        pygame.draw.rect(screen, self.color, self.rect)

class Character:
    def __init__(self, pixels: list):
        self.pixels = []
        for i in pixels:
            new_px = Pixel(i[0], i[1])
            self.pixels.append(new_px)
    
    def move(self, x: int, y: int):
        for i in self.pixels:
            i.move(x, y)
    
    def draw(self, screen: pygame.display):
        for i in self.pixels:
            i.draw(screen)