#!/usr/bin/python3
from sense_hat import SenseHat
from time import sleep
import random
import math
sense = SenseHat()
sense.clear()
# examples using (x, y, r, g, b)
'''
sense.set_pixel(0, 0, 255, 0, 0)
sleep(1)
sense.set_pixel(0, 7, 0, 255, 0)
sleep(1)
sense.set_pixel(7, 0, 0, 0, 255)
sleep(1)
sense.set_pixel(7, 7, 255, 0, 255)
sleep(10)

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# examples using (x, y, pixel)
sense.set_pixel(0, 7, red)
sleep(1)
sense.set_pixel(7, 0, green)
sleep(1)
sense.set_pixel(7, 7, blue)
sleep(20)
sense.clear(100,100,100)


X = [255, 0, 0]  # Red
O = [255, 255, 255]  # White

question_mark = [
O, O, O, X, X, O, O, O,
O, O, X, O, O, X, O, O,
O, O, O, O, O, X, O, O,
O, O, O, O, X, O, O, O,
O, O, O, X, O, O, O, O,
O, O, O, X, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, X, O, O, O, O
]

sense.set_pixels(question_mark)
'''
max_x = 7
my_y = 7
origin = (0,0)
sense.set_pixel(origin[0], origin[1], 255, 255, 255)
print('Nullpunkt',origin)
def gerade(color): #einzelne pixel setzen und wieder löschen
    for i in range(0,max_x+1):
        sense.set_pixel(i, 0, color)
        print('color:',i)
        sleep(1)
    print('fertig anzuenden')    
    for a in range(max_x,-1,-1):
        sense.set_pixel(a, 0, 0, 0, 0)
        print('a:',a)
        sleep(1)
    print('fertig loeschen')

def kreis(color):
    center_x = float(input("Zentrum in X :"))
    print(center_x)
    center_y = 3.5
    radius = 3
 
    for x in range(8):
        for y in range(8):
            distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            if abs(distance - radius) < 0.5:
                sense.set_pixel(x, y, color)


def draw_line(x0, y0, x1, y1, color):
    #Bresenham-Algorithmus
    try:
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        doLoop = True
        while doLoop: 
            if 0 <= x0 < 8 and 0 <= y0 < 8:
                sense.set_pixel(x0, y0, color)
            
            if x0 == x1 and y0 == y1:
                doLoop=False
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
    except:
        print(f'ERROR: Einer der Parameter {x0, y0, x1, y1} ist kein gueltiger Wert')
def draw_pixel(x0, y0, x1, y1, color,interval):
    #Bresenham-Algorithmus
    try:
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        doLoop = True
        while doLoop: 
            if 0 <= x0 < 8 and 0 <= y0 < 8:
                sense.set_pixel(x0, y0, color)
                sleep(interval)
                sense.clear()
                
            if x0 == x1 and y0 == y1:
                doLoop=False
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
    except:
        print(f'ERROR: Einer der Parameter {x0, y0, x1, y1} ist kein gueltiger Wert')
def smiley(stimmung):
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)
    pixels = [(0, 0, 0)] * 64 #alle pixel schwarz
    
    # Augen
    sense.set_pixel(2, 2, YELLOW)
    sense.set_pixel(5, 2, YELLOW)

    if stimmung == "happy":       
        sense.set_pixel(2, 5, YELLOW)
        sense.set_pixel(3, 6, YELLOW)
        sense.set_pixel(4, 6, YELLOW)
        sense.set_pixel(5, 6, YELLOW)
        sense.set_pixel(6, 5, YELLOW)
    if stimmung == "traurig":       
        sense.set_pixel(2, 6, YELLOW)
        sense.set_pixel(3, 5, YELLOW)
        sense.set_pixel(4, 5, YELLOW)
        sense.set_pixel(5, 5, YELLOW)
        sense.set_pixel(6, 6, YELLOW)
    if stimmung == "hmm":       
        sense.set_pixel(3, 5, YELLOW)
        sense.set_pixel(4, 5, YELLOW)
        sense.set_pixel(5, 5, YELLOW)

    
    '''
    # Augen
    pixels[9] = YELLOW
    pixels[14] = YELLOW

    # Mund (einfacher Bogen)
    pixels[40] = YELLOW
    pixels[41] = YELLOW
    pixels[42] = YELLOW
    pixels[43] = YELLOW
    # Optional: Ecken des Mundes
    pixels[33] = YELLOW
    pixels[50] = YELLOW

    sense.set_pixels(pixels)
    '''
    
def pong(color):

    posX = 0
    posY = 3
    directionX = 1
    directionY = 1
    while True:
        sense.clear()
        sense.set_pixel(posX, posY,color)
        posX += directionX
        posY += directionY
        if posX > 7:
            posX = 6
            directionX *= -1
        elif posX < 0:
            posX = 1
            directionX *= -1

        if posY > 7:
            posY = 6
            directionY *= -1
        elif posY < 0:
            posY = 1
            directionY *= -1

        sleep(0.5)
def pong_zufall(color):

    posX = 0
    posY = 3
    directionX = 1
    directionY = 1
    #naechster punkt muss irgendwo am rand sein)
    while True:
        zahl_x = random.randint(7, 0)
        zahl_y = random.randint(0, 7)
        sense.clear()
        sense.set_pixel(posX, posY,color)
        posX += directionX
        posY += directionY
        if posX > 7:
            last_posX = posX
            posX = zahl_x
            directionX *= -1
        elif posX < 0:
            posX = 1
            directionX *= -1

        if posY > 7:
            last_pos_Y = posY
            posY = zahl_y
            directionY *= -1
        elif posY < 0:
            posY = 1
            directionY *= -1
        sleep(0.5)   







color = (0,255,0)  
#draw_line(0,0,5,7,color)
draw_pixel(0,0,5,7,color,0.5)
#kreis(color)   
#linie(color)    
#smiley("hmm")
#pong(color)
#pong_zufall(color)