#!/usr/bin/python

from pyspark import SparkConf, SparkContext

import string
import sys
import os

conf = SparkConf().setMaster('local').setAppName('comparaPais')
sc = SparkContext(conf = conf)

ruta1990 = os.getcwd() + "/1990/"

ruta2017 = os.getcwd() + "/2017/"

if len(sys.argv) != 4:
	print("Usage: comparaPais.py [country1] [country2] [year]")
	exit(-1)
else:
	country1 = sys.argv[1].capitalize()

	country2 = sys.argv[2].capitalize()

	year = int(sys.argv[3])

	if year == 2017:

		ruta = os.getcwd() + "/2017/"

	else:
		if year == 1990:

			ruta = os.getcwd() + "/1990/"

		else:

			print "No es un anyo valido!!!"
			print("Usage: comparaPais.py [country1] [country2] [2017|1990]")
			exit(-1)


	RDDvar = sc.textFile(ruta + "Nodos.csv")

	words = RDDvar.filter(lambda line: country1 in line)

	words1 = RDDvar.filter(lambda line: country2 in line)

	result = words.map(lambda line: line.replace(";","    "))

	result1 = words1.map(lambda line: line.replace(";","    "))

	if words.isEmpty() or words1.isEmpty():

		print "Este pais no esta en la lista!!!"

	else:

		array1 = result.collect()

		array2 = result1.collect()

		print

		print("**********************************************************")
		print " Compare: ", country1, " and ", country2, "Year:", year
		print("**********************************************************")

		print 

		print "id:    Pais:     Inm:     TNa:     TMo     EVi: "

		print("**********************************************************")

		print("----------------------------------------------------------")

		print array1[0]

		print("----------------------------------------------------------")

		print array2[0]

		print("----------------------------------------------------------")

		print