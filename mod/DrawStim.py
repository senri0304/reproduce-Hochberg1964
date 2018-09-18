import pyglet
from pyglet.gl import *

class DrawStim():
    def __init__(self, width, height, xpos, ypos, R, G, B):
        self.width = width
        self.height = height
        self.xpos = xpos
        self.ypos = ypos
        self.R = R
        self.G = G
        self.B = B
    
    def draw(self):
        glPushMatrix()
        glColor3f(self.R, self.G, self.B)
        x = self.width / 2
        y = self.height / 2
        vlist = pyglet.graphics.vertex_list(4,
                          ('v2f',[-x+self.xpos, y+self.ypos,
                                  -x+self.xpos, -y+self.ypos,
                                  x+self.xpos, -y+self.ypos,
                                  x+self.xpos, y+self.ypos]))
        vlist.draw(GL_QUADS)
        glPopMatrix()


class DrawLine():
    def __init__(self, xpos, ypos, length, width, quantity, interval, rotation):
        self.xpos = xpos
        self.ypos = ypos
        self.length = length
        self.width = width
        self.quantity = quantity
        self.interval = interval
        self.rotation = rotation
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.xpos, self.ypos, 0)
        glColor3f(0.0, 0.0, 0.0)
        glRotatef(self.rotation, 0, 0, 1)
        glLineWidth(self.width)
        for i in range(self.quantity):
            vlist = pyglet.graphics.vertex_list(2,
                                                ("v2f", [0, 0 + i*self.interval, self.length, 0 + i*self.interval]))
            
            vlist.draw(GL_LINES)
        glPopMatrix()
