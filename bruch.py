#!/usr/bin/python
print("Hallo Welt")
from math import gcd
class Bruchrechnen:
    def __init__(self,zaehler=None,nenner=None):
        if nenner == 0:
            raise ValueError("Nenner darf nicht 0 sein!")
        self.zaehler = int(zaehler)
        self.nenner = int(nenner)
        
    def __str__(self):
        return f"{self.zaehler}/{self.nenner}"
    @property
    def zaehler(self): 
        return self.__zaehler  
    @property
    def nenner(self): 
        return self.__nenner    
    @zaehler.setter
    def zaehler(self,new_zaehler):
        self.__zaehler = new_zaehler
    @nenner.setter
    def nenner(self,new_nenner):
        self.__nenner = new_nenner
    def bruch_div(self):
        teiler = gcd(zaehler, nenner)
        return self.zaehler / self.nenner
    def kuerzen():
        teiler = gcd(zaehler, nenner)
        self.zaehler //= teiler
        self.nenner //= teiler
if __name__ == '__main__':
    rechner = Bruchrechnen(zaehler = 11,nenner= 2)
    print(rechner.kuerzen)
