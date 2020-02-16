
import pygame
from tkinter import filedialog
from tkinter import *
import pickle

class Persister():

    def __init__(self):
        pass


    def save(self, amap):
        root = Tk()
        print(amap)
        filename = filedialog.asksaveasfilename(initialdir = ".",title = "Select file")
        print(filename)
        try:
            f = open(filename, 'wb')
            pickle.dump(amap, f)
        except:
            raise
            pass
        root.destroy()


    def open(self):
        root = Tk()
        filename = filedialog.askopenfilename(initialdir = ".",title = "Select file")
        try:
            f = open(filename, 'rb')
            amap = pickle.load(f)
        except:
            raise
            return None
        root.destroy()

        return amap


class Map():

    def __init__(self):
        self.points = []
        self.points.append([])
        self.i = 0


    def new_part(self):
        self.points.append([])
        self.i+=1

    def add(self, p):
        self.points[self.i].append(p)

    def remove_last(self):
        if self.i<0:
            return
        if len(self.points[self.i]) > 0:
            self.points[self.i].pop()
        elif len(self.points) > 1:
            self.points.pop()
            self.i -= 1




class Presenter():
    
    green = (50,250,150)
    blue = (50,150,250)
    
    def __init__(self):
        pass    

    def draw(self, surface, map):
        for poly in map.points:
            if len(poly) > 1:
                pygame.draw.aalines(surface, self.green, False, poly, 2)

            for p in poly:
                pygame.draw.circle(surface, self.blue, (int(p.x), int(p.y)), 4, 4)
