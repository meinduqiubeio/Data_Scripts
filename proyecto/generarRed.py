import unidecode
import os

#Obtenemos el nombre del país, teniendo en cuenta que puede haber nombres con espacios o con (-) 
# (ej: Estados Unidos, Birmania - Myanmar)
def sacarNombre(row, columna):
	partirG = row.split(";")
	paisG=partirG[columna].split(" ")
	paisG.pop()
	paisG=' '.join(paisG)
	paisG = paisG.split("-")
	paisG = ' '.join(paisG)
	return paisG, partirG

#-------------------------

#Indicamos la red que queremos generar
print("Red a generar: 1990 o 2017")
red = input()
ruta1 = "/" + red
ruta = os.getcwd() + ruta1
os.chdir(ruta)

#Abrimos todos los ficheros que vamos a necesitar para la generación de la tabla de nodos

#Ficheros de datos comunes de 2017 y 1990: nombre de los países, número de inmigrantes, tasa de natalidad, 
#tasa de mortalidad y esperanza de vida al nacer

#Ficheros de datos que solo pertenecen a 2017: índice de paz 
FilePaises= open('TodosPaises.csv', newline='', encoding='utf-8')
FileNatalidad = open('TasaNatalidad.csv', newline='', encoding='utf-8')
FileMortalidad = open('TasaMortalidad.csv', newline='', encoding='utf-8')
FileEsperanzaDeVida = open('EsperanzaDeVida.csv', newline='', encoding='utf-8')
#Las primeras líneas se descartan porque contienen los nombres de las columnas de la tabla csv
FilePaises.readline()
FileNatalidad.readline()
FileMortalidad.readline()
FileEsperanzaDeVida.readline()

if red == "2017":
	FilePaz = open('IndicePaz.csv', newline='', encoding='utf-8')
	FileCapitalHumano = open('CapitalHumano.csv', newline='', encoding='utf-8')
	FileDesarrolloHumano = open('IndiceDesarrolloHumano.csv', newline='', encoding='utf-8')
	FilePaz.readline()
	FileCapitalHumano.readline()
	FileDesarrolloHumano.readline()

#-------------------------
#Para sacar los datos: se lee línea a línea los ficheros, compara el orden de los nombres de los países 
#para asegurarnos de que tenemos toda la información (0 si no se tiene su índice social) y
#añade o actualiza los datos en los diccionarios.

#Cada vez que terminamos de insertar los datos de un índice social en el fichero Nodos, ponemos el puntero
#del fichero en el inicio del fichero TodosPaises para volver a realizar una lectura. Al finalizar, cerramos
#todos los archivos

#Creamos el fichero de los nodos
fNodos = open('Nodos.csv', 'w')
if red == "2017":
	fNodos.write("id;label;numInmigrantes;tasaNatalidad;tasaMortalidad;esperanzaDeVida;indicePaz;capitalHumano;indiceDesarrolloHumano" + '\n')
else:
	fNodos.write("id;label;numInmigrantes;tasaNatalidad;tasaMortalidad;esperanzaDeVida" + '\n')
#Id de los nodos 
id = 0
#Diccionario para guardar el nombre del país y su lista de indicadores sociales
paisId = {}
caractNodo = []

#Extracción de datos comunes

#Número de inmigrantes
for rowPais in FilePaises.readlines():
	pais, partir = sacarNombre(rowPais, 1)
	inmigrantes = partir[5]
	if len(inmigrantes)>3:
				inmigrantes = inmigrantes.split(".")
				inmigrantes= ''.join(inmigrantes)
	pais = unidecode.unidecode(pais)
	caractNodo = [id, inmigrantes]
	paisId.update({pais:caractNodo})
	id = id + 1

#Tasa de natalidad
FilePaises.seek(0)
FilePaises.readline()

