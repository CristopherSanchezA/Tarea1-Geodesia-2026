# Importamos las librerías que utilizaremos
import pygmt #Utilizamos pygmt para crear mapas
import xarray as xr #nos sirve para abrir, manipular y guardar grillas de datos 
import os #con esto trabajamos en archivos y directorios
import numpy as np #para trabajar con arreglos y funciones matemáticas
import matplotlib.pyplot as plt #para graficar y mostrar imágenes
import pandas as pd #para trabajar con tablas de datos


#Definimos parámetros base para la creación de nuestro mapa
name = "Mapa_estaciones_gps.pdf"


region = [124.0, 142.5, 33.0, 44.5]   # más amplia
projection = "M12c"
jc = [137.25, 37.0, "0.9c"]

input_grid = "ETOPO1_Ice_c_gmt4.grd"
grid_file = "topo_japon.grd"

# Cortar la topografía y guardarla como grilla (si no existe)
if not os.path.exists(grid_file):
    pygmt.grdcut(grid=input_grid, region=region, outgrid=grid_file) 
    print(f"{grid_file} created.")
else:
    print(f"{grid_file} already exists, skipping grdcut.")

# Verificar si 'topo.grd' se creó correctamente
if not os.path.exists(grid_file):
    raise FileNotFoundError(f"{grid_file} was not created.")


paleta = "geo" # Paleta de colores (más bonito según yo)

# Cortar la topografía y guardarla como grilla (si no existe)

# Generar nuevamente la grilla para la región seleccionada
pygmt.grdcut(
    grid=input_grid,
    region=region,
    outgrid=grid_file
)


# Creamos la figura 1

fig1 = pygmt.Figure()

fig1.basemap(region=region,
             projection=projection,
             frame=["WSne", "x3f1", "y2f2"]
) #Con frame determinamos el tamaño del marco, A1 indica el tick principal cada 1°, g la grilla principal cada 1° y f1 el tick secundario cada 1°

# Grilla
fig1.grdimage(grid=grid_file,
               cmap=paleta,
             projection=projection, 
             region=region
) # frame=True para mostrar la grilla de fondo

# Línea de costa
fig1.coast(region=region, 
           projection=projection, 
           shorelines="0.3p,black", 
           borders=[1], 
           rivers="a/0.1p,39/64/139", 
           resolution="h"
)

path1 = "pulled_data_terremoto_noto_2024_japon"
ruta1 = f"{path1}/id_coords.txt"

data_st_eq = np.loadtxt(ruta1, dtype=str)

lon_st_eq = data_st_eq[:,1]
lat_st_eq = data_st_eq[:,2]

fig1.plot(
    x=lon_st_eq.astype(float), 
    y=lat_st_eq.astype(float), 
    style="t0.2c",  
    pen="0.4p,black",
    fill="blue",
    label="Estaciones GPS zona de terremoto"
)

path2 = "pulled_data_zona_estable_AM"
ruta2 = f"{path2}/id_coords.txt"

data_st_sta = np.loadtxt(ruta2, dtype=str)

lon_st_sta = data_st_sta[:,1]
lat_st_sta = data_st_sta[:,2]

fig1.plot(
    x=lon_st_sta.astype(float), 
    y=lat_st_sta.astype(float), 
    style="t0.2c",
    pen="0.4p,black",
    fill="red",
    label="Estaciones GPS zona estable"
)

# LEYENDA (Top Right)
# position="JTR" la ancla arriba a la derecha (Justify Top Right)
# box="+gwhite+p1p" le da un fondo blanco sólido y un borde negro de 1 punto para que no se mezcle con la topografía
fig1.legend(position="JTR+jTR+o0.2c", box="+gwhite+p1p")

fig1.show()
# Guardar mapa como PDF
fig1.savefig(name, dpi=600)