import numpy as np

#L=弧長;
#d=弦長;
#h=矢高;
#r=半径;

pi = np.pi

L = 0
h = 5
d = 0
r = 50


if L<>0 and h<>0 and d==0 and r==0:
    # 円弧の長さと矢高から弦長
    
    a=2.*h/L
    x=1.0
    for (j=0;j<=20;j=j+1):
        x=x-(-a*x*x+x*(1.-cos(x)))/(x*sin(x)-1.+cos(x))
    th=2*x
    r=L/th
    d=2.*r*sin(x)

elif L<>0 and d<>0 and h==0 and r==0:
    # 円弧の長さと弦長から矢高

    c=d/L
    x=1.0
    for j=0;j<=20;j=j+1:
        x=x-((x*sin(x)-c*x*x)/(x*cos(x)-sin(x)))
    th=2*x
    r=L/th
    h=r*(1.-cos(th/2.))

elif L==0 and d<>0 and h<>0 and r==0:
    # 弦長と矢高から円弧
    
    a=h/d
    x=1.0
    for j=0;j<=20;j=j+1:
        f=(1.-cos(x))/(2.*sin(x)) - a
        fd = (1.-cos(x))/(2.*sin(x)*sin(x))
        x=x-f/fd
    th=2*x
    r=d/(2.*sin(x))
    L=r*th

elif L<>0 and d==0 and h==0 and r<>0:
    # 円弧の長さと半径から弦長・矢高

    th=L/r
    d=2.*r*sin(th/2.)
    h=r*(1.-cos(th/2.))

elif L==0 and d<>0 and h==0 and r<>0:
    # 弦長と半径から矢高・円弧
    th = 2.*asin(d/(2.*r))
    L=r*th
    h=r*(1.-cos(th/2.))

elif L==0 and d==0 and h<>0 and r<>0:
   # 矢高と半径から弦長・弧長
   th = 2.*acos(1.-(h/r))
   L=r*th
   d=2.*r*sin(th/2.)

print(L)
print(d)
print(h)
print(r)
print(th*180/pi)
