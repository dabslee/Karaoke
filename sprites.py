import pygame
import time

import auxiliary

# Template for Sprite objects
#    All sprites should have the following methods:
#     __init__(self)
#     event_update(self, event)
#     continuous_update(self)
#     render(self, screen)

# Kwargs enum
class KWARGS:
    STATE = "state"
    SCORE = "score"

# States enum
class STATES():
    INTRO = "Intro" # The startup screen
    HELP = "Help" # The help screen
    START = "Start" # Waiting to begin recording
    LISTENING = "Listening" # Recording the audios
    RESULTS = "Results" # Displaying the results

# The sprite class
class Sprite():
    _instances = list()
    def __init__(self, kwargs):
        Sprite._instances.append(self)
    def event_update(self, event, kwargs):
        return 0
    def continuous_update(self, kwargs):
        pass
    def render(self, screen, kwargs):
        pass

    @classmethod
    def getinstances(cls):
        return cls._instances

    def delete(self):
        Sprite._instances.remove(self)

# General image sprite class
class ImageSprite(Sprite):
    costume = None
    position = (0,0)
    dimensions = (0,0)
    alpha = 0

    def __init__(self, kwargs, imagepath):
        self.costume = auxiliary.get_image(imagepath)
        self.dimensions = self.costume.get_rect().size
        Sprite.__init__(self, kwargs)

    def render(self, screen, kwargs):
        screen.blit(pygame.transform.scale(self.costume, self.dimensions), self.position)
        Sprite.render(self, screen, kwargs)

    # Check if it's clicked
    def touchingmouse(self):
        pos = pygame.mouse.get_pos()
        if (pos[0] >= self.position[0] and pos[0] <= self.position[0] + self.dimensions[0] and 
            pos[1] >= self.position[1] and pos[1] <= self.position[1] + self.dimensions[1]):
            return True
        return False

# The background sprite
# Also initializes all the kwarg variables
class Background(ImageSprite):
    def __init__(self, kwargs):
        kwargs[KWARGS.STATE] = STATES.INTRO
        kwargs[KWARGS.SCORE] = 0
        ImageSprite.__init__(self, kwargs, "neon_background.png")

