#!/usr/bin/python3
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
sense.clear()
sleep(1)
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
origin = (0,7)
sense.set_pixel(origin[0], origin[1], 255, 0, 0)
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