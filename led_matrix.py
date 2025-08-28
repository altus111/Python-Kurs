#!/usr/bin/python3
from sense_hat import SenseHat
from time import sleep
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
origin = (7,0)
sense.set_pixel(origin[0], origin[1], 255, 255, 255)
print('Nullpunkt',origin)
def gerade():
    for i in range(0,max_x+1):
        sense.set_pixel(i, 0, 255, 0, 0)
        print('i:',i)
        sleep(1)
    print('fertig anzuenden')    
    for a in range(max_x,-1,-1):
        sense.set_pixel(a, 0, 0, 0, 0)
        print('a:',a)
        sleep(1)
    print('fertig loeschen')

def kreis():
    center_x = float(input("Zentrum in X :"))
    print(center_x)
    center_y = 3.5
    radius = 3
    color = (255,0,0)
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
  
color = (0,255,0)  
#draw_line(0,0,4,7,color)
#kreis()   
#linie()    