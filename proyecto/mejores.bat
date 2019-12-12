@echo off
:while 
	python mejoresPaises.py
	set /p opcion = Calcular otro año (SI/NO): 
	if %opcion% == NO exit
	goto :while 
pause
exit