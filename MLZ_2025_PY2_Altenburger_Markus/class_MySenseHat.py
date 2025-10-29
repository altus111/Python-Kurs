#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ====================================
# Autor: Markus Altenburger
# Erstellt am: 2025-10-01
# Beschreibung: Beschreibung des Skripts
# ====================================
from sense_hat import SenseHat
import time
import json
from class_Converter import Converter
class MySenseHat(SenseHat):
    def __init__(self):
        super().__init__()
        self.mconverter = Converter()
        self.width = 8
        self.height = 8
        self.buffer = [(0, 0, 0)] * (self.width * self.height) #stellt die 64 Pixel dar und Farbe dar.
    def chkValue(self,value):
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            try:
                num = float(value)     
                num =round(num)
                return num
            except ValueError:
                return None  # String war keine Zahl (z. B. 'hallo')
    def get_pixel(self, x, y,typ=None):
        if typ == 'None':
            return tuple(super().get_pixel(x, y))
        elif typ == 'json':
            json_output = json.dumps({"color": tuple(super().get_pixel(x, y))})
            return json_output
            

    def get_pixels(self):
        pixels = super().get_pixels()
        tmp_pixel = {}
        tmp_pixels =[]
        for i, p in enumerate(pixels):
            tmp_pixel={f'index = {i}': (f'color = {p}', f'coordinates = {self.mconverter.get_coordinates_by_index(i)}')}
            tmp_pixels.append(tmp_pixel)
        self.buffer = pixels
        return tmp_pixels

    def clear(self, color=(0,0,0)):
        self.buffer = [color] * (self.width * self.height)
        self.render()
    def render(self):  #alles auf einmal anzeigen
        super().set_pixels(self.buffer)

    def flip_v(self):
        """Spiegelt die LED-Matrix vertikal (oben ↔ unten)."""
        pixels = self.get_pixels()
        # Umwandeln in 8x8 Matrix
        matrix = [pixels[i*8:(i+1)*8] for i in range(8)]

        # Vertikal spiegeln: Reihen umdrehen
        flipped = list(reversed(matrix))

        # Zurück in flache Liste
        flat = [pixel for row in flipped for pixel in row]
        super.set_pixels(flat)
        print("Matrix vertikal gespiegelt.")

    def flip_h(self):
        """Spiegelt die LED-Matrix horizontal (links ↔ rechts)."""
        pixels = self.get_pixels()
        # Umwandeln in 8x8 Matrix
        matrix = [pixels[i*8:(i+1)*8] for i in range(8)]

        # Horizontal spiegeln: Jede Zeile umdrehen
        flipped = [list(reversed(row)) for row in matrix]

        # Zurück in flache Liste
        flat = [pixel for row in flipped for pixel in row]
        super().set_pixels(flat)
        print("Matrix horizontal gespiegelt.")

    def rotate(self, angle=90):
        """Dreht die aktuelle LED-Matrix um 90°, 180° oder 270°."""
        pixels = self.get_pixels()
        # Umwandeln in 8x8 Matrix
        matrix = [pixels[i*8:(i+1)*8] for i in range(8)]

        if angle == 90:
            rotated = [list(reversed(col)) for col in zip(*matrix)]
        elif angle == 180:
            rotated = [list(reversed(row)) for row in reversed(matrix)]
        elif angle == 270:
            rotated = [list(col) for col in reversed(list(zip(*matrix)))]
        else:
            print("Nur 90, 180 oder 270 Grad erlaubt.")
            return

        # Zurück in flache Liste
        flat = [pixel for row in rotated for pixel in row]
        super().set_pixels(flat)
        print(f"Matrix um {angle}° gedreht.")



    def set_pixel(self, x, y, color=(255, 255, 255),received_parameter = None, arguments=None):
        orig_x = x
        orig_y = y
        try:
            x = self.chkValue(x)
            y = self.chkValue(y)
            if 0 <= x < self.width and 0 <= y < self.height:
                super().set_pixel(x, y,color)
            else:
                print(f"Error: Pixel-Koordinaten ({x}, {y}) ausserhalb des gueltigen Bereichs.")
        except:
            print(f"Die Werte {orig_x}, {orig_y} sind ungültig.")

    def draw_line(self, x_start, y_start, x_end, y_end, color=(255, 255, 255),speed=0):
            # Sonderfall: vertikale Linie
            if x_start == x_end:
                y_min, y_max = sorted([y_start, y_end]) # y_min ist der kleinere Wert.sorted = Sortieren von klein nach gross
                for y in range(y_min, y_max + 1):
                    self.set_pixel(x_start, y, color=color)
                    time.sleep(speed)
                return

            # Steigung a und Achsenabschnitt b
            a = (y_end - y_start) / (x_end - x_start)
            b = y_start - a * x_start

            # Fall 1: flache Steigung (|a| <= 1) → über x iterieren
            if abs(a) <= 1:
                x_min, x_max = sorted([x_start, x_end])
                for x in range(x_min, x_max + 1):
                    y = round(a * x + b)
                    self.set_pixel(x, y, color=color)
                    time.sleep(speed)

            # Fall 2: steile Steigung (|a| > 1) → über y iterieren
            else:
                self.draw_line_bres(x_start, y_start, x_end, y_end, color)
                y_min, y_max = sorted([y_start, y_end])
                for y in range(y_min, y_max + 1): #zum vergleich
                    x = round((y - b) / a)
                    self.set_pixel(x, y, color=color)
                    time.sleep(speed)
    # Linie mit Bresenham-Algorithmus
    def draw_line_bres(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            self.set_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

if __name__ == "__main__":
    #from class_MySenseHat import MySenseHat
    import time
    sense = MySenseHat()
    sense.clear()
     
    #sense.set_pixel(0, 0, (255, 200, 0))  #nullpunkt
    #sense.set_pixel(4, 5, (255, 0, 0)) # Punkt 2.1
    #sense.set_pixel(8, 5, (255, 255, 0))    # Punkt 2.2.1
    #sense.set_pixel('6.1', '5', (255, 0, 0)) # Punkt 2.2.2
    #sense.set_pixel('3', '3', (255, 255, 0))  # Punkt 2.2.3
    #sense.set_pixel('test', '5', (255, 0, 0)) # Punkt 2.2.3
    #sense.draw_line(0, 0, 7, 7, (0, 255, 0))  # Diagonale
    #sense.draw_line(0, 0, 10, 10, (255, 255, 255))  # Diagonale mit Werten ausserhalb des Bereichs
    #sense.draw_line(0, 7, 3, 0, (0, 0, 255))  # flache Steigung
    #sense.draw_line(0, 0, 7, 2, (0, 255, 255))  # steile Steigung
    #sense.draw_line(0, 5, 7, 5, (255, 255, 255))  # Horizontale Linie
    sense.draw_line(3, 2, 3, 7, (255, 0, 255))  # Vertikale Linie
    time.sleep(2)
    sense.flip_v()
    time.sleep(2)
    sense.flip_h()
    #sense.rotate(135)
    #sense.rotate(180)
    #sense.rotate(270) 
    #sense.rotate(135)  # ungültiger Wert
