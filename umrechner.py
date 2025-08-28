#!/usr/bin/python

# ------------------------------------------------------------------
# Name  : umrechner.py
# Source: 
# Description:
#
# Autor: Markus Altenburger
#
# History:
# 25.8.2025   Markus Altenburger      Initial Version
# 
# ------------------------------------------------------------------import math
import math
# const / Globale Variable
pi = math.pi

# Function
def VT52_cls():
    print("\033[2J",end="", flush=True)   # set cursor to home position

def VT52_home():
    print("\033[H",end="", flush=True)    # set cursor to home position

def VT52_cls_home():
    VT52_cls()
    VT52_home()
def halt(prompt="Weiter?"):
    return input(prompt)

# Umrechnungsformeln
# -------------------------
def grad2Rad(grad):
    return math.pi*grad/180

def rad2Grad(rad):
    return 180*rad/math.pi

def fahrenheit2Celsius(fahrenheit):
    return (fahrenheit-32)/1.8
	
def celsius2Fahrenheit(celsius):
    return (celsius*1.8)+32


def read_float(prompt, min=None, max=None):
    has_error = True
    float_val = 0.0  # Initialisierung, damit return funktioniert, falls etwas schiefgeht

    while has_error:
        try:
            float_str = input(prompt)
            float_val = float(float_str)

            if min is not None and float_val < min:
                print(f'ERROR: {float_val} ist kleiner als das Minimum {min}')
            elif max is not None and float_val > max:
                print(f'ERROR: {float_val} ist groeßer als das Maximum {max}')
            else:
                has_error = False

        except ValueError:
            print(f'ERROR: {float_str} ist kein gueltiger Float-Wert')
    return float_val
        
 
def read_int(prompt, min=None, max=None):
    has_error = True
    int_val = 0

    while has_error:
        try:
            int_str = input(prompt)
            int_val = int(int_str)  # korrekt: Umwandlung in int

            if min is not None and int_val < min:
                print(f'ERROR: {int_val} ist kleiner als das Minimum {min}')
            elif max is not None and int_val > max:
                print(f'ERROR: {int_val} ist groeßer als das Maximum {max}')
            else:
                has_error = False

        except ValueError:
            print(f'ERROR: {int_str} ist kein gueltiger Integer-Wert')

    return int_val

doLoop = True
while doLoop:
    print("\033[2J",end="", flush=True)   # clear Screen
    print("\033[H",end="", flush=True)    # set cursor to home position
    print("Umrechnungen")
    print("============")
    print("  1: Grad in Bogenmass") #rad  = grad*pi/180
    print("  2:Bogenmass in Grad") #grad = rad*180/pi
    print("  3:Fahrenheit in Celsius")
    print("  4 Celsius in Fahrenheit")
    print("  0 Abbruch")
    antwort = input("Waehle ein Menu aus :")
    if (antwort == "1"):
        VT52_cls_home()
        print("Grad --> Bogenmass")
        gradValue = float(input("Grad: "))
        radValue  = grad2Rad(gradValue)
        print("Grad={grad:1.2f}  ==> Rad={rad:1.2f}".format(grad=gradValue,rad=radValue))
        halt()

    if (antwort == "2"):
        VT52_cls_home()
        print("Bogenmass --> Grad")
        radValue = float(input("Rad: "))
        gradValue  = read_float(rad2Grad(radValue))
        print("Rad={rad:1.2f}  ==> Grad={grad:1.2f}".format(grad=gradValue,rad=radValue))
        halt()

    if (antwort == "3"):
        VT52_cls_home()
        print("Fahrenheit --> Celsius")
        fahrValue = float(input("Fahrenheit: "))
        gradValue  = fahrenheit2Celsius(fahrValue)
        print("Fahrenheit={fahr:1.2f}  ==> Celsius={cel:1.2f}".format(cel=gradValue,fahr=fahrValue))
        halt()

    if (antwort == "4"):
        VT52_cls_home()
        print("Celsius --> Fahrenheit")
        gradValue = float(input("Celsius: "))
        fahrValue  = celsius2Fahrenheit(gradValue)
        print("Celsius={cel:1.2f}  ==> Fahrenheit={fahr:1.2f}".format(cel=gradValue,fahr=fahrValue))
        halt()
			
    if (antwort == "0"):
        doLoop = False
         
 #print("Ende....Done")
 