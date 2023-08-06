#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 19:52:31 2021

@author: Ignacio Florido
"""
hastaprimo = int(input("Números primos y pares hasta este número: "))

def espar(n):
	for i in range(n):
		if(i % 2 == 0):
			print(f"{i} es un número par") 

def esprimo(n):
	for i in range(2, n):
		es_primo = True
		for j in range(2, i):
			if(i%j == 0):
				es_primo = False
		if(es_primo):
			print(f"{i} es un número primo") 

esprimo(hastaprimo)
espar(hastaprimo)