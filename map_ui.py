
 
import pygame
from pygame.math import *
import math
from polymap import Map, Presenter, Persister



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 

pygame.init()
 
w = 800
h = 600
screen = pygame.display.set_mode([w, h])
 
pygame.display.set_caption('Create map')
 
clock = pygame.time.Clock()
done = False

amap = Map()
presenter = Presenter()
saver = Persister()


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pressed = pygame.mouse.get_pressed()
            if pressed[1]:
                amap.new_part()

            if pressed[0]: 
                p = pygame.mouse.get_pos()
                p = Vector2(p)
                amap.add(p)

            if pressed[2]:
                amap.remove_last()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_s:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    saver.save(amap)

        
 
        
 
    dt = clock.tick(120)

    screen.fill((30, 30, 30))
    
    presenter.draw(screen, amap)
   
    pygame.display.flip()
    
    
 
pygame.quit()