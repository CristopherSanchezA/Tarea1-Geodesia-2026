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
ruta1 = f"{carpeta1}/vector_de_velocidades_ITRF_zona_estable_v2.txt"


# Marco del mapa
fig1.basemap(region=region, projection=projection, frame="a1g1f1") #Con frame determinamos el tamaño del marco, A1 indica el tick principal cada 1°, g la grilla principal cada 1° y f1 el tick secundario cada 1°

# Grilla
fig1.grdimage(grid=grid_file, cmap=paleta, projection=projection, region=region, frame=True) 

# Línea de costa
fig1.coast(region=region, projection=projection, shorelines="0.3p,black", borders=[1], rivers="a/0.1p,39/64/139", frame="a5f1", resolution="h")

data_stable = pd.read_csv(ruta1, sep="\t", header=None)
#data_stable[3] = data_stable[3] * 0.1  # Escalar velocidades
data_stable.to_csv("stable_scaled.txt", sep="\t", index=False, header=False)

#fig1.plot(data="trench.dat",pen="0.2p", style="f0.5i/0.1i+r+t+o1", fill="white")

fig1.velo(
    data="stable_scaled.txt",
    spec="e0.05/0.39/2",
    vector="0.3c+p1p+e+gred",
    pen="1p,red",
)
 
ruta2 = f"{carpeta1}/vector_de_velocidades_ITRF_zona_terremoto_v2.txt"

data_stable = pd.read_csv(ruta2, sep="\t", header=None)
#data_stable[3] = data_stable[3] * 0.1  # Escalar velocidades
data_stable.to_csv("eq_scaled.txt", sep="\t", index=False, header=False)
# Procesar y agregar datos para Turquía
fig1.velo(
    data="eq_scaled.txt",
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

ruta3 = "pred_zona_estable_v2.txt"

# Marco del mapa
fig2.basemap(region=region, projection=projection, frame="a1g1f1") #Con frame determinamos el tamaño del marco, A1 indica el tick principal cada 1°, g la grilla principal cada 1° y f1 el tick secundario cada 1°

# Grilla
fig2.grdimage(grid=grid_file, cmap=paleta, projection=projection, region=region, frame=True) 

# Línea de costa
fig2.coast(region=region, projection=projection, shorelines="0.3p,black", borders=[1], rivers="a/0.1p,39/64/139", frame="a5f1", resolution="h")

data_pred = pd.read_csv(ruta3, sep="\t", header=None)
#data_pred[3] = data_pred[3] * 0.1  # Escalar velocidades
data_pred.to_csv("stable_scaled_pred.txt", sep="\t", index=False, header=False)
fig2.velo(
    data="stable_scaled_pred.txt",
    spec="e0.05/0.39/2",
    vector="0.3c+p1p+e+gred",
    pen="1p,red",
)

ruta4 = "pred_zona_terremoto_v2.txt"

data_stable = pd.read_csv(ruta4, sep="\t", header=None)
#data_stable[3] = data_stable[3] * 0.1  # Escalar velocidades
data_stable.to_csv("eq_scaled_pred.txt", sep="\t", index=False, header=False)

# Procesar y agregar datos para Turquía
fig2.velo(
    data="eq_scaled_pred.txt",
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



ruta5 = f"{carpeta1}/vector_de_velocidades_ITRF_absoluta_v2.txt"
data_abs = pd.read_csv(ruta5, sep="\t", header=None)
#data_abs[3] = data_abs[3] * 0.1  # Escalar velocidades
data_abs.to_csv("stable_scaled_abs.txt", sep="\t", index=False, header=False)

ruta6 = "trench.dat"

# Trazar el límite de placa (trench) con una línea segmentada gruesa (roja o negra)
fig3.plot(
    data=ruta6,
    pen="1.5p,red,-",  # El "-" hace que la línea sea segmentada
    region=region,
    projection=projection
)

fig3.plot(x=142.37, y=38.30, style="a0.5c", pen="0.5p,black", fill="yellow") # Epicentro Terremoto 9.1 Mww de 2011

# Procesar y agregar datos para Turquía
fig3.velo(
    data="stable_scaled_abs.txt",
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