
 
import pygame
from pygame.math import *
import math

from car import Car, Lidar
from polymap import Map, Presenter, Persister

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 


pygame.init()

w = 800
h = 600
screen = pygame.display.set_mode([w, h])
 
pygame.display.set_caption('Drift')
 
clock = pygame.time.Clock()
done = False

presenter = Presenter()
persister = Persister()

map = persister.open()



debug = (50,250,150)
def point(p, c):
    pygame.draw.circle(screen, c, (int(p.x), int(p.y)), 4, 4)

def line(p, v):
    pygame.draw.line(screen, debug, p, p+v, 2)

def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def intersects_map(map, box):
    for cara, carb in zip(box, box[1:]+[box[0]]):
        points = []
        for part in map.points:
            for pa, pb in zip(part, part[1:]):
                if intersect(cara,carb,pa,pb):
                    return True
    return False

car = Car(Vector2(w/2, h/2))
sprites = pygame.sprite.Group(car)

lidar = Lidar()

while not done:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            done = True
            break  
        elif e.type == pygame.KEYDOWN \
        	and e.key == pygame.K_ESCAPE:
                done = True
 
    dt = clock.tick(120)
    
    sprites.update(events, dt)

    screen.fill((30, 30, 30))
    
    sprites.draw(screen)

    debug = (50,250,150)
    # pygame.draw.rect(screen, debug, car.rect, 1)
    car_box = car.get_hitbox()

    if intersects_map(map, car_box):
        pygame.draw.aalines(screen, (255,0,0), True, car.get_hitbox(), 2)
    else:
        pygame.draw.aalines(screen, debug, True, car.get_hitbox(), 2)


    

    # point(car.r, (255, 0, 0))
    # point(car.bot, (0,0,255))
    # point(car.position, (0,255,0))
    # point(car.position+car.direction*100, (255,255,0))
    # point(car.r+car.r_to_new_bot, (255,0,255))

    # line(car.bot, car.bot_to_r)
    # line(car.r, car.r_to_new_bot)
    # direc = Vector2()
    # direc.from_polar((1, car.angle))
    # line(car.position, direc*40)
    presenter.draw(screen, map)

    lidar.draw(screen, car.position, car.angle, map)

    pygame.display.flip()
    
    
 
pygame.quit()

speeds = car.debug["speed"]
print(car.debug) 
import matplotlib.pyplot as plt

plt.plot(speeds)
plt.savefig("img.png")