# Importamos las librerías que utilizaremos
import pygmt #Utilizamos pygmt para crear mapas
import xarray as xr #nos sirve para abrir, manipular y guardar grillas de datos 
import os #con esto trabajamos en archivos y directorios
import numpy as np #para trabajar con arreglos y funciones matemáticas
import matplotlib.pyplot as plt #para graficar y mostrar imágenes


#Definimos parámetros base para la creación de nuestro mapa
name = "Mapa_Noto.png"

name = "Mapa_Noto.png"

region = [135.6, 140.0, 35.0, 39.2]   # más amplia
projection = "M12c"
jc = [137.25, 37.0, "0.9c"]
japan_region = [128, 147, 30, 46]


#paleta = "wiki-france.cpt" # Paleta de colores
paleta = "geo"

#Grilla de entrada y de salida
#input_grid = "ETOPO1_Ice_c_gmt4.grd"
input_grid = "gebco_2026_n39.2_s35.0_w135.6_e140.0.nc"
grid_file = "topo.grd"

# Cortar la topografía y guardarla como grilla (si no existe)

# Generar nuevamente la grilla para la región seleccionada
pygmt.grdcut(
    grid=input_grid,
    region=region,
    outgrid=grid_file
)

# Creamos la figura
fig = pygmt.Figure()

# Marco del mapa
fig.basemap(region=region, projection=projection, frame="a1g1f1") #Con frame determinamos el tamaño del marco, A1 indica el tick principal cada 1°, g la grilla principal cada 1° y f1 el tick secundario cada 1°

# Grilla
fig.grdimage(grid=grid_file, cmap=paleta, projection=projection, region=region, frame=True) 

# Línea de costa
fig.coast(region=region, projection=projection, shorelines="0.3p,black", borders=[1], rivers="a/0.1p,39/64/139", frame="a5f1", resolution="h")


ruta_F1SOE = "F1_S-O_E.txt"

fig.plot(
    data=ruta_F1SOE,
    # pen: Línea de 1.5 puntos de grosor, color rojo
    pen="1.2p,darkorange", 
    # style="f": frente de falla (inversa)
    # 0.4c: espacio entre triángulos
    # 0.15c: tamaño del triángulo
    # +r: triángulos a la derecha de la línea (dirección del Strike)
    # +t: forma de triángulo
    style="f0.25c/0.1c+r+t,darkorange", 
    #color="red", 
    label= "Subfalla 1-2 Suzu-Oki"
)

ruta_F2SOO = "F2_S-O_O.txt"

fig.plot(
    data=ruta_F2SOO,
    # pen: Línea de 1.5 puntos de grosor, color rojo
    pen="1.2p,darkorange", 
    # style="f": frente de falla (inversa)
    # 0.4c: espacio entre triángulos
    # 0.15c: tamaño del triángulo
    # +r: triángulos a la derecha de la línea (dirección del Strike)
    # +t: forma de triángulo
    style="f0.25c/0.1c+r+t,darkorange", 
    #color="red", 
    #label= "Subfalla 2 Suzu-Oki"
)

ruta_F3WOE = "F3_W-O_E.txt"

fig.plot(
    data=ruta_F3WOE,
    # pen: Línea de 1.5 puntos de grosor, color rojo
    pen="1.2p,black", 
    # style="f": frente de falla (inversa)
    # 0.4c: espacio entre triángulos
    # 0.15c: tamaño del triángulo
    # +r: triángulos a la derecha de la línea (dirección del Strike)
    # +t: forma de triángulo
    style="f0.25c/0.1c+r+t,black", 
    #color="red", 
    label= "Subfalla 3-4 Wajima-Oki"
)

ruta_F4WOE = "F4_W-O_O.txt"

fig.plot(
    data=ruta_F4WOE,
    # pen: Línea de 1.5 puntos de grosor, color rojo
    pen="1.2p,black", 
    # style="f": frente de falla (inversa)
    # 0.4c: espacio entre triángulos
    # 0.15c: tamaño del triángulo
    # +r: triángulos a la derecha de la línea (dirección del Strike)
    # +t: forma de triángulo
    style="f0.25c/0.1c+r+t,black", 
    #color="red", 
    #label= "Subfalla 4 Wajima-Oki"
)


fig.plot(x=137.271, 
         y=37.4875, 
         style="a0.5c", 
         pen="0.5p,black", 
         fill="yellow",
        label = "Epicentro"
)

red_points = [
    #[137.1477, 37.3103], #
    [137.2604, 37.4363],
    [136.8991, 37.3906],
    [136.9674, 37.0431],
    [138.3975, 38.0675],
    #[136.6565, 36.5611],
    [137.2136, 36.6959],
    [137.0257, 36.7541],
    [137.8626, 37.0390],
    #[139.0364, 37.9162], #
    #[138.1947, 36.6487], #
    [138.5578, 37.3648],
]

fig.plot(x=[p[0] for p in red_points], 
         y=[p[1] for p in red_points], 
         style="c0.2c", 
         pen="0.5p,black", 
         fill="red",
         label = "Ciudades"
)

# Nombre de ciudades
comunas = [
    #[137.3700, 37.4400, "Suzu"], #
    [137.2422, 37.29, "Noto"],
    [136.2820, 37.4210, "Wajima"], #136.2200, 37.3906
    [137.1000, 37.0521, "Nanao"],
    [138.4875, 38.0675, "Isla Sado"],
    #[136.7450, 36.5611, "Kanazawa"], #
    [137.3236, 36.7559, "Toyama"],
    [136.3157, 36.7541, "Takaoka"],
    [137.9726, 37.0590, "Itoigawa"],
    #[139.0994, 37.9162, "Niigata"], #
    #[138.2747, 36.6687, "Nagano"], #
    [138.6271, 37.3748, "Kashiwazaki"]
]

for comuna in comunas:
    fig.text(x=comuna[0], y=comuna[1], text=comuna[2], font="10p,Helvetica-Bold,black", fill="white", justify="LM")

fig.text(x=138.0101, 
         y=35.9651, 
         text="Japan", 
         font="18p,Helvetica-Bold,white=~1p,black", 
         justify="LM"
)

fig.plot(
    data="noto.txt",
    pen="2p,red",
    label = "Largo de Ruptura"
)

# Legend
fig.legend(position="JTR+jTR+o0.5c/0.5c", box="+gwhite+p1p")
fig.show()
# Guardar mapa como PDF
fig.savefig("mapa_noto.pdf", dpi=600)

# Convertir PDF a SVG