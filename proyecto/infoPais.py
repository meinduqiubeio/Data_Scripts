#!/usr/bin/python

from pyspark import SparkConf, SparkContext

import string
import sys
import os

conf = SparkConf().setMaster('local').setAppName('infoPais')
sc = SparkContext(conf = conf)

ruta1990 = os.getcwd() + "/1990/"

ruta2017 = os.getcwd() + "/2017/"

def info_to_number(info):
	if info == "inmigrantes":
		return 2
	if info == "natalidad":
		return 3
	if info == "mortalidad":
		return 4
	if info == "esperanza":
		return 5
	else:
		return -1

if len(sys.argv) != 3:
	print("Usage: infoPais.py [country] [inmigrantes|natalidad|mortalidad|esperanza]")
	exit(-1)
else:
	country = sys.argv[1].capitalize()

	number = info_to_number(sys.argv[2].lower())

	RDDvar = sc.textFile(ruta1990 + "Nodos.csv")

	words = RDDvar.filter(lambda line: country in line)

	if words.isEmpty():

		print "Este pais no esta en la lista!!!"

	else:

		if number == -1:

			print "Informacion no disponible!!!!"
			print("Usage: infoPais.py [country] [inmigrantes|natalidad|mortalidad|esperanza]")

		else:

			info = words.map(lambda line: (str(line.split(';')[1]),str(line.split(';')[number])))

			RDDvar1 = sc.textFile(ruta2017 + "Nodos.csv")

			words1 = RDDvar1.filter(lambda line: country in line)

			info1 = words1.map(lambda line: (str(line.split(';')[1]),str(line.split(';')[number])))

			array1 = info.collect()

			array2 = info1.collect()

			print

			print("-------------------------------")
			print " Country Info: ", sys.argv[2]
			print("-------------------------------")

			print array1[0], " % 1990", 

			print array2[0], " % 2017"

			print