#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 19:52:31 2021

@author: Jose
"""
n = int(input("introduce un número para ver si es primo: "))
print("el numero que has introducido es: ", n)
def primo(n):
	for i in range(2, n):
		seria_primo = True
		for j in range(2, i):
			if(i%j == 0):
				seria_primo = False
		if(seria_primo):
			print(f"{i} es primo")

primo(n)
