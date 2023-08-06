# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 05:24:29 2021

@author: juank
"""

def calcula_mis_primos (num):

    primo = True

    for i in range(2,num):
        if(num%i==0):
            primo = False
    if primo:
        print("es mi primo")
    else: 
        print("no es mi primo")
    
    
#calcula_mis_primos(45)