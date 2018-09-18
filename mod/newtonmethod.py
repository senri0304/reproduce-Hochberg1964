from numpy import *

d = float(5)
r = float(50)

th = 2.0*arcsin(d/(2.0*r))
L = r*th
h = r*(1.0-cos(th/2))

print(th*180/pi)

theta = th*180.0/pi
n = -sin(theta)

print(n)
