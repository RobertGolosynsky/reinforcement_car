import pygame
from pygame.math import Vector2
import math
import numpy as np


def crosspoint(p, r, p1, p2):
    # rayOrigin = np.array(rayOrigin, dtype=np.float)
    # rayDirection = np.array(norm(rayDirection), dtype=np.float)
    # point1 = np.array(point1, dtype=np.float)
    # point2 = np.array(point2, dtype=np.float)
    
    v1 = p - p1
    v2 = p2 - p1
    v3 = Vector2(-r.y, r.x)
    t1 = v2.cross(v1) / v2.dot(v3)
    t2 = v1.dot(v3) / v2.dot(v3)
    if t1 >= 0.0 and t2 >= 0.0 and t2 <= 1.0:
        return p + t1 * r
    return None



class Lidar():

    def __init__(self, laser_count = 7, spread = 90):
        self.laser_count = laser_count
        self.lasers = []
        self.color = (150,0,255)
        for angle in np.linspace(-spread, spread, num = laser_count):
            laser = Vector2()
            laser.from_polar((1, angle))
            self.lasers.append(laser)


    def draw(self, screen, position, angle, map):
        closest_points = []
        for laser in self.lasers:
            points = []
            for part in map.points:
                for pa, pb in zip(part, part[1:]):
                    cross = crosspoint(position, laser.rotate(angle), pa, pb)
                    if cross:
                        points.append(cross)
            if len(points)>0:
                # print(list(sorted(zip(points, [position.distance_to(p) for p in points]), key = lambda a: a[1])) )
                closest = min(points, key= lambda p: position.distance_to(p))
                # print(closest)
            else:
                closest = None
            closest_points.append(closest)

        for p in closest_points:
            if p:
                pygame.draw.line(screen, self.color, position, p, 1)



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
        self.max_turn_angle = 40
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
            if self.speed<0:
                self.acceleration = 0.0003
            else:
                self.acceleration = 0.0001
        if keypressed[pygame.K_DOWN]:
            if self.speed>0:
                self.acceleration = -0.0003
            else:
                self.acceleration = -0.0001
        
        self.turn_angle = max(min(self.max_turn_angle, self.turn_angle), -self.max_turn_angle)
        
        self.speed+=self.acceleration*dt
        self.acceleration = 0

        self.direction = Vector2()
        self.direction.from_polar((1, self.angle))
        self.bot = self.position - self.direction*(self.car_length/2)
        
        if self.speed == 0:
            return

        if self.turn_angle > 0.001 or self.turn_angle < -0.001:
           
            # print("angle", self.angle)
            # print("direction", self.direction)
            turn_radius = self.car_length/math.tan(math.radians(-self.turn_angle))
      
            bot_to_r = self.direction.rotate(90).normalize()*turn_radius
            self.bot_to_r = bot_to_r
            
            

            r = self.bot+bot_to_r
            self.r = r
            # print(self.r)
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
     