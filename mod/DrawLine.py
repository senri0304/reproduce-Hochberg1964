import os, sys, pyglet
from pyglet.gl import *
import numpy as np

batch = pyglet.graphics.Batch()
pi = np.pi

class DrawLine():
    def __init__(self, xpos, ypos, length, width, quantity, interval):
        self.xpos = int(round(xpos))
        self.ypos = int(round(ypos))
        self.length = int(length)
        self.width = width
        self.quantity = int(quantity)
        self.interval = int(interval)
        glClear(GL_COLOR_BUFFER_BIT)
        
    def vline(self):
        glPushMatrix()
        glLineWidth(self.width)
        for i in range(self.quantity):
            vlist = batch.add(2, GL_LINES, None, 
            ("v2i", [self.xpos, self.ypos + i*self.interval,
                     self.xpos + self.length, self.ypos + i*self.interval]),
            ("c3f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
        glPopMatrix()
        
    def hline(self):
        for i in range(self.quantity):
            vlist = batch.add(2, GL_LINES, None, 
            ("v2i", [self.xpos + i*self.interval, self.ypos,
                     self.xpos + i*self.interval, self.ypos + self.length]),
            ("c3f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
    
    def draw(self):
#        glLineWidth(self.width)
#        glColorf(1.0, 1.0, 1.0)
        batch.draw()

class DrawLine2():
    def __init__(self, xpos, ypos, length, width, quantity, interval):
        self.xpos = int(round(xpos))
        self.ypos = int(round(ypos))
        self.length = int(length)
        self.width = width
        self.quantity = int(quantity)
        self.interval = int(interval)
        glClear(GL_COLOR_BUFFER_BIT)

    def draw(self):
        pass

class DrawCircularLine():
    def __init__(self, xpos, ypos, length, width, radius, vertices):
        self.xpos = xpos
        self.ypos = ypos
        self.length = length
        self.width = width
        self.radius = radius
        self.vertices = vertices
        
    def cline(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLineWidth(self.width)
        for i in range(self.vertices+1):
            x = self.radius*np.sin(2.0*pi*float(i)/float(self.vertices))
            y = self.radius*np.cos(2.0*pi*float(i)/float(self.vertices))
            vlist = batch.add(2, GL_LINES, None,
                              ("v2f", [x-self.length+self.xpos, y+self.ypos,
                                       x+self.length+self.xpos, y+self.ypos]),
                              ("c3f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
            
    def half_cline(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLineWidth(self.width)
        for i in range(self.vertices+1):
            x = self.radius*np.sin(pi*float(i)/float(self.vertices))
            y = self.radius*np.cos(pi*float(i)/float(self.vertices))
            vlist = batch.add(2, GL_LINES, None,
                              ("v2f", [x-self.length+self.xpos, y+self.ypos,
                                       x+self.length+self.xpos, y+self.ypos]),
                              ("c3f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
    
    def occlusion_half_cline(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLineWidth(self.width)
        for i in range(self.vertices+1):
            x = self.radius*np.sin(pi*float(i)/float(self.vertices))
            y = self.radius*np.cos(pi*float(i)/float(self.vertices))
            vlist = batch.add(2, GL_LINES, None,
                              ("v2f", [x+self.xpos, y+self.ypos,
                                       self.length+self.xpos, y+self.ypos]),
                              ("c3f", [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
    
    def draw(self):
        batch.draw()

class Mask():
    def __init__(self, xpos, ypos, radius, vertices, group):
        self.xpos = int(round(xpos))
        self.ypos = int(round(ypos))
        self.radius = radius
        self.vertices = vertices
        self.group = group
    
    def half_mask(self):
        for i in range(1, self.vertices):
            x = self.radius*-np.sin(pi*float(i)/float(self.vertices))
            y = self.radius*-np.cos(pi*float(i)/float(self.vertices))
            vlist = batch.add(1, GL_POLYGON, self.group, ("v2f", [x + self.xpos, y + self.ypos]), ("c3f", [1.0, 1.0, 1.0]))
    
    def polygon_mask_upper_right(self):
        batch.add(1, GL_POLYGON, self.group, ("v2f", [self.xpos+self.radius*2, self.ypos+self.radius]),  ("c3f", [1.0, 1.0, 1.0]))
        for i in range(1, self.vertices+1):
            x = self.radius*np.sin(0.5*pi*float(i)/float(self.vertices+1))
            y = self.radius*np.cos(0.5*pi*float(i)/float(self.vertices+1))
            vlist = batch.add(1, GL_POLYGON, self.group, ("v2f", [x + self.xpos, y + self.ypos]), ("c3f", [1.0, 1.0, 1.0]))
        batch.add(1, GL_POLYGON, self.group, ("v2f", [self.xpos+2*self.radius, self.ypos-1]),  ("c3f", [1.0, 1.0, 1.0]))
    
    def polygon_mask_lower_right(self):
        batch.add(1, GL_POLYGON, self.group, ("v2f", [self.xpos+self.radius*2, self.ypos-self.radius-10]),  ("c3f", [1.0, 1.0, 1.0]))
        for i in range(1, self.vertices+1):
            x = self.radius*np.sin(0.5*pi*float(i)/float(self.vertices+1))
            y = self.radius*-np.cos(0.5*pi*float(i)/float(self.vertices+1))
            vlist = batch.add(1, GL_POLYGON, self.group, ("v2f", [x + self.xpos, y + self.ypos]), ("c3f", [1.0, 1.0, 1.0]))
        batch.add(1, GL_POLYGON, self.group, ("v2f", [self.xpos+2*self.radius, self.ypos+2]),  ("c3f", [1.0, 1.0, 1.0]))
    
    def draw(self):
        batch.draw()
