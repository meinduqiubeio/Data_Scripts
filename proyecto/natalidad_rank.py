#!/usr/bin/python

from pyspark import SparkConf, SparkContext

import string
import sys
import os

conf = SparkConf().setMaster('local').setAppName('esperanzaRank')
sc = SparkContext(conf = conf)

ruta1990 = os.getcwd() + "/1990/"

ruta2017 = os.getcwd() + "/2017/"

RDDvar = sc.textFile(ruta1990 + "Nodos.csv")

words = RDDvar.filter(lambda line: "id" not in line and "none" not in line)

orden = words.sortBy(lambda line: int((line.split(';')[3]).split(",")[0]), ascending = 0)

natalidad1 = orden.map(lambda line: (str(line.split(';')[1]), str(line.split(';')[3])))

RDDvar1 = sc.textFile(ruta2017 + "Nodos.csv")

words1 = RDDvar1.filter(lambda line: "id" not in line and "none" not in line)

orden1 = words1.sortBy(lambda line: int((line.split(';')[3]).split(",")[0]), ascending = 0)

natalidad2 = orden1.map(lambda line: (str(line.split(';')[1]),str(line.split(';')[3])))

array1 = natalidad1.collect()

array2 = natalidad2.collect()

print("-------------------------------")
print("      Natalidad 1990     	  ")
print("-------------------------------")

i = 0
for i in range(5):
	print "   ", array1[i], "%"

print

print("-------------------------------")
print("      Natalidad 2019     	  ")
print("-------------------------------")

j = 0

for j in range(5):
	print "   ", array2[j], "%"

print