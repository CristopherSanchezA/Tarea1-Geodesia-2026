import pygmt
import os
import pandas as pd

# ---------------------------------------------------------
# Parámetros base del mapa
# ---------------------------------------------------------
region = [124.0, 142.5, 33.0, 44.5]
projection = "M12c"
paleta = "wiki-france.cpt"

input_grid = "ETOPO1_Ice_c_gmt4.grd"
grid_file = "topo_japon.grd"
carpeta1 = "velocidades_itrf"

# Generar grilla recortada (solo si no existe)
if not os.path.exists(grid_file):
    pygmt.grdcut(grid=input_grid, region=region, outgrid=grid_file)
    print(f"{grid_file} creado exitosamente.")

# Especificaciones de escala para fig.velo
# 'e0.005/0.95/0' -> 1 mm/año (o mm) = 0.005 cm en el mapa. Confianza 95%.
escala_velo = "e0.01/0.95/0" 

# ---------------------------------------------------------
# FIGURA 1: Velocidades / Desplazamientos GPS observados
# ---------------------------------------------------------
fig1 = pygmt.Figure()

# Basemap, Topografía y Costa
fig1.basemap(region=region, projection=projection, frame="a2f1g1")
fig1.grdimage(grid=grid_file, cmap=paleta, projection=projection, region=region)
fig1.coast(
    region=region, 
    projection=projection, 
    shorelines="0.3p,black", 
    borders=[1], 
    rivers="a/0.1p,39/64/139", 
    resolution="h"
)

# 1. Zona Estable (Amur) -> Vectores Rojos usando velo
ruta_estable = f"{carpeta1}/vector_de_velocidades_ITRF_zona_estable.txt"
if os.path.exists(ruta_estable):
    fig1.velo(
        data=ruta_estable,
        spec=escala_velo,
        vector="0.25c+p1p,red+e+gred",
        pen="0.8p,red",
        projection=projection,
        region=region
    )

# 2. Zona Terremoto (Japón) -> Vectores Azules usando velo
ruta_japon = f"{carpeta1}/vector_de_velocidades_ITRF_zona_terremoto.txt"
if os.path.exists(ruta_japon):
    fig1.velo(
        data=ruta_japon,
        spec=escala_velo,
        vector="0.25c+p1p,blue+e+gblue",
        pen="0.8p,blue",
        projection=projection,
        region=region
    )

fig1.savefig("mapa_velocidades_gps.pdf", dpi=600)
fig1.show()


# ---------------------------------------------------------
# FIGURA 2: Velocidades / Desplazamientos Predichos por el Modelo
# ---------------------------------------------------------
fig2 = pygmt.Figure()

fig2.basemap(region=region, projection=projection, frame="a2f1g1")
fig2.grdimage(grid=grid_file, cmap=paleta, projection=projection, region=region)
fig2.coast(
    region=region, 
    projection=projection, 
    shorelines="0.3p,black", 
    borders=[1], 
    rivers="a/0.1p,39/64/139", 
    resolution="h"
)

ruta_pred_estable = "pred_zonaestable.txt"
if os.path.exists(ruta_pred_estable):
    fig2.velo(
        data=ruta_pred_estable,
        spec=escala_velo,
        vector="0.25c+p1p,red+e+gred",
        pen="0.8p,red",
        projection=projection,
        region=region
    )

ruta_pred_japon = "pred_zonaterremoto.txt"
if os.path.exists(ruta_pred_japon):
    fig2.velo(
        data=ruta_pred_japon,
        spec=escala_velo,
        vector="0.25c+p1p,blue+e+gblue",
        pen="0.8p,blue",
        projection=projection,
        region=region
    )

fig2.savefig("mapa_velocidades_pred.pdf", dpi=600)
fig2.show()


# ---------------------------------------------------------
# FIGURA 3: Campo Absoluto / Cosísmico
# ---------------------------------------------------------
fig3 = pygmt.Figure()

fig3.basemap(region=region, projection=projection, frame="a2f1g1")
fig3.grdimage(grid=grid_file, cmap=paleta, projection=projection, region=region)
fig3.coast(
    region=region, 
    projection=projection, 
    shorelines="0.3p,black", 
    borders=[1], 
    rivers="a/0.1p,39/64/139", 
    resolution="h"
)

ruta_absoluta = f"{carpeta1}/vector_de_velocidades_ITRF_absoluta.txt"
if os.path.exists(ruta_absoluta):
    fig3.velo(
        data=ruta_absoluta,
        spec=escala_velo,
        vector="0.25c+p1p,blue+e+gblue",
        pen="0.8p,blue",
        projection=projection,
        region=region
    )

fig3.savefig("mapa_velocidades_eq.pdf", dpi=600)
fig3.show()