for rowNatalidad in FileNatalidad.readlines():
	rowPais = FilePaises.readline()
	pais, partir = sacarNombre(rowPais, 1)
	paisNatalidad, partirNatalidad = sacarNombre(rowNatalidad, 1)

	while pais != paisNatalidad:
		pais = unidecode.unidecode(pais)
		caractNodo = paisId[pais]
		id = caractNodo[0]
		inmigrantes = caractNodo[1]
		caractNodo = [id, inmigrantes, 0]
		paisId.update({pais:caractNodo})
		id = id +1

		rowPais = FilePaises.readline()
		pais, partir = sacarNombre(rowPais, 1)
		
	tasaNatalidad = partirNatalidad[7].split("‰")
	tasaNatalidad = tasaNatalidad[0]
	pais = unidecode.unidecode(pais)
	caractNodo = paisId[pais]
	id = caractNodo[0]
	inmigrantes = caractNodo[1]
	caractNodo = [id, inmigrantes, tasaNatalidad]
	paisId.update({pais:caractNodo})
	id = id + 1

#Tasa de mortalidad
FilePaises.seek(0)
FilePaises.readline()
for rowMortalidad in FileMortalidad.readlines():
	rowPais = FilePaises.readline()
	pais, partir = sacarNombre(rowPais, 1)
	paisMortalidad, partirMortalidad = sacarNombre(rowMortalidad, 1)
	
	while pais != paisMortalidad:
		pais = unidecode.unidecode(pais)
		caractNodo = paisId[pais]
		id = caractNodo[0]
		inmigrantes = caractNodo[1]
		tasaNatalidad = caractNodo[2]
		caractNodo = [id, inmigrantes, tasaNatalidad, 0]
		paisId.update({pais:caractNodo})
		id = id +1

		rowPais = FilePaises.readline()
		pais, partir = sacarNombre(rowPais, 1)
		
	tasaMortalidad = partirMortalidad[5].split("‰")
	tasaMortalidad = tasaMortalidad[0]
	pais = unidecode.unidecode(pais)
	caractNodo = paisId[pais]
	id = caractNodo[0]
	inmigrantes = caractNodo[1]
	tasaNatalidad = caractNodo[2]
	caractNodo = [id, inmigrantes, tasaNatalidad, tasaMortalidad]
	paisId.update({pais:caractNodo})
	id = id + 1
	
#Esperanza de vida al nacer
FilePaises.seek(0)
FilePaises.readline()

for rowEsperanzaVida in FileEsperanzaDeVida.readlines():
	rowPais = FilePaises.readline()
	
	pais, partir = sacarNombre(rowPais, 1)
	paisEsperanzaVida, partirEsperanzaVida = sacarNombre(rowEsperanzaVida, 1)
	
	while pais != paisEsperanzaVida:
		pais = unidecode.unidecode(pais)
		caractNodo = paisId[pais]
		id = caractNodo[0]
		inmigrantes = caractNodo[1]
		tasaNatalidad = caractNodo[2]
		tasaMortalidad = caractNodo[3]
		caractNodo = [id, inmigrantes, tasaNatalidad, tasaMortalidad, 0]
		paisId.update({pais:caractNodo})
		id = id +1
		
		rowPais = FilePaises.readline()
		pais, partir = sacarNombre(rowPais, 1)
		
	esperanzaDeVida = partirEsperanzaVida[6]
	pais = unidecode.unidecode(pais)
	caractNodo = paisId[pais]
	id = caractNodo[0]
	inmigrantes = caractNodo[1]
	tasaNatalidad = caractNodo[2]
	tasaMortalidad = caractNodo[3]
	caractNodo = [id, inmigrantes, tasaNatalidad, tasaMortalidad, esperanzaDeVida]
	paisId.update({pais:caractNodo})
	id = id + 1

#Extracción de datos únicos de 2017

