import os

def sacarNombre(row, columna):
	partirG = row.split(";")
	paisG=partirG[columna].split(" ")
	paisG=' '.join(paisG)
	paisG = paisG.split("-")
	paisG = ' '.join(paisG)
	return paisG, partirG

print("Mejores países para vivir en 2017")
ruta = os.getcwd() + "/2017"
os.chdir(ruta)

FichNodos = open('Nodos.csv', newline='', encoding='utf-8')
FichNodos.readline()

paises = {}
puntuacion = 0

for rowNodos in FichNodos.readlines():
    pais, linea = sacarNombre(rowNodos, 1)
    #Tasa de natalidad
    if linea[3] == "0":
        puntuacion = puntuacion - 70
    else:
        natalidad = linea[3].split(",")
        puntuacion = int(natalidad[0]) - puntuacion
    #Tasa de mortalidad
    if linea[4] == "0":
        puntuacion = puntuacion - 30
    else:
        mortalidad = linea[4].split(",")
        puntuacion = int(mortalidad[0]) - puntuacion
    #Esperanza de vida
    if linea[5] == "0":
        puntuacion = puntuacion + 65
    else:
        esperanzaVida = linea[5].split(",")
        puntuacion = int(esperanzaVida[0]) + puntuacion
    #Índice de paz
    if linea[6] == "0":
        puntuacion = puntuacion - 100
    else:
        puntuacion = int(linea[6]) - puntuacion
    #Capital humano
    if linea[7] == "0":
        puntuacion = puntuacion - 100
    else:
        puntuacion = int(linea[7]) - puntuacion
    #Indice de desarrollo humano
    if linea[8] == "0":
        puntuacion = puntuacion - 100
    else:
        puntuacion = int(linea[8]) - puntuacion

    paises[pais] = puntuacion
    puntuacion = 0


FichMejores = open('Mejores.csv', 'w')
FichMejores.write("pais;puntuacion" + '\n')


for i in paises:
    key = paises.get(i)
    FichMejores.write(str(i) + ";" + str(key) + "\n")

FichNodos.close()  
FichMejores.close()