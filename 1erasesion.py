# %% Maxi shell
import numpy as np 

# %% Cris

from obspy.clients.fdsn import Client
from obspy import UTCDateTime

client = Client("USGS")
ti = UTCDateTime("2024-01-1T00:00:00")
tf = UTCDateTime("2024-01-2T00:00:00")
catalogo = client.get_events(starttime=ti, endtime=tf, minmagnitude=7.0, 
                             minlatitude=37, maxlatitude=38, 
                             minlongitude=137, maxlongitude=138)

print(catalogo)
catalogo.plot(outfile="figura.svg")

# %%

# Importamos la librerías
import pygmt

# Agregamos el nombre que le daremos el mapa
figname = 'Map_Noto_Japan.png'

# Creamos la base donde situaremos el mapa
fig = pygmt.Figure()

fig.basemap(
    region=[135.5, 139.5, 35.5,39.5],
    projection="M12c", # M12c para proyección Mercator(M) y ancho de 12 cm
    frame=["a1g1f1"])

fig.coast(
    shorelines="1/0.1p,black", # 1 de detalle / 0.3p = 0.3 puntos de grosor de las líneas, black = líneas costeras negras
    land="69/139/0",
    water="126/192/238",
    rivers="4/0.1p,135/206/255")

# Añadir el epicentro
fig.plot(
    x=[137.271],
    y=[37.487],
    style="a0.5c", # estrella de 0.5 cm de tamaño
    pen="0.5p,black", # borde 0.5 puntos de grosor, color negro
    fill="yellow", # color de relleno de la estrella
    label = "Epicentro")

fig.show()
 
#%%
import numpy as np
from datetime import datetime
# importo el modelo de trayectoria y otras funciones
from Trajectory_ayudantia import Trajectory as tj
from Trajectory_ayudantia import toYearFraction

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
    param = tj(sta, t_eq=t_eq, t_at=False, Do_plot=True, new_at=True, tau=15, t_cut=False)
    break

# %%
