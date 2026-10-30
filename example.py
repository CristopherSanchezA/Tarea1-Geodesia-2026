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
    param = tj(sta, t_eq=t_eq, t_at=False, Do_plot=True, new_at=True, tau=15, t_cut=2017)
    break

# Corroborar largo de ruptura en el mata_noto.png


# Eliminar estaciones lejos del epicentro (Esto implica modificar a mano el id_coords).


# Arreglar el guardado del to_plot (tratar de que el guardado sea dentro del to_plot).
# Tratar de crear una recta en el t_eq del terremoto para que se vea mejor el salto en la figura.
# Añadir trench real (ayuda ayudante)

# Quitar/Achicar medio grado de Oeste a Este

print("fg_all")
print(param.keys()) # muestra los diccionarios que devuelve el modelo

# %%
##
station_dir = Path("pulled_data_terremoto noto 2024 japon")
station_ids = [
    line.split()[0]
    for line in (station_dir / "id_coords.txt").read_text().splitlines()
    if line.strip()
]

params = {}
for station_id in station_ids:
    station_file = station_dir / f"{station_id}.txt"
    params[station_id] = tj(
        str(station_file),
        t_eq=t_eq,
        t_at=False,
        Do_plot=True,
        new_at=True,
        tau=15,
        t_cut=False,
    )