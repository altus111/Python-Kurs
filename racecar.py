#!/usr/bin/python3

# ------------------------------------------------------------------
# Name  : Car.py
# Source: https://raw.githubusercontent.com/walter-rothlin/Source-Code/master/Python_WaltisExamples/_Libraries/School_Examples/Car.py
#
# Description: Beispiel einer Klasse und Sub-Klasse mit Properties,....
#
#
# Autor: Walter Rothlin
#
# History:
# 14-Jun-2022   Walter Rothlin      Initial Version (Class Car and derived class Racecar)
# 28-Jun-2022   Walter Rothlin      Property (leistung),
#                                   Dynamische Attribute (Aufkleber),
#                                   Klassvariablen (Wartungsintervall),
#                                   Statische Methoden (production_statistik)
# 28-Jun-2022   Walter Rothlin      Property (leistung)
# 20-Nov-2023   Walter Rothlin      Extended for HBU_2023
# 20-Nov-2023   Walter Rothlin      Splitted Racecar und Car in two files
# ------------------------------------------------------------------
from Car import Car, Colors
class Car:
    """This class represents a car."""
    def __init__(self, marke="VW", farbe=Colors.WHITE, v=0, max_speed=160):
        """
        Initializes a new Car object.

        :param marke: The brand of the car.
        :param farbe: The color of the car.
        :param v: The speed of the car.
        :param max_speed: The maximum speed of the car.
        """
        self.__marke = marke
        self.__farbe = farbe
        self.__v = v
        self.__max_speed = max_speed
        self.__engine_power = 100  # in PS
        self.__aufkleber = []  # Dynamic attribute - list of stickers on the car

    def __str__(self):
        return f"Marke: {self.__marke}, Farbe: {self.__farbe}, Speed: {self.__v} km/h, MaxSpeed: {self.__max_speed} km/h, Leistung: {self.__engine_power} PS, Aufkleber: {self.__aufkleber}"

    def setSpeed(self, newSpeed):
        if newSpeed < 0:
            self.__v = 0
        elif newSpeed > self.__max_speed:
            self.__v = self.__max_speed
        else:
            self.__v = newSpeed

    @property
    def engine_power(self):
        return self.__engine_power

    @engine_power.setter
    def engine_power(self, new_leistung):
        if new_leistung < 50:
            self.__engine_power = 50
        elif new_leistung > 500:
            self.__engine_power = 500
        else:
            self.__engine_power = new_leistung

    def set_leistung(self, new_leistung, min_P=50, max_P=500, trace=True):
        """
        Sets the power of the car.

        :param new_leistung: The new power value.
        :param min_P: Minimum allowed power.
        :param max_P: Maximum allowed power.
        :param trace: If True, prints debug information.
        """
        if trace:
            print('Car::set_leistung() has been called!')
        if new_leistung < min_P:
            self.__engine_power = min_P
            if trace:
                print(f'Power too low. Set to minimum')
                      
class Racecar(Car):
    """This class represents a racecar, which is a type of car."""
    def __init__(self, marke="Ferrari", farbe=Colors.RED, v=0, maxSpeed=200, gewicht=800):
        """
        Initializes a new Racecar object.

        :param marke: The brand of the racecar.
        :param farbe: The color of the racecar.
        :param v: The speed of the racecar.
        :param maxSpeed: The maximum speed of the racecar.
        :param gewicht: The weight of the racecar.
        """
        super().__init__(marke=marke, farbe=farbe, v=v, max_speed=maxSpeed)
        self.__gewicht = gewicht

    def __str__(self):
        return "Racecar :: " + "Gewicht:" + str(self.__gewicht) + super().__str__()

    def setSpeed(self, newSpeed):
        super().setSpeed(newSpeed)

    def set_leistung(self, new_leistung, min_P=550, max_P=1500, trace=True):
        """
        Sets the power of the car.

        :param new_leistung: The new power value.
        """
        if trace:
            print('Racecar::set_leistung() has been called!')
        super().set_leistung(new_leistung, min_P=min_P, max_P=max_P, trace=False)

if __name__ == '__main__':
    waltisCar = Car('Opel', Colors.BLUE)
    waltisCar.setSpeed(80)
    print(f'waltisCar: {waltisCar}')
    claudiasCar = Car()
    claudiasCar.setSpeed(120)
    print(f'claudiasCar: {claudiasCar}')


    schumisCar = Racecar(marke="Ferrari", farbe=Colors.RED, gewicht= 820, maxSpeed=340)
    schumisCar.setSpeed(223)
    print(f'schumisCar: {schumisCar}')

    maxsCar = Racecar()
    maxsCar.setSpeed(120)
    maxsCar.engine_power = 200
    maxsCar.set_leistung(1100)
    maxsCar.set_leistung(1100)
    maxsCar.set_leistung(5500, max_P=6000)
    print(f'maxsCar: {maxsCar}')
