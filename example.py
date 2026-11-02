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
from pathlib import Path
import pylab as pl
# estaión que quiero correr
#sta = 'BN05.txt'

carpeta = "pulled_data_terremoto_noto_2024_japon"
ruta = f"{carpeta}/id_coords.txt"

matriz = np.loadtxt(ruta, dtype=str)
ID = matriz[:, 0]

t_eq_noto2024 = toYearFraction(datetime(2024, 1, 1))  # 7.5 Mww
t_eq_noto2023 = toYearFraction(datetime(2023, 5, 5))  # 6.3 Mww
t_eq = [t_eq_noto2024, t_eq_noto2023]

for codigo in ID:
    # Le indicamos a Python que el archivo está adentro de la subcarpeta
    sta = f"{carpeta}/{codigo}.txt"
    param = tj(sta, t_eq=t_eq, t_at=False, Do_plot=False, new_at=True, tau=15, t_cut=2017)

# Mover largo de ruptura en el mata_noto.png

# Tratar de crear una recta en el t_eq del terremoto para que se vea mejor el salto en la figura.

# Añadir trench real (ayuda ayudante)

# Quitar/Achicar medio grado de Oeste a Este

# Ejecutar example con tj cambiado a archivos de zona estable, y correr el inverso con el archivo obtenido 

print("fg_all")
print(param.keys()) # muestra los diccionarios que devuelve el modelo


# %%
