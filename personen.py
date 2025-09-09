#!/usr/bin/python
print("Hallo Welt")

class Person:
    def __init__(self,firstname=None,lastname=None):
        self.firstname = firstname
        self.lastname = lastname
        
    def __str__(self):
        return f'''
            Vorname:{self.__firstname}
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
    def lastname(self,new_firstName):
        self.__lastname = __firstnameName

if __name__ == '__main__':
    erst_person = Person(lastname='Altenburger',firstname='Markus')
    zweite_person = Person(lastname='Mueller',firstname='Peter')
    print(erst_person)
    erst_person.firstnamename = "Peter"
    print(e
    rst_person.firstname)
    zweite_person.lastname("Schlosser")
    print(zweite_person)
    zweite_person = erst_person