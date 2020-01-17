import pygame
import os

# GAME SETTINGS

gametitle = "Karaoke Fun"
fps = 60
resolution = (1280,720)

# GENERAL USE

COLORS = {"BLACK": (0,0,0),
          "WHITE": (255,255,255),
          "RED": (255,0,0),
          "ORANGE": (255,165,0),
          "YELLOW": (255,255,0),
          "GREEN": (0,255,0),
          "BLUE": (0,0,255),
          "INDIGO": (75,0,130),
          "VIOLET": (238,130,238),
          "MAGENTA": (255,0,255),
          "CYAN": (0,255,255),}

_image_library = {}
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path)
            _image_library[path] = image
    return image.convert_alpha()

def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)