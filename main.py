import math
import pygame
pygame.init()

px = None
py = None
px = 300
py = 300

mapX = 8
mapY = 8
mapS = mapX*mapY

a = 0
s = .03
ts = .2
n = 0
ph = 0

with open("world.wor") as f:
    map = []
    [[map.append(int(j)) for j in i.strip().split(" ")] for i in f.readlines()]


delta = None

w = pygame.display.set_mode([480, 512])
c = pygame.time.Clock()

def FixAng(a):
    if(a>359):   a-=360
    if(a<0):    a+=360
    return a

def degToRad(a):
    return a*math.pi/180.0

def intersects(cx, cy, r, rx, ry, rw, rh):
    cdx = abs(cx - rx)
    cdy = abs(cy - ry)

    if (cdx > (rw/2 + r)):  return False
    if (cdy > (rh/2 + r)):  return False

    if (cdx <= (rw/2)):    return True
    if (cdy <= (rh/2)):    return True

    cornerDistance_sq = ((cdx - rw/2)*(cdx - rw/2)) + ((cdy - rh/2) * (cdy - rh/2))

    return (cornerDistance_sq <= (r*r))


def check(keys):
    global px
    global py
    global delta
    global a
    global n
    global ph

    dx = 0
    dy = 0
    if keys[pygame.K_LEFT]:
        a += delta*ts
    if keys[pygame.K_RIGHT]:
        a -= delta*ts
    if keys[pygame.K_UP]:
        dx = math.cos(-(a) * (math.pi/180)) * 5
        dy = math.sin(-(a) * (math.pi/180)) * 5
    if keys[pygame.K_DOWN]:
        dx = math.cos(-(a-180) * (math.pi/180)) * 5
        dy = math.sin(-(a-180) * (math.pi/180)) * 5
        

    if keys[pygame.K_DOWN] != keys[pygame.K_UP]:
        ph = math.sin(n)*10
        n += 0.2
    else:
        n = 0
        ph = 0

    ix = False
    iy = False

    for y in range(0, mapY):
        for x in range(0, mapX):
            if map[y*mapX+x]:
                
                xo = x*mapS+32
                yo = y*mapS+32

                if intersects(px + (s * dx) * delta, py, 8, xo, yo, mapS, mapS):
                    ix = True
                if intersects(px, py + (s * dy) * delta, 8, xo, yo, mapS, mapS):
                    iy = True

    if not ix:
        px += (s * dx) * delta
    if not iy:
        py += (s * dy) * delta


def drawRays2D(ph):

    r = 0
    mx = 0
    my = 0
    mp = 0
    dof = 0
    vx = 0
    vy = 0
    rx = 0
    ry = 0
    ra = 0
    xo = 0
    yo = 0
    disV = 0
    disH = 0    
    ra = FixAng(a+30)  # ray set back 30 degrees  
    for r in range(0, 61):
        # ---Vertical---
        dof = 0
        disV = 100000
        Tan = math.tan(degToRad(ra))
        if(math.cos(degToRad(ra)) > 0.001):
            # looking left
            rx = ((int(px)>>6)<<6)+64      
            ry = (px-rx)*Tan+py 
            xo = 64 
            yo = -xo*Tan  
        elif(math.cos(degToRad(ra)) < -0.001):
            # looking right
            rx = ((int(px)>>6)<<6) - 0.0001 
            ry = (px-rx)*Tan+py 
            xo = -64 
            yo = -xo*Tan
        else:
            # looking up or down. no hit   
            rx = px 
            ry = py 
            dof = 8
        while(dof < 8):
            mx = int(rx) >> 6 
            my = int(ry) >> 6 
            mp = my*mapX+mx
            if(mp > 0 and mp < mapX*mapY and map[mp] == 1):
                # hit
                dof = 8 
                disV = math.cos(degToRad(ra))*(rx-px)-math.sin(degToRad(ra))*(ry-py)
            else:
                # check next horizontal
                rx += xo 
                ry += yo 
                dof += 1  
        
        vx = rx 
        vy = ry  
        # ---Horizontal---
        dof = 0 
        disH = 100000
        try:
            Tan = 1.0/Tan
        except:
            pass
        if(math.sin(degToRad(ra)) > 0.001):
            # looking up
            ry = ((int(py)>>6)<<6) - 0.0001 
            rx = (py-ry)*Tan+px 
            yo = -64 
            xo = -yo*Tan
        
        elif(math.sin(degToRad(ra))<-0.001):
            #looking down
            ry=((int(py)>>6)<<6)+64;      
            rx=(py-ry)*Tan+px
            yo= 64
            xo=-yo*Tan
        
        else:
            # looking straight left or right 
            rx = px 
            ry = py 
            dof = 8
        while(dof < 8):
            mx = int(rx) >> 6 
            my = int(ry) >> 6 
            mp = my*mapX+mx
            if(mp > 0 and mp < mapX*mapY and map[mp] == 1):
                # hit
                dof = 8 
                disH = math.cos(degToRad(ra))*(rx-px)-math.sin(degToRad(ra))*(ry-py)
            else:
                # check next horizontal
                rx += xo 
                ry += yo 
                dof += 1
        
        c = (0, 204, 0)
        if(disV < disH):
            # horizontal hit first
            rx = vx 
            ry = vy 
            disH = disV 
            c = (0, 153, 0)
        ca = FixAng(a-ra) 
        disH = disH*math.cos(degToRad(ca))  # fix fisheye
        lineH = (mapS*320)/(disH)
        lineOff = 160 - (lineH/2)  # line offset
        pygame.draw.line(w, c, (r*8, lineOff+lineH+ph), (r*8, lineOff+ph), 8)
        
        pygame.draw.line(w, (255, 0, 0), (r*8, lineOff+lineH+ph), (r*8, 512), 8)
        pygame.draw.line(w, (0, 0, 255), (r*8, 0), (r*8, lineOff+ph), 8)

        ra = FixAng(ra-1)  # go to next ray

running = True
while running:
    delta = c.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    w.fill((76, 76, 76))

    check(pygame.key.get_pressed())
    drawRays2D(ph)

    pygame.display.flip()
pygame.quit()
