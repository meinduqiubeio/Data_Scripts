@echo off
:while 
	python generarRed.py
	set /p opcion = Generar otra red (SI/NO): 
	if %opcion% == NO exit
	goto :while 
pause
exit