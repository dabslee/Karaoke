import pygame

import auxiliary
import sprites
import time

pygame.init()
screen = pygame.display.set_mode((600, 720), pygame.RESIZABLE)
running = True
clock = pygame.time.Clock()

pygame.display.set_caption(auxiliary.gametitle)
pygame.display.set_icon(auxiliary.get_image("favicon.png"))

# Dictionary that stores "global" variables
kwargs = {}
# Declare all sprites here
sprites_list = [sprites.Background(kwargs),
                sprites.Title(kwargs),
                sprites.PlayButton(kwargs),
                sprites.HelpButton(kwargs),
                sprites.HelpBox(kwargs),
                sprites.RecordButton(kwargs),
                sprites.Score(kwargs),
                sprites.BackToStart(kwargs),]

# Main loop
while running:

    sprites_list = sprites.Sprite.getinstances()
    
    # Continuous updates
    for sprite in sprites_list:
        sprite.continuous_update(kwargs)

    # Rendering
    screen.fill(auxiliary.COLORS["BLUE"])
    for sprite in sprites_list:
        sprite.render(screen, kwargs)

    pygame.display.flip()
    clock.tick(auxiliary.fps)

    # Event handling
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            running = False
            break
        if (event.type == pygame.VIDEORESIZE):
            pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        for sprite in sprites_list:
            if (sprite.event_update(event, kwargs) == 1):
                break