if red == "2017":
#Índice de paz
	FilePaises.seek(0)
	FilePaises.readline()
	for rowPaz in FilePaz.readlines():
		rowPais = FilePaises.readline()
		pais, partir = sacarNombre(rowPais, 1)
		paisPaz, partirPaz = sacarNombre(rowPaz, 1)
		
		while pais != paisPaz:
			pais = unidecode.unidecode(pais)
			caractNodo = paisId[pais]
			id = caractNodo[0]
			inmigrantes = caractNodo[1]
			tasaNatalidad = caractNodo[2]
			tasaMortalidad = caractNodo[3]
			esperanzaDeVida = caractNodo[4]
			caractNodo = [id, inmigrantes, tasaNatalidad, tasaMortalidad, esperanzaDeVida, 0]
			paisId.update({pais:caractNodo})
			id = id +1

			rowPais = FilePaises.readline()
			pais, partir = sacarNombre(rowPais, 1)
	
		indicePaz = partirPaz[4].split("º")
		indicePaz = indicePaz[0]
		pais = unidecode.unidecode(pais)
		caractNodo = paisId[pais]

		id = caractNodo[0]
		inmigrantes = caractNodo[1]
		tasaNatalidad = caractNodo[2]
		tasaMortalidad = caractNodo[3]
		esperanzaDeVida = caractNodo[4]
		pais = unidecode.unidecode(pais)
		caractNodo = [id, inmigrantes, tasaNatalidad, tasaMortalidad, esperanzaDeVida, indicePaz]
		paisId.update({pais:caractNodo})
		id = id + 1

	#Capital humano
	FilePaises.seek(0)
	FilePaises.readline()
	for rowCapital in FileCapitalHumano.readlines():
		rowPais = FilePaises.readline()
		pais, partir = sacarNombre(rowPais, 1)
		paisCapital, partirCapital = sacarNombre(rowCapital, 1)
		
		while pais != paisCapital:
			pais = unidecode.unidecode(pais)
			caractNodo = paisId[pais]
			id = caractNodo[0]
			inmigrantes = caractNodo[1]
			tasaNatalidad = caractNodo[2]
			tasaMortalidad = caractNodo[3]
			esperanzaDeVida = caractNodo[4]
			indicePaz = caractNodo[5]
			caractNodo = [id, inmigrantes, tasaNatalidad, tasaMortalidad, esperanzaDeVida, indicePaz, 0]
			paisId.update({pais:caractNodo})
			id = id + 1

			rowPais = FilePaises.readline()
			pais, partir = sacarNombre(rowPais, 1)
	
		capitalHumano = partirCapital[3].split("º")
		capitalHumano = capitalHumano[0]
		pais = unidecode.unidecode(pais)
		caractNodo = paisId[pais]

		id = caractNodo[0]
		inmigrantes = caractNodo[1]
		tasaNatalidad = caractNodo[2]
		tasaMortalidad = caractNodo[3]
		esperanzaDeVida = caractNodo[4]
		indicePaz = caractNodo[5]
		pais = unidecode.unidecode(pais)
		caractNodo = [id, inmigrantes, tasaNatalidad, tasaMortalidad, esperanzaDeVida, indicePaz, capitalHumano]
		paisId.update({pais:caractNodo})
		id = id + 1
	
	#Índice de desarrollo humano
	FilePaises.seek(0)
	FilePaises.readline()
	for rowDesarrollo in FileDesarrolloHumano.readlines():
		rowPais = FilePaises.readline()
		pais, partir = sacarNombre(rowPais, 1)
		paisDesarrollo, partirDesarrollo = sacarNombre(rowDesarrollo, 1)
		
		while pais != paisDesarrollo:
			pais = unidecode.unidecode(pais)
			caractNodo = paisId[pais]
			id = caractNodo[0]
			inmigrantes = caractNodo[1]
			tasaNatalidad = caractNodo[2]
			tasaMortalidad = caractNodo[3]
			esperanzaDeVida = caractNodo[4]
			indicePaz = caractNodo[5]
			capitalHumano = caractNodo[6]
			caractNodo = [id, inmigrantes, tasaNatalidad, tasaMortalidad, esperanzaDeVida, indicePaz, capitalHumano, 0]
			paisId.update({pais:caractNodo})
			id = id +1

			rowPais = FilePaises.readline()
			pais, partir = sacarNombre(rowPais, 1)
	
		desarrolloHumano = partirDesarrollo[4].split("º")
		desarrolloHumano = desarrolloHumano[0]
		pais = unidecode.unidecode(pais)
		caractNodo = paisId[pais]

		id = caractNodo[0]
		inmigrantes = caractNodo[1]
		tasaNatalidad = caractNodo[2]
		tasaMortalidad = caractNodo[3]
		esperanzaDeVida = caractNodo[4]
		indicePaz = caractNodo[5]
		capitalHumano = caractNodo[6]
		pais = unidecode.unidecode(pais)
		caractNodo = [id, inmigrantes, tasaNatalidad, tasaMortalidad, esperanzaDeVida, indicePaz, capitalHumano, desarrolloHumano]
		paisId.update({pais:caractNodo})
		id = id + 1


