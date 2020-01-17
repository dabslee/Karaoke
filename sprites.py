import pygame
import threading
import random
import datetime

import auxiliary

# Template for Sprite objects
#    All sprites should have the following methods:
#     __init__(self)
#     event_update(self, event)
#     continuous_update(self)
#     render(self, screen)

def vecdist(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

# General
class Sprite():
    _instances = list()
    def __init__(self, kwargs):
        Sprite._instances.append(self)
    def event_update(self, event, kwargs):
        pass
    def continuous_update(self, kwargs):
        pass
    def render(self, screen, kwargs):
        pass

    @classmethod
    def getinstances(cls):
        return cls._instances

    def delete(self):
        Sprite._instances.remove(self)

class SurfaceSprite(Sprite):
    alpha = 255
    surface = pygame.Surface((100,100))
    location = (0,0)
    
    fading = False
    fadestart = datetime.datetime.now()
    fadetime = 1

    def __init__(self, surface, location, kwargs):
        self.surface = surface
        self.location = location
        Sprite.__init__(self, kwargs)

    def event_update(self, event, kwargs):
        Sprite.event_update(self, event, kwargs);

    def continuous_update(self, kwargs):
        secondssince = (datetime.datetime.now()-self.fadestart).total_seconds()
        if self.fading and self.alpha > 0:
            self.alpha = max(0, 255-255/self.fadetime*secondssince)
        elif not self.fading and self.alpha < 255:
            self.alpha = min(255, 255/self.fadetime*secondssince)
        Sprite.continuous_update(self, kwargs);

    def render(self, screen, kwargs):
        auxiliary.blit_alpha(screen, self.surface, self.location, self.alpha)
        Sprite.render(self, screen, kwargs);

    def hide(self):
        self.fading = True
        self.alpha = 0

    def show(self):
        self.fading = False
        self.alpha = 255

    def fade_out(self, fadetime=1):
        self.fading = True
        self.fadestart = datetime.datetime.now()
        self.fadetime = fadetime

    def fade_in(self, fadetime=1):
        self.fading = False
        self.fadetime = fadetime
        self.fadestart = datetime.datetime.now()

    def go_to_front(self):
        self.delete()
        Sprite._instances.append(self)

class TextSprite(SurfaceSprite):
    font = "TNR"
    fontsize = 20
    fontcolor = auxiliary.COLORS["BLACK"]
    centered = False
    texttrack = ""

    def __init__(self, text, location, kwargs, font="TNR", fontsize=20, fontcolor=auxiliary.COLORS["WHITE"]):
        self.font = font
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.texttrack = text
        myfont = pygame.font.Font("resources/fonts/" + font + ".ttf", fontsize)
        surface = myfont.render(text, True, fontcolor)
        if (location[0] == -1):
            self.centered = True
            location = (auxiliary.resolution[0]/2-surface.get_width()/2, location[1])
        SurfaceSprite.__init__(self, surface, location, kwargs)

    def set_text(self, text):
        myfont = pygame.font.Font("resources/fonts/" + self.font + ".ttf", self.fontsize)
        self.surface = myfont.render(text, True, self.fontcolor)
        if self.centered:
            self.location = (auxiliary.resolution[0]/2-self.surface.get_width()/2, self.location[1])
        self.texttrack = text

    def get_text(self):
        return self.texttrack

class ImageSprite(SurfaceSprite):
    imagepath = ""
    size = (-1,-1)

    def __init__(self, imagepath, location, kwargs, size=(-1,-1)):
        self.imagepath = imagepath
        self.size = size
        surface = auxiliary.get_image(imagepath)
        if (size[0] != -1):
            surface = pygame.transform.scale(surface, size)
        SurfaceSprite.__init__(self, surface, location, kwargs)

    def continuous_update(self, kwargs):
        if (self.size[0] != -1):
            self.surface = pygame.transform.scale(auxiliary.get_image(self.imagepath), self.size)
        SurfaceSprite.continuous_update(self, kwargs);

class Background(Sprite):
    move_on = True

    def __init__(self, kwargs):
        Sprite.__init__(self, kwargs)

    def event_update(self, event, kwargs):
        Sprite.event_update(self, event, kwargs)

    def continuous_update(self, kwargs):
        Sprite.continuous_update(self, kwargs)

    def render(self, screen, kwargs):
        Sprite.render(self, screen, kwargs)