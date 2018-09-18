import pyglet
from pyglet.gl import *
import numpy as np

batch = pyglet.graphics.Batch()
pi = np.pi

class DrawCircle():
    def __init__(self, xpos, ypos, radius, vertices):
        self.xpos = xpos
        self.ypos = ypos
        self.radius = radius
        self.vertices = vertices
        glClear(GL_COLOR_BUFFER_BIT)
    def circle(self):
        glPushMatrix()
        glLineWidth(5)
        for i in range(self.vertices):
            x = self.radius*np.cos(2.0*pi*float(i)/float(self.vertices))
            y = self.radius*np.sin(2.0*pi*float(i)/float(self.vertices))
            vlist = batch.add(1, GL_LINE_LOOP, None,
                              ("v2f", [x + self.xpos, y + self.ypos]),
                              ("c3f", [0.0, 0.0, 0.0]))
        glPopMatrix()
    def draw(self):
        batch.draw()