#Cerramos los ficheros
FilePaises.close()
FileNatalidad.close()
FileMortalidad.close()
FileEsperanzaDeVida.close()
if red == "2017":
	FilePaz.close()
	FileCapitalHumano.close()
	FileDesarrolloHumano.close()

#-------------------------
#Abrimos todos los ficheros que vamos a necesitar para la generación de la tabla de nodos, que están dentro
#de la carpeta Aristas
rutaAct = os.getcwd() + "/Aristas"
#Formar una lista con todos los archivos de la ruta
listaAristas = os.listdir(rutaAct)
#Creamos el archivo de aristas
fAristas = open('Aristas.csv', 'w')
fAristas.write("Source,Target,Type,Id,Weight" + "\n")
#Diccionario con el id del pais y los paises de los que recibe inmigrantes, con su id y peso
relacion = {}

for nombreArchivo in listaAristas:
	archivoAbrir = rutaAct + "/" + nombreArchivo
	#Se abre cada uno de los archivos
	fArchivo = open(archivoAbrir, 'r', encoding='utf-8')
	nombreArchivo = nombreArchivo.split("(")
	nombreArchivo = nombreArchivo[0].split("-")
	nombreArchivo.pop()
	nombreArchivo = " ".join(nombreArchivo)
	nombreArchivo = unidecode.unidecode(nombreArchivo)
	#Id asociado al nombre del país
	idDest = paisId.get(nombreArchivo)[0]
	line = fArchivo.readline()
	#Diccionario con la asociación del pais de donde proceden los inmigrantes y su peso
	paisesInmigrantes = {}
	#Se recorre el archivo con la información de los países de procedencia de los inmigrantes
	for linea in fArchivo.readlines():
		partir = linea.split(",")
		pais = partir[1]
		pais = pais.split("-")
		pais = ' '.join(pais)
		pais = unidecode.unidecode(pais[1:-1])
		#Id del país de procedencia
		idOr = paisId.get(pais)[0]
		#Pesos
		pesos = partir[2].split()
		pesos = pesos[0]
		pesos = pesos[1:-1]

		if len(pesos)>3:
			pesos = pesos.split(".")
			pesos= ''.join(pesos)

		paisesInmigrantes.update({idOr:pesos})

	relacion.update({idDest:paisesInmigrantes})

#-------------------------
#Insertamos en los archivos los diccionarios con la información recopilada

#Nodos
for key in paisId:
	id = paisId.get(key)[0]
	inmigrantes = paisId.get(key)[1]
	tasaNatalidad = paisId.get(key)[2]
	tasaMortalidad = paisId.get(key)[3]
	esperanzaDeVida = paisId.get(key)[4]
	if red == "2017":
		indicePaz = paisId.get(key)[5]
		capitalHumano = paisId.get(key)[6]
		desarrolloHumano = paisId.get(key)[7]
		fNodos.write(str(id) + ";" + key + ";" + str(inmigrantes) + ";" + str(tasaNatalidad) + ";" + str(tasaMortalidad) + ";" + str(esperanzaDeVida) + ";" +  str(indicePaz) +  ";" + str(capitalHumano) +  ";" + str(desarrolloHumano) + '\n')
	else:
		fNodos.write(str(id) + ";" + key + ";" + str(inmigrantes) + ";" + str(tasaNatalidad) + ";" + str(tasaMortalidad) + ";" + str(esperanzaDeVida) + '\n')

#Aristas
contAristas = 0
for key in relacion:
	dicRel = relacion.get(key)
	for r in dicRel:
		p = dicRel.get(r)
		fAristas.write(str(r) + "," + str(key) + ","+ "Directed" + "," + str(contAristas) + "," + str(p) + "\n")
		contAristas = contAristas + 1
