# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 16:36:47 2021

@author: pablo.ruiz
"""

def num_primos(a):
  primos=[]
  x = 0
  y = 0
  primo = 's'
  while (x < a):
    x += 1
    for n in range(2, x):
      if x % n == 0: # No es primo
        primo = 'n'
        break
    if primo != 'n':
      primos.append (x)
      y += 1
    else:
      primo = 's'
  print("Hay " + str(y) + " números primos entre 1 y " + str(a) + "." + "\n\nSon:" )
  return (primos)