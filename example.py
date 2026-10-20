# %%
"""

Example to marcos
J.Hormazabal AGO 2022
"""
# importo librerias utiles
import numpy as np
from datetime import datetime
# importo el modelo de trayectoria y otras funciones
from Trajectory_ayudantia import Trajectory as tj
from Trajectory_ayudantia import toYearFraction

# estaión que quiero correr
sta = 'BN05.txt'
#sta = 'PATH.txt'
#name = antenas
# corro el modelo de trayectoria
# tiene estos inputs (solo es necesario el txt de la estación)
# ts_file: ruta a la estación
# t_eq = None : si quieres ingresar un terremoto
# el formato del tiempo del terremoto es en fracción de año
# usar: "t_eq_pisagua = toYearFraction(datetime(2014,4,1))" # fecha es año mes dia
# tau = None # para los postsismicos, se ingresan en dias
# t_at = False  
# en caso de querer usar saltos (estos se guardan en un .pickle y hay que crear el directorio)
# new_at = False 
# para agregar cambios de antena (hay que dejar el Do_plot = True para esto), se abrira al figura y uno pincha donde los quiere
# Do_plot = False
# para plotear las series de tiempo con el modelo
# t_cut = False
# para cortar las series de tiempo desde un ti

#t_eq_maule = toYearFraction(datetime(2010,2,27))
#t_eq_pisagua = toYearFraction(datetime(2014,4,1))
#param = tj(sta,  t_eq=[t_eq_pisagua], t_at=False, Do_plot=True, new_at=False, tau = 15, t_cut=2008)


#t_eq_illapel = toYearFraction(datetime(2015,9,16))
#param = tj(sta,  t_eq=[t_eq_illapel], t_at=False, Do_plot=True, 
		#		new_at=True,tau = 15, t_cut=False)


t_eq_valparaiso = toYearFraction(datetime(2017,4,24))
#param = tj(sta,  t_eq=[t_eq_illapel,t_eq_valparaiso], t_at=False, Do_plot=True, 
		#		new_at=True,tau = 15, t_cut=False)


#t_eq_sanantonio = toYearFraction(datetime(2016,10,27))
#param = tj(sta,  t_eq=[t_eq_illapel, t_eq_valparaiso, t_eq_sanantonio], t_at=True, Do_plot=True, 
				#new_at=True, tau = 15, t_cut=False)




t_eq_maule = toYearFraction(datetime(2010,2,27))
t_eq_calera = toYearFraction(datetime(2012,3,25))
t_eq_calera2 = toYearFraction(datetime(2012,4,17))
t_eq_sanantonio = toYearFraction(datetime(2014,3,4))
t_eq_sanantonio2 = toYearFraction(datetime(2016,10,27))
t_eq_calera3 = toYearFraction(datetime(2014,8,23))
t_eq_otro = toYearFraction(datetime(2014,4,5))
t_eq_illapel = toYearFraction(datetime(2015,9,16))
t_eq_valpo = toYearFraction(datetime(2017,4,27))
#t_eq_huasco = toYearFraction(datetime(2020,9,1))

#t_eq=[ t_eq_calera,t_eq_calera2, t_eq_otro, t_eq_calera3,t_eq_sanantonio, t_eq_illapel, t_eq_valpo]
t_eq=[  t_eq_calera, t_eq_calera2, t_eq_illapel, t_eq_valpo]
param = tj(sta,  t_eq=t_eq, t_at=False, Do_plot=True, 
				new_at=True, tau = 15, t_cut=False)

print("fg_all")
print(param.keys()) # muestra los diccionarios que devuelve el modelo
# Param tiene los "m" y "Cm"
# fg_all tiene la matriz G
# fg tiene todas las funciones bases separadas
# data tiene los datos (tiempo, ew, ns, up, sigm_Ew, sigm_ns, sigm_up)
# wrms son los errores cuadraticos medio con pesos respectivos

# %%
##
