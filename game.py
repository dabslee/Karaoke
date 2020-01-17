import pygame
import os

import auxiliary
import sprites
import threading
import time
import random

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
running = True
clock = pygame.time.Clock()

pygame.display.set_caption(auxiliary.gametitle)

# Dictionary that stores "global" variables
kwargs = {}
# Declare all sprites here
sprites_list = [sprites.ImageSprite("background.png", (0,0), kwargs),
                sprites.TextSprite("Karaoke Fun", (700,300), kwargs, fontsize=80, fontcolor=auxiliary.COLORS["BLACK"]),
                sprites.TextSprite("Start recording", (700,500), kwargs, fontsize=30, fontcolor=auxiliary.COLORS["RED"])]

# Main loop
while running:

    sprites_list = sprites.Sprite.getinstances()
    
    # Continuous updates
    for sprite in sprites_list:
        sprite.continuous_update(kwargs)

    # Rendering
    screen.fill(auxiliary.COLORS["BLUE"])
    spritescopy = sprites_list.copy()
    for sprite in spritescopy:
        sprite.render(screen, kwargs)

    pygame.display.flip()
    clock.tick(auxiliary.fps)

    # Event handling
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            running = False
            break
        if (event.type == pygame.MOUSEBUTTONUP):
            if (sprites_list[2].get_text() == "Start recording"):
                sprites_list[2].set_text("Stop recording")
            elif (sprites_list[2].get_text() == "Stop recording"):
                sprites_list[2].set_text("Calculate score")
            elif (sprites_list[2].get_text() == "Calculate score"):
                sprites_list[2].set_text("...")
                time.sleep(random.random()*2)
            elif (sprites_list[2].get_text() == "..."):
                sprites_list[2].set_text("Score: " + str(round(random.random()*100)))
            else:
                sprites_list[2].set_text("Start recording")
        for sprite in sprites_list:
            sprite.event_update(event, kwargs)