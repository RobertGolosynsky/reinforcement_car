"""
 Simple snake example.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
"""
 
import pygame
from pygame.math import *
import math
# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 




 
# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x600 sized screen
w = 800
h = 600
screen = pygame.display.set_mode([w, h])
 

# Set the title of the window
pygame.display.set_caption('Drift')


 
clock = pygame.time.Clock()
done = False


class Car(pygame.sprite.Sprite):

    def __init__(self, position):
        super().__init__()
        car_img = pygame.image.load("car_red.jpg")
        self.car_length = 40
        self.image = pygame.transform.scale(car_img, (40, 20))
        self.org_image = self.image.copy()
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect(center=position)

        self.position = position  
        self.speed = 0 
        self.acceleration = 0

        self.turn_angle = 0
        self.angle = -90

        self.r = Vector2()
        self.bot = Vector2()
        self.bot_to_r = Vector2()
        self.r_to_new_bot = Vector2()
    

    def update(self, events, dt):
        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_LEFT]:
            self.turn_angle += 1 
        elif keypressed[pygame.K_RIGHT]:
            self.turn_angle -= 1
        else:
            self.turn_angle = 0
        if keypressed[pygame.K_UP]:
            self.acceleration = 0.0001
        if keypressed[pygame.K_DOWN]:
            self.acceleration = -0.0001
        
        self.turn_angle = max(min(30, self.turn_angle), -30)
        print("turn_angle", self.turn_angle)
        
        self.speed+=self.acceleration*dt
        self.acceleration = 0

        self.direction = Vector2()
        self.direction.from_polar((1, self.angle))
        self.bot = self.position - self.direction*(self.car_length/2)
        
        if self.speed == 0:
            return

        if self.turn_angle > 0.001 or self.turn_angle < -0.001:
           
            print("angle", self.angle)
            print("direction", self.direction)
            turn_radius = self.car_length/math.tan(math.radians(-self.turn_angle))
      
            bot_to_r = self.direction.rotate(90).normalize()*turn_radius
            self.bot_to_r = bot_to_r
            
            

            r = self.bot+bot_to_r
            self.r = r
            print(self.r)
            r_to_bot = bot_to_r*(-1)
            gamma = (self.speed*dt*180)/(math.pi*turn_radius)
            # print(gamma)
            self.r_to_new_bot = r_to_bot.rotate(gamma)
            new_bot = r+self.r_to_new_bot
            
            self.angle += gamma
            new_mid = new_bot + self.direction.rotate(gamma)*self.car_length/2
            self.position = new_mid

            self.image = pygame.transform.rotate(self.org_image, - self.angle)
        else:
            
            self.position+=self.direction*self.speed*dt
        self.rect = self.image.get_rect(center=self.position)
        # if self.turn_angle > 0.1 :
        #     self.turn_angle -= 0.1
        # else:
        #     if self.turn_angle < -0.1:
        #         self.turn_angle += 0.1  
     


debug = (50,250,150)
def point(p, c):
    
    print("point", p)
    pygame.draw.circle(screen, c, (int(p.x), int(p.y)), 4, 4)

def line(p, v):
    pygame.draw.line(screen, debug, p, p+v, 2)

car = Car(Vector2(w/2, h/2))
sprites = pygame.sprite.Group(car)
while not done:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            done = True
            break  
 
        
 
    dt = clock.tick(120)
    
    sprites.update(events, dt)

    screen.fill((30, 30, 30))
    
    sprites.draw(screen)

    debug = (50,250,150)
    pygame.draw.rect(screen, debug, car.rect, 1)
   
    point(car.r, (255, 0, 0))
    point(car.bot, (0,0,255))
    point(car.position, (0,255,0))
    point(car.position+car.direction*100, (255,255,0))
    point(car.r+car.r_to_new_bot, (255,0,255))

    line(car.bot, car.bot_to_r)
    line(car.r, car.r_to_new_bot)
    direc = Vector2()
    direc.from_polar((1, car.angle))
    line(car.position, direc*40)


    pygame.display.flip()
    
    
 
pygame.quit()