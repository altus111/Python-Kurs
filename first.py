#!/usr/bin/python
vorname='Markus'
anzahl=67
preis=567.8
schalter_ein=True
nachname="Altenburger"
Langer_text = '''
Das ist ein langer text
'''
ganzer_name = vorname + " " + nachname
print ('hello HBU',vorname,nachname, Langer_text)
print(ganzer_name, anzahl*preis, "Zeilen", sep='Trenner',end="\n\n")

print("Schluss")