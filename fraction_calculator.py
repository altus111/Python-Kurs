#!/usr/bin/python
from Class_Bruch import *
import pydoc
bruch_1 = Fraction(bruch_str='')
print("Bruch 1: ", bruch_1)

#help(Fraction)
print(bruch_1.to_decimal.__doc__)
hilfe_text = pydoc.render_doc(Fraction,title="Hilfe fuer %s")
print(hilfe_text)
