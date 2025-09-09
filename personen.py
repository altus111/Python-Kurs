#!/usr/bin/python
print("Hallo Welt")

class Person:
    def __init__(self,firstname=None,lastname=None):
        self.firstname = firstname
        self.lastname = lastname
        
    def __str__(self):
        return f'''
            Vorname:{self.firstname}
            Nachname:{self.lastname}
        '''
    @property
    def lastname(self): 
        return self.__lastname  
        
    @lastname.setter
    def lastname(self,new_lastName):
        self.__lastname = new_lastName

    @property
    def firstname(self): 
        return self.__firstname
    
    @firstname.setter
    def firstname(self,new_firstName):
        self.__firstname = new_firstName

if __name__ == '__main__':
    erst_person = Person(lastname='Altenburger',firstname='Markus')
    zweite_person = Person(lastname='Mueller',firstname='Peter')
    print(erst_person)
    erst_person.firstname = "Peter"
    print(erst_person.firstname)
    zweite_person.lastname="Schlosser"
    print(zweite_person)
