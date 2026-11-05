# Importamos las librerías que utilizaremos
import pygmt #Utilizamos pygmt para crear mapas
import xarray as xr #nos sirve para abrir, manipular y guardar grillas de datos 
import os #con esto trabajamos en archivos y directorios
import numpy as np #para trabajar con arreglos y funciones matemáticas
import matplotlib.pyplot as plt #para graficar y mostrar imágenes
import pandas as pd #para trabajar con tablas de datos


#Definimos parámetros base para la creación de nuestro mapa
name = "Mapa_final1.png"


region = [124.0, 142.5, 33.0, 44.5]   # más amplia
projection = "M12c"
jc = [137.25, 37.0, "0.9c"]
japan_region = [128, 147, 30, 46]

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


paleta = "wiki-france.cpt" # Paleta de colores # Pensar en cambiarlo por geo

# Cortar la topografía y guardarla como grilla (si no existe)

# Generar nuevamente la grilla para la región seleccionada
pygmt.grdcut(
    grid=input_grid,
    region=region,
    outgrid=grid_file
)

# Creamos la figura 1
fig1    = pygmt.Figure()

carpeta1 = "velocidades_itrf"
ruta1 = f"{carpeta1}/vector_de_velocidades_ITRF_zona_estable.txt"


# Marco del mapa
fig1.basemap(region=region, projection=projection, frame="a1g1f1") #Con frame determinamos el tamaño del marco, A1 indica el tick principal cada 1°, g la grilla principal cada 1° y f1 el tick secundario cada 1°

# Grilla
fig1.grdimage(grid=grid_file, cmap=paleta, projection=projection, region=region, frame=True) 

# Línea de costa
fig1.coast(region=region, projection=projection, shorelines="0.3p,black", borders=[1], rivers="a/0.1p,39/64/139", frame="a5f1", resolution="h")

data_stable = pd.read_csv(ruta1, sep="\t", header=None)
data_stable[3] = data_stable[3] * 0.1  # Escalar velocidades
data_stable.to_csv("stable_scaled.txt", sep="\t", index=False, header=False)
fig1.plot(
    data="stable_scaled.txt",
    style="V0.2c+e+gblack+h0+p1p,red",
    pen="1p,red",
    region=region,
    projection=projection,
)
 
ruta2 = f"{carpeta1}/vector_de_velocidades_ITRF_zona_terremoto.txt"

# Procesar y agregar datos para Turquía
fig1.velo(
    data=ruta2,
    spec="e0.05/0.39/2",
    vector="0.3c+p1p+e+gblue",
    pen="1p,blue",
)


fig1.show()
# Guardar mapa como PDF
fig1.savefig("mapa_velocidades_gps.pdf", dpi=600)

#figura 2:#################################################





# Creamos la figura
fig2 = pygmt.Figure()

ruta3 = "pred_zonaestable.txt"


# Marco del mapa
fig2.basemap(region=region, projection=projection, frame="a1g1f1") #Con frame determinamos el tamaño del marco, A1 indica el tick principal cada 1°, g la grilla principal cada 1° y f1 el tick secundario cada 1°

# Grilla
fig2.grdimage(grid=grid_file, cmap=paleta, projection=projection, region=region, frame=True) 

# Línea de costa
fig2.coast(region=region, projection=projection, shorelines="0.3p,black", borders=[1], rivers="a/0.1p,39/64/139", frame="a5f1", resolution="h")

data_pred = pd.read_csv(ruta3, sep="\t", header=None)
data_pred[3] = data_pred[3] * 0.1  # Escalar velocidades
data_pred.to_csv("stable_scaled_pred.txt", sep="\t", index=False, header=False)
fig2.plot(
    data="stable_scaled_pred.txt",
    style="V0.2c+e+gblack+h0+p1p,red",
    pen="1p,red",
    region=region,
    projection=projection,
)

ruta4 = "pred_zonaterremoto.txt"

# Procesar y agregar datos para Turquía
fig2.velo(
    data=ruta4,
    spec="e0.05/0.39/2",
    vector="0.3c+p1p+e+gblue",
    pen="1p,blue",
)


fig2.show()
# Guardar mapa como PDF
fig2.savefig("mapa_velocidades_pred.pdf", dpi=600)

#figura 3:#################################################





# Creamos la figura
fig3 = pygmt.Figure()



# Marco del mapa
fig3.basemap(region=region, projection=projection, frame="a1g1f1") #Con frame determinamos el tamaño del marco, A1 indica el tick principal cada 1°, g la grilla principal cada 1° y f1 el tick secundario cada 1°

# Grilla
fig3.grdimage(grid=grid_file, cmap=paleta, projection=projection, region=region, frame=True) 

# Línea de costa
fig3.coast(region=region, projection=projection, shorelines="0.3p,black", borders=[1], rivers="a/0.1p,39/64/139", frame="a5f1", resolution="h")



ruta5 = f"{carpeta1}/vector_de_velocidades_ITRF_absoluta.txt"

# Procesar y agregar datos para Turquía
fig3.velo(
    data=ruta5,
    spec="e0.05/0.39/2",
    vector="0.3c+p1p+e+gblue",
    pen="1p,blue",
)


fig3.show()
# Guardar mapa como PDF
fig3.savefig("mapa_velocidades_eq.pdf", dpi=600)


# Arreglar:
# 1. Ticks
# 2. Flechas (escala)
# 3. Colores
# 4. Títulos
# 5. Leyenda (fig1 y fig2)