# The logo/title image
class Title(ImageSprite):
    def __init__(self, kwargs):
        ImageSprite.__init__(self, kwargs, "title.png")

    def continuous_update(self, kwargs):
        windowsize = pygame.display.get_surface().get_size()
        if (kwargs[KWARGS.STATE] == STATES.INTRO):
            self.dimensions = self.costume.get_rect().size
            self.position = (windowsize[0]//2-self.dimensions[0]//2, windowsize[1]//5)
        elif (kwargs[KWARGS.STATE] == STATES.HELP):
            self.position = (20,20)
            self.dimensions = [i//2 for i in self.costume.get_rect().size]
        elif (kwargs[KWARGS.STATE] == STATES.START):
            self.position = (windowsize[0]//2-self.dimensions[0]//2, windowsize[1]//5)
        ImageSprite.continuous_update(self, kwargs)

    def assume_position(self):
        windowsize = pygame.display.get_surface().get_size()
        if (kwargs[KWARGS.STATE] == STATES.INTRO):
            self.position = (windowsize[0]//2-self.dimensions[0]//2, windowsize[1]//5)
        elif (kwargs[KWARGS.STATE] == STATES.HELP):
            self.position = (20,20)

# The play button you press to start
class PlayButton(ImageSprite):
    def __init__(self, kwargs):
        ImageSprite.__init__(self, kwargs, "play.png")

    def render(self, screen, kwargs):
        if (kwargs[KWARGS.STATE] == STATES.INTRO):
            if (self.touchingmouse()):
                factor = 1.1
                largerdim = [int(i*factor) for i in self.dimensions]
                shiftedpos = (self.position[0]-(factor-1)*self.dimensions[0]/2,
                              self.position[1]-(factor-1)*self.dimensions[1]/2)
                screen.blit(pygame.transform.scale(self.costume, largerdim), shiftedpos)
                Sprite.render(self, screen, kwargs)
            else:
                ImageSprite.render(self, screen, kwargs)
        else:
            Sprite.render(self, screen, kwargs)
    
    def event_update(self, event, kwargs):
        if (kwargs[KWARGS.STATE] == STATES.INTRO):
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if self.touchingmouse():
                    kwargs[KWARGS.STATE] = STATES.START
                    return 1
            elif (event.type == pygame.VIDEORESIZE):
                windowsize = pygame.display.get_surface().get_size()
                self.position = (windowsize[0]//2-self.dimensions[0]//2, int(windowsize[1]/2.5))
        return ImageSprite.event_update(self, event, kwargs)

# The button you press to open the help screen
class HelpButton(ImageSprite):
    def __init__(self, kwargs):
        ImageSprite.__init__(self, kwargs, "help.png")

    def render(self, screen, kwargs):
        if (kwargs[KWARGS.STATE] == STATES.INTRO):
            if (self.touchingmouse()):
                factor = 1.1
                largerdim = [int(i*factor) for i in self.dimensions]
                shiftedpos = (self.position[0]-(factor-1)*self.dimensions[0]/2,
                              self.position[1]-(factor-1)*self.dimensions[1]/2)
                screen.blit(pygame.transform.scale(self.costume, largerdim), shiftedpos)
                Sprite.render(self, screen, kwargs)
            else:
                ImageSprite.render(self, screen, kwargs)
        else:
            Sprite.render(self, screen, kwargs)
    
    def event_update(self, event, kwargs):
        if (kwargs[KWARGS.STATE] == STATES.INTRO):
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if self.touchingmouse():
                    kwargs[KWARGS.STATE] = STATES.HELP
                    return 1
            elif (event.type == pygame.VIDEORESIZE):
                windowsize = pygame.display.get_surface().get_size()
                self.position = (windowsize[0]//2-self.dimensions[0]//2, int(windowsize[1]/2))
        return ImageSprite.event_update(self, event, kwargs)

# The help screen
class HelpBox(ImageSprite):
    def __init__(self, kwargs):
        ImageSprite.__init__(self, kwargs, "helpbox.png")

    def continuous_update(self, kwargs):
        windowsize = pygame.display.get_surface().get_size()
        self.dimensions = (int(windowsize[1]/1.5), int(windowsize[1]/1.5))
        self.position = (windowsize[0]//2-self.dimensions[0]//2, int(windowsize[1]/5))
        ImageSprite.continuous_update(self, kwargs)

    def render(self, screen, kwargs):
        if (kwargs[KWARGS.STATE] == STATES.HELP):
            ImageSprite.render(self, screen, kwargs)
        else:
            Sprite.render(self, screen, kwargs)
    
    def event_update(self, event, kwargs):
        if (kwargs[KWARGS.STATE] == STATES.HELP):
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if self.touchingmouse():
                    kwargs[KWARGS.STATE] = STATES.INTRO
                    return 1
        return ImageSprite.event_update(self, event, kwargs)

# Press to start recording, press again to stop recording
class RecordButton(ImageSprite):
    rcex = auxiliary.Recorder(auxiliary.Recorder.EXTERNAL)
    rcin = auxiliary.Recorder(auxiliary.Recorder.INTERNAL)

    def __init__(self, kwargs):
        ImageSprite.__init__(self, kwargs, "recordlogo_off.png")
        self.dimensions = [int(i*0.5) for i in self.dimensions]

    def render(self, screen, kwargs):
        windowsize = pygame.display.get_surface().get_size()
        self.position = (windowsize[0]//2-self.dimensions[0]//2, int(windowsize[1]/2.2))
        if (kwargs[KWARGS.STATE] in [STATES.INTRO, STATES.HELP]):
            Sprite.render(self, screen, kwargs)
        elif (kwargs[KWARGS.STATE] in [STATES.LISTENING]):
            self.costume = auxiliary.get_image("recordlogo_on.png")
            ImageSprite.render(self, screen, kwargs)
        else:
            self.costume = auxiliary.get_image("recordlogo_off.png")
            ImageSprite.render(self, screen, kwargs)

    def event_update(self, event, kwargs):
        if (kwargs[KWARGS.STATE] == STATES.START):
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if self.touchingmouse():
                    kwargs[KWARGS.STATE] = STATES.LISTENING
                    self.rcex.begin_recording()
                    self.rcin.begin_recording()
                    return 1
        elif (kwargs[KWARGS.STATE] == STATES.LISTENING):
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if self.touchingmouse():
                    self.rcex.end_recording()
                    self.rcin.end_recording()
                    kwargs[KWARGS.SCORE] = int(100*auxiliary.compareNparr(self.rcex.fullrec, self.rcin.fullrec))
                    kwargs[KWARGS.STATE] = STATES.RESULTS
                    return 1
        return ImageSprite.event_update(self, event, kwargs)

# Shows the score on results screen
class Score(Sprite):
    def render(self, screen, kwargs):
        if (kwargs[KWARGS.STATE] == STATES.RESULTS):
            charwidth = 80
            windowsize = pygame.display.get_surface().get_size()
            images = [pygame.transform.scale(auxiliary.get_image("digits/"+thedigit+".png"), (charwidth,charwidth*181//125))
                      for thedigit in str(kwargs[KWARGS.SCORE])]
            for i in range(len(images)):
                screen.blit(images[i], (int(windowsize[0]/2-charwidth*len(str(kwargs[KWARGS.SCORE]))/2+i*charwidth),
                                        int(windowsize[1]/1.5)))

# The button to go back to ready-to-record on results screen
class BackToStart(ImageSprite):
    def __init__(self, kwargs):
        ImageSprite.__init__(self, kwargs, "okay.png")
        self.dimensions = [i//2 for i in self.dimensions]

    def render(self, screen, kwargs):
        windowsize = pygame.display.get_surface().get_size()
        self.position = (windowsize[0]//2-self.dimensions[0]//2, int(windowsize[1]/1.2))
        if (kwargs[KWARGS.STATE] == STATES.RESULTS):
            if (self.touchingmouse()):
                factor = 1.1
                largerdim = [int(i*factor) for i in self.dimensions]
                shiftedpos = (self.position[0]-(factor-1)*self.dimensions[0]/2,
                              self.position[1]-(factor-1)*self.dimensions[1]/2)
                screen.blit(pygame.transform.scale(self.costume, largerdim), shiftedpos)
                Sprite.render(self, screen, kwargs)
            else:
                ImageSprite.render(self, screen, kwargs)
        else:
            Sprite.render(self, screen, kwargs)
    
    def event_update(self, event, kwargs):
        if (kwargs[KWARGS.STATE] == STATES.RESULTS):
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if self.touchingmouse():
                    kwargs[KWARGS.STATE] = STATES.START
                    return 1
            elif (event.type == pygame.VIDEORESIZE):
                windowsize = pygame.display.get_surface().get_size()
        return ImageSprite.event_update(self, event, kwargs)