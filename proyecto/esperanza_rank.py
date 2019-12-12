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

esperanza1 = words.map(lambda line: (str(line.split(';')[1]),str(line.split(';')[5])))

RDDvar1 = sc.textFile(ruta2017 + "Nodos.csv")

words1 = RDDvar1.filter(lambda line: "id" not in line and "none" not in line)

esperanza2 = words1.map(lambda line: (str(line.split(';')[1]),str(line.split(';')[5])))

total1 = esperanza1.sortBy(lambda x: x[1], ascending = 0)

total2 = esperanza2.sortBy(lambda x: x[1], ascending = 0)

array1 = total1.collect()

array2 = total2.collect()

print("-------------------------------")
print("    Esperanza de vida 1990     ")
print("-------------------------------")

for i in range(5):
	print "   ", array1[i], "%"

print

print("-------------------------------")
print("    Esperanza de vida 1990     ")
print("-------------------------------")

for j in range(5):
	print "   ", array2[j], "%"